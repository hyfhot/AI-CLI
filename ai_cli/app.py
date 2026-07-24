"""Main application logic."""
import os
import asyncio
import subprocess
import sys
import time
from typing import Optional, List, Tuple, Dict, Any
from ai_cli.config import ConfigManager
from ai_cli.models import Config, ProjectNode, Tool, ToolEnvironment
from ai_cli.ui.menu import MenuRenderer
from ai_cli.ui.input import InputHandler, InputEvent
from ai_cli.platform.factory import get_platform_adapter
from ai_cli.core.tools import ToolDetector
from ai_cli.core.installer import ToolInstaller
from ai_cli.core.updater import UpdateInfo, check_latest_version_async
from ai_cli.i18n import get_text


class Application:
    """Main application class."""
    
    def __init__(self, language: Optional[str] = None):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        
        # Initialize i18n
        from ai_cli.i18n import init_language
        # Priority: CLI argument > config file > auto
        if language:
            init_language(language)
        else:
            language = self.config.settings.language if hasattr(self.config.settings, 'language') else 'auto'
            init_language(language)
        
        self.menu = MenuRenderer()
        self.input_handler = InputHandler()
        self.platform_adapter = get_platform_adapter()
        self.tool_detector = ToolDetector()  # Single instance with cache
        self.tool_installer = ToolInstaller()  # Tool installer
        self.current_path: List[str] = []
        self.selected_project_index = 0  # For project selection
        self.selected_tool_index = 0  # For tool selection
        
        # Remember last selected tool (name + environment)
        self.last_selected_tool_name: Optional[str] = None
        self.last_selected_tool_env: Optional[ToolEnvironment] = None
        
        # Detect Windows Terminal availability once at startup
        self.wt_available = self._check_wt_available()
        
        # Current working directory at startup (for cwd awareness feature)
        self.startup_cwd = os.path.abspath(os.getcwd())

        # Update checker state
        self.update_info = UpdateInfo()
        self._start_update_check()
    
    def _check_wt_available(self) -> bool:
        """Check if Windows Terminal is available."""
        if sys.platform != 'win32':
            return False
        try:
            result = subprocess.run(["cmd.exe", "/c", "where", "wt"], 
                                  capture_output=True, timeout=2)
            return result.returncode == 0
        except:
            return False

    def _start_update_check(self):
        """Start background update check in a daemon thread."""
        def _on_result(info):
            self.update_info = info
        check_latest_version_async(on_done=_on_result)
    
    def _find_project_by_path(self, target_path: str):
        """
        Recursively search the project tree for a project matching target_path.
        
        Returns:
            (ProjectNode, breadcrumb_list) – breadcrumb_list is the list of
            folder names from root to the parent container.  Both are None if
            no match is found.
        """
        target = os.path.normpath(os.path.abspath(target_path))
        
        def search(nodes, breadcrumb):
            for node in nodes:
                if node.type == "project" and node.path:
                    node_path = os.path.normpath(os.path.abspath(node.path))
                    if node_path == target:
                        return (node, breadcrumb)
                if node.type == "folder" and node.children:
                    result = search(node.children, breadcrumb + [node.name])
                    if result[0] is not None:
                        return result
            return (None, None)
        
        return search(self.config.projects, [])
    
    def _find_project_by_name(self, name: str) -> Optional[ProjectNode]:
        """Search the project tree for a project or folder whose *name* matches."""
        def search(nodes):
            for node in nodes:
                if node.name == name:
                    return node
                if node.type == "folder":
                    result = search(node.children)
                    if result:
                        return result
            return None
        return search(self.config.projects)
    
    def _resolve_platform_enum(self, platform_name: str = None) -> ToolEnvironment:
        """Convert a CLI --platform string to a ToolEnvironment enum."""
        if platform_name:
            mapping = {
                "windows": ToolEnvironment.WINDOWS,
                "wsl":     ToolEnvironment.WSL,
                "linux":   ToolEnvironment.LINUX,
                "macos":   ToolEnvironment.MACOS,
            }
            return mapping.get(platform_name.lower(), ToolEnvironment.WINDOWS)
        if sys.platform == "win32":
            return ToolEnvironment.WINDOWS
        elif sys.platform == "darwin":
            return ToolEnvironment.MACOS
        else:
            return ToolEnvironment.LINUX
    
    def _resolve_direct_project(self, project_name: str, work_dir: str) -> ProjectNode:
        """
        Build a ProjectNode for direct-launch mode.
        
        Priority:
          1. If *project_name* is given, look it up in the config tree and
             return the stored node (which includes its env vars).
          2. Otherwise search the config tree for a project whose path equals
             *work_dir* (case-insensitive on Windows).
          3. Fall back to a transient ProjectNode with only the directory path.
        """
        if project_name:
            found = self._find_project_by_name(project_name)
            if found and found.type == "project":
                return found
        
        # Try to match work_dir to a configured project
        matched, _ = self._find_project_by_path(work_dir)
        if matched:
            return matched
        
        # Fallback: transient node
        dir_name = os.path.basename(work_dir) or work_dir
        return ProjectNode(
            type="project",
            name=dir_name,
            path=work_dir,
        )
    
    def run(self) -> None:
        """Main application loop."""
        # Start background tool detection (non-blocking)
        asyncio.run(self._start_background_detection())
        
        while True:
            try:
                # Check if background detection is complete
                if self.tool_detector.is_background_complete():
                    self.config_manager.save(self.config)  # Save updated cache to config
                    self.tool_detector.cleanup_background_task()
                
                project = self._select_project()
                if not project:
                    break
                
                result = asyncio.run(self._select_tool(project))
                if not result:
                    continue
                
                tool, new_tab, working_path, tool_items, selected_index, project_info = result
                # Create temporary project with working_path
                from copy import copy
                temp_project = copy(project)
                temp_project.path = working_path
                self._launch_tool(tool, temp_project, new_tab, tool_items, selected_index, project_info)
            except KeyboardInterrupt:
                break
            except Exception as e:
                import traceback
                self.menu.console.print(f"\n[red]Error: {e}[/red]")
                self.menu.console.print(f"[dim]{traceback.format_exc()}[/dim]")
                import time
                time.sleep(3)
                break
    
    def direct_launch(self, tool_name: str, project_name: str = None,
                      directory: str = None, platform_name: str = None) -> bool:
        """
        Direct-launch mode: skip the interactive UI and run *tool_name* in the
        current terminal, injecting any project-specific environment variables.
        
        Returns True if the tool exited with code 0.
        """
        # ---- resolve working directory ----
        if directory:
            work_dir = os.path.abspath(directory)
        elif project_name:
            found = self._find_project_by_name(project_name)
            if not found:
                self.menu.console.print(
                    f"[red]Project not found: {project_name}[/red]")
                return False
            work_dir = found.path or os.path.abspath(os.getcwd())
        else:
            work_dir = os.path.abspath(os.getcwd())
        
        # ---- resolve ProjectNode (with env vars if applicable) ----
        project = self._resolve_direct_project(project_name, work_dir)
        
        # ---- resolve tool config ----
        tool_config = next(
            (t for t in self.config.tools if t.name == tool_name), None)
        if not tool_config:
            self.menu.console.print(
                f"[red]Tool not found: {tool_name}[/red]")
            return False
        
        # ---- detect the tool on the requested platform ----
        target_env = self._resolve_platform_enum(platform_name)
        
        # Ensure detection has been run at least once
        asyncio.run(self.tool_detector.detect_all_tools(self.config.tools))
        tools = self.tool_detector._build_tool_list(self.config.tools)
        
        tool = next(
            (t for t in tools
             if t.name == tool_name and t.environment == target_env), None)
        if not tool:
            self.menu.console.print(
                f"[red]Tool '{tool_name}' is not available "
                f"on {target_env.value}[/red]")
            return False
        
        # ---- foreground execution ----
        exit_code = self.platform_adapter.run_in_current_terminal(tool, project)
        if exit_code == 0:
            # Record usage for this tool
            for tc in self.config.tools:
                if tc.name == tool.name:
                    tc.record_usage()
                    self.config_manager.save(self.config)
                    break
        return exit_code == 0
    
    async def _start_background_detection(self):
        """Start background tool detection."""
        self.tool_detector.start_background_detection(self.config.tools)
    
    def _select_project(self) -> Optional[ProjectNode]:
        """Project selection menu. Returns None only on Q (quit)."""
        from rich.live import Live
        
        # CWD auto-navigation flag – only trigger once per session
        if not getattr(self, '_cwd_resolved', False):
            self._cwd_resolved = True
            matched, breadcrumb = self._find_project_by_path(self.startup_cwd)
            if matched and breadcrumb:
                # Navigate into the folder hierarchy automatically
                self.current_path = breadcrumb
                self.selected_project_index = 0
            elif matched:
                # Match at root level – select its index
                for i, item in enumerate(self.config.projects):
                    if item is matched:
                        self.selected_project_index = i
                        break
        
        while True:
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            
            # ---- Build item list, optionally injecting cwd virtual item ----
            cwd_item = None
            if not self.current_path:
                matched, _ = self._find_project_by_path(self.startup_cwd)
                if not matched:
                    dir_name = os.path.basename(self.startup_cwd) or self.startup_cwd
                    cwd_item = {
                        "name": dir_name,
                        "type": "project",
                        "path": self.startup_cwd,
                        "children_count": 0,
                        "is_cwd": True,
                    }
            
            total_items = (1 if cwd_item else 0) + len(items)
            
            # Ensure selected_project_index is within bounds
            if total_items:
                self.selected_project_index = min(
                    self.selected_project_index, total_items - 1)
            else:
                self.selected_project_index = 0
            
            self.menu.clear()
            
            breadcrumb = ["Home"] + self.current_path
            
            # Build item list with path and children count
            item_list = []
            if cwd_item:
                item_list.append(cwd_item)
            for item in items:
                item_dict = {
                    "name": item.name,
                    "type": item.type,
                    "path": item.path if item.type == "project" else None,
                    "children_count": (
                        len(item.children)
                        if (item.type == "folder"
                            and hasattr(item, 'children')
                            and item.children)
                        else 0
                    )
                }
                item_list.append(item_dict)
            
            display = self.menu.build_tree_display(
                item_list,
                self.selected_project_index,
                breadcrumb=breadcrumb,
                update_info=self.update_info
            )
            
            result = None
            with Live(display, console=self.menu.console,
                      refresh_per_second=10, screen=True) as live:
                while True:
                    event = self.input_handler.get_input()
                    
                    if event == InputEvent.UP:
                        self.selected_project_index = max(
                            0, self.selected_project_index - 1)
                        live.update(self.menu.build_tree_display(
                            item_list,
                            self.selected_project_index,
                            breadcrumb=breadcrumb,
                            update_info=self.update_info
                        ))
                    elif event == InputEvent.DOWN:
                        self.selected_project_index = min(
                            total_items - 1, self.selected_project_index + 1)
                        live.update(self.menu.build_tree_display(
                            item_list,
                            self.selected_project_index,
                            breadcrumb=breadcrumb,
                            update_info=self.update_info
                        ))
                    elif event == InputEvent.UPDATE:
                        if self.update_info.is_update_available:
                            self._upgrade_and_restart()
                    elif event == InputEvent.ENTER:
                        effective_index = self.selected_project_index
                        if cwd_item:
                            if effective_index == 0:
                                # CWD virtual item selected
                                result = ProjectNode(
                                    type="project",
                                    name=(os.path.basename(self.startup_cwd)
                                          or self.startup_cwd),
                                    path=self.startup_cwd,
                                )
                                break
                            effective_index -= 1
                        selected = items[effective_index]
                        if selected.type == "folder":
                            self.current_path.append(selected.name)
                            self.selected_project_index = 0
                            break
                        else:
                            result = selected
                            break
                    elif event == InputEvent.NEW:
                        if cwd_item and self.selected_project_index == 0:
                            # Cannot edit the virtual CWD item
                            self.menu.console.print(
                                "\n[yellow]Current directory entry cannot "
                                "be modified.  Navigate into a folder first."
                                "[/yellow]"
                            )
                            time.sleep(1.5)
                            break
                        result = "__ADD_NEW__"
                        break
                    elif event == InputEvent.DELETE:
                        if cwd_item and self.selected_project_index == 0:
                            # Cannot delete the virtual CWD item
                            self.menu.console.print(
                                "\n[yellow]Current directory entry cannot "
                                "be deleted.[/yellow]"
                            )
                            time.sleep(1.5)
                            break
                        result = "__DELETE__"
                        break
                    elif event == InputEvent.ESCAPE:
                        if self.current_path:
                            self.current_path.pop()
                            self.selected_project_index = 0
                            break
                    elif event == InputEvent.QUIT:
                        result = None
                        break
            
            # Handle special actions after exiting Live context
            if result == "__ADD_NEW__":
                if self._add_new_item():
                    pass
                continue
            elif result == "__DELETE__":
                effective_index = (
                    self.selected_project_index - 1
                    if (cwd_item and self.selected_project_index > 0)
                    else self.selected_project_index
                )
                selected = items[effective_index]
                if self._delete_item(selected):
                    self.selected_project_index = 0
                continue
            
            if result is not None or event == InputEvent.QUIT:
                return result
    
    async def _select_tool(self, project: ProjectNode) -> Optional[Tuple]:
        """Tool selection menu. Returns (tool, new_tab) or None."""
        from rich.live import Live
        
        self.menu.clear()
        
        # Use working_path to avoid modifying project.path permanently
        working_path = project.path
        
        # Check for git worktrees and let user select if multiple exist
        if working_path:
            from ai_cli.core.git import GitManager

            # First verify this is a valid git repository
            try:
                subprocess.run(
                    ["git", "rev-parse", "--is-inside-work-tree"],
                    cwd=working_path,
                    capture_output=True,
                    check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Not a valid git repository, skip worktree detection
                pass
            else:
                try:
                    git_manager = GitManager()
                    worktrees = git_manager.detect_worktrees(working_path)

                    if len(worktrees) > 1:
                        selected_path = git_manager.select_worktree(
                            worktrees, working_path)
                        if selected_path:
                            working_path = selected_path
                        else:
                            return None
                        self.menu.clear()
                except subprocess.CalledProcessError:
                    # Git command failed during worktree detection
                    pass
                except Exception as e:
                    # Unexpected error during worktree detection - log it
                    import logging
                    logging.warning(f"Worktree detection failed: {e}")
                    pass
        
        # Prepare project info using working_path
        project_info = {
            'name': project.name,
            'path': working_path,
            'env': project.env if project.env else None
        }
        
        # Detect git branch if path exists
        if working_path:
            try:
                from ai_cli.core.git import GitDetector
                git_detector = GitDetector()
                branch = git_detector.get_current_branch(working_path)
                if branch:
                    project_info['branch'] = branch
            except:
                pass
        
        # Show detecting message in tool display
        self.menu.clear()
        from rich.live import Live
        from rich.text import Text
        from rich.console import Group
        
        detecting_lines = []
        if project_info:
            detecting_lines.append(
                Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}",
                     style="bold cyan"))
            if project_info.get('path'):
                detecting_lines.append(
                    Text(f"{get_text('path_label').format(project_info['path'])}",
                         style="dim"))
            if project_info.get('env'):
                env_str = ', '.join(
                    f"{k}={v}" for k, v in project_info['env'].items())
                detecting_lines.append(
                    Text(f"{get_text('env_label').format(env_str)}", style="dim"))
            if project_info.get('branch'):
                detecting_lines.append(
                    Text(f"{get_text('branch_label').format(project_info['branch'])}",
                         style="dim"))
        
        detecting_lines.append(
            Text(f"\n=== {get_text('select_tool')} ===\n", style="bold cyan"))
        detecting_lines.append(
            Text(f"  {get_text('detecting_tools')}", style="yellow"))
        detecting_display = Group(*detecting_lines)
        
        with Live(detecting_display, console=self.menu.console,
                  refresh_per_second=10, screen=False) as live:
            # Detect tools (uses cache from config if available)
            cache_was_empty = self.tool_detector._is_cache_empty(
                self.config.tools)
            tools = await self.tool_detector.detect_all_tools(self.config.tools)
            
            # Save config if detection was performed
            if cache_was_empty:
                self.config_manager.save(self.config)
            
            if not tools:
                self.menu.clear()
                self.menu.console.print(
                    f"\n[red]{get_text('no_tools')}[/red]")
                time.sleep(2)
                return None
        
        # Clear the detecting message
        self.menu.clear()
        
        # Build usage counts from tool configs
        usage_counts = {}  # (display_name, env) -> count
        for t in tools:
            tc = next((tc for tc in self.config.tools if tc.name == t.name), None)
            if tc:
                usage_counts[(t.display_name, t.environment.value)] = tc.usage_count_15d()
        
        # Sort state (default: by usage count, descending)
        sort_mode = "usage"
        sort_descending = True
        
        # Restore last selected tool BEFORE sorting (to know what to re-find)
        if 0 <= self.selected_tool_index < len(tools):
            prev_selected_name = tools[self.selected_tool_index].name
            prev_selected_env = tools[self.selected_tool_index].environment
        else:
            prev_selected_name = None
            prev_selected_env = None
        if self.last_selected_tool_name and self.last_selected_tool_env:
            prev_selected_name = self.last_selected_tool_name
            prev_selected_env = self.last_selected_tool_env
        
        # Sort tools by default rule (usage descending)
        if sort_mode == "usage":
            tools.sort(key=lambda t: usage_counts.get((t.display_name, t.environment.value), 0), reverse=sort_descending)
        else:
            tools.sort(key=lambda t: t.display_name.lower(), reverse=sort_descending)
        
        # Re-find selected index after sorting
        restored_index = 0
        if prev_selected_name and prev_selected_env:
            for i, tool in enumerate(tools):
                if (tool.name == prev_selected_name
                        and tool.environment == prev_selected_env):
                    restored_index = i
                    break
        if restored_index >= len(tools):
            restored_index = 0
       
        self.selected_tool_index = restored_index
        
        # Show tool list
        tool_items = []
        for t in tools:
            tool_items.append({
                "name": t.display_name,
                "env": t.environment.value
            })
        
        # Build initial display
        display = self.menu.build_tools_display(
            tool_items,
            self.selected_tool_index,
            show_new_tab=self.wt_available,
            project_info=project_info,
            update_info=self.update_info,
            usage_counts=usage_counts,
            sort_mode=sort_mode,
            sort_descending=sort_descending
        )
        
        result = None
        with Live(display, console=self.menu.console,
                  refresh_per_second=10, screen=True) as live:
            while True:
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    self.selected_tool_index = max(
                        0, self.selected_tool_index - 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available,
                        project_info=project_info,
                        update_info=self.update_info,
                        usage_counts=usage_counts,
                        sort_mode=sort_mode,
                        sort_descending=sort_descending
                    ))
                elif event == InputEvent.DOWN:
                    self.selected_tool_index = min(
                        len(tools) - 1, self.selected_tool_index + 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available,
                        project_info=project_info,
                        update_info=self.update_info,
                        usage_counts=usage_counts,
                        sort_mode=sort_mode,
                        sort_descending=sort_descending
                    ))
                elif event == InputEvent.UPDATE:
                    if self.update_info.is_update_available:
                        self._upgrade_and_restart()
                elif event == InputEvent.SORT:
                    # Cycle: usage↓ → usage↑ → name↓ → name↑ → usage↓
                    if sort_mode == "usage" and sort_descending:
                        sort_descending = False
                    elif sort_mode == "usage" and not sort_descending:
                        sort_mode = "name"
                        sort_descending = True
                    elif sort_mode == "name" and sort_descending:
                        sort_descending = False
                    else:  # name ascending → back to usage descending
                        sort_mode = "usage"
                        sort_descending = True
                    # Re-sort and rebuild tool_items
                    if sort_mode == "usage":
                        tools.sort(key=lambda t: usage_counts.get((t.display_name, t.environment.value), 0), reverse=sort_descending)
                    else:
                        tools.sort(key=lambda t: t.display_name.lower(), reverse=sort_descending)
                    tool_items = [
                        {"name": t.display_name, "env": t.environment.value}
                        for t in tools
                    ]
                    # Re-find the previously selected tool
                    if prev_selected_name and prev_selected_env:
                        for i, t in enumerate(tools):
                            if t.name == prev_selected_name and t.environment == prev_selected_env:
                                self.selected_tool_index = i
                                break
                        else:
                            self.selected_tool_index = 0
                    else:
                        self.selected_tool_index = 0
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available,
                        project_info=project_info,
                        update_info=self.update_info,
                        usage_counts=usage_counts,
                        sort_mode=sort_mode,
                        sort_descending=sort_descending
                    ))
                    # Track current selection for next sort
                    if self.selected_tool_index < len(tools):
                        prev_selected_name = tools[self.selected_tool_index].name
                        prev_selected_env = tools[self.selected_tool_index].environment
                elif event == InputEvent.ENTER:
                    selected_tool = tools[self.selected_tool_index]
                    # Save tool selection for next time
                    self.last_selected_tool_name = selected_tool.name
                    self.last_selected_tool_env = selected_tool.environment
                    result = (selected_tool, False, working_path,
                              tool_items, self.selected_tool_index,
                              project_info)
                    break
                elif event == InputEvent.NEW_TAB:
                    if self.wt_available:
                        selected_tool = tools[self.selected_tool_index]
                        self.last_selected_tool_name = selected_tool.name
                        self.last_selected_tool_env = selected_tool.environment
                        result = (selected_tool, True, working_path,
                                  tool_items, self.selected_tool_index,
                                  project_info)
                        break
                elif event == InputEvent.INSTALL:
                    result = ("INSTALL", None, working_path,
                              tool_items, self.selected_tool_index,
                              project_info)
                    break
                elif event == InputEvent.RUN:
                    # Show detecting message
                    from rich.text import Text
                    from rich.console import Group
                    
                    detecting_lines = []
                    if project_info:
                        detecting_lines.append(
                            Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}",
                                 style="bold cyan"))
                        if project_info.get('path'):
                            detecting_lines.append(
                                Text(f"{get_text('path_label').format(project_info['path'])}",
                                     style="dim"))
                        if project_info.get('env'):
                            env_str = ', '.join(
                                f"{k}={v}" for k, v in project_info['env'].items())
                            detecting_lines.append(
                                Text(f"{get_text('env_label').format(env_str)}",
                                     style="dim"))
                        if project_info.get('branch'):
                            detecting_lines.append(
                                Text(f"{get_text('branch_label').format(project_info['branch'])}",
                                     style="dim"))
                    
                    detecting_lines.append(
                        Text(f"\n=== {get_text('select_tool')} ===\n",
                             style="bold cyan"))
                    detecting_lines.append(
                        Text(f"  {get_text('refreshing')}", style="yellow"))
                    live.update(Group(*detecting_lines))
                    
                    # Force detection and save config
                    tools = await self.tool_detector.detect_all_tools(
                        self.config.tools, force=True)
                    self.config_manager.save(self.config)
                    
                    if not tools:
                        msg_lines = []
                        if project_info:
                            msg_lines.append(
                                Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}",
                                     style="bold cyan"))
                            if project_info.get('path'):
                                msg_lines.append(
                                    Text(f"{get_text('path_label').format(project_info['path'])}",
                                         style="dim"))
                            if project_info.get('env'):
                                env_str = ', '.join(
                                    f"{k}={v}" for k, v in project_info['env'].items())
                                msg_lines.append(
                                    Text(f"{get_text('env_label').format(env_str)}",
                                         style="dim"))
                            if project_info.get('branch'):
                                msg_lines.append(
                                    Text(f"{get_text('branch_label').format(project_info['branch'])}",
                                         style="dim"))
                        
                        msg_lines.append(
                            Text(f"\n=== {get_text('select_tool')} ===\n",
                                 style="bold cyan"))
                        msg_lines.append(
                            Text(f"\n[red]{get_text('no_tools')}[/red]",
                                 style="red"))
                        msg_lines.append(
                            Text(f"\n[dim][I] {get_text('install')} | "
                                 f"[Esc] {get_text('back')}[/dim]",
                                 style="dim"))
                        live.update(Group(*msg_lines))
                        continue
                    
                    # Rebuild usage counts after refresh
                    usage_counts = {}
                    for t in tools:
                        tc = next((tc for tc in self.config.tools if tc.name == t.name), None)
                        if tc:
                            usage_counts[(t.display_name, t.environment.value)] = tc.usage_count_15d()
                    
                    # Re-sort
                    if sort_mode == "usage":
                        tools.sort(key=lambda t: usage_counts.get((t.display_name, t.environment.value), 0), reverse=sort_descending)
                    else:
                        tools.sort(key=lambda t: t.display_name.lower(), reverse=sort_descending)
                    
                    # Restore last selected tool
                    if self.last_selected_tool_name and self.last_selected_tool_env:
                        for i, tool in enumerate(tools):
                            if (tool.name == self.last_selected_tool_name
                                    and tool.environment == self.last_selected_tool_env):
                                self.selected_tool_index = i
                                break
                        else:
                            if self.selected_tool_index >= len(tools):
                                self.selected_tool_index = 0
                    else:
                        if self.selected_tool_index >= len(tools):
                            self.selected_tool_index = 0
                    
                    tool_items = [
                        {"name": t.display_name, "env": t.environment.value}
                        for t in tools
                    ]
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available,
                        project_info=project_info,
                        update_info=self.update_info,
                        usage_counts=usage_counts,
                        sort_mode=sort_mode,
                        sort_descending=sort_descending
                    ))
                elif event == InputEvent.ESCAPE:
                    result = None
                    break
                elif event == InputEvent.QUIT:
                    raise KeyboardInterrupt
        
        # Handle INSTALL outside Live context
        if result and result[0] == "INSTALL":
            await self._install_tool_menu()
            return await self._select_tool(project)
        
        return result
    
    def _launch_tool(self, tool: Tool, project: ProjectNode, new_tab: bool = False, 
                     tool_items: List = None, selected_index: int = 0,
                     project_info: Dict = None) -> None:
        """Launch tool in terminal."""
        import time
        from rich.live import Live
        from rich.text import Text
        
        # Clear screen and redisplay tool list with launch info
        self.menu.clear()
        
        # Display tool list if provided
        if tool_items and project_info:
            display = self.menu.build_tools_display(
                tool_items,
                selected_index,
                show_new_tab=self.wt_available,
                project_info=project_info
            )
            self.menu.console.print(display)
        
        try:
            self.platform_adapter.launch_terminal(
                tool, project, new_tab=new_tab, wt_available=self.wt_available)
            tab_mode = "new tab" if new_tab else "new window"
            self.menu.console.print(
                f"\n[green]✓ Launched {tool.name} for {project.name} "
                f"in {tab_mode}[/green]")
            
            # Record usage for this tool
            for tc in self.config.tools:
                if tc.name == tool.name:
                    tc.record_usage()
                    self.config_manager.save(self.config)
                    break
            
            # Use Text objects to avoid markup interpretation
            from rich.text import Text
            self.menu.console.print(
                Text(get_text('tool_label').format(tool.name), style="dim"))
            self.menu.console.print(
                Text(get_text('project_label').format(project.name), style="dim"))
            self.menu.console.print(
                Text(get_text('path_label').format(project.path), style="dim"))
            
            # Display project environment variables if any
            if project.env:
                env_str = ', '.join(
                    f"{k}={v}" for k, v in project.env.items())
                self.menu.console.print(
                    Text(get_text('env_label').format(env_str), style="dim"))
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console,
                      refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(
                        get_text('returning_to_selection').format(i),
                        style="yellow"))
                    time.sleep(1)
        except Exception as e:
            self.menu.console.print(
                f"\n[red]{get_text('failed_to_launch').format(e)}[/red]")
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console,
                      refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(
                        get_text('returning_to_selection').format(i),
                        style="yellow"))
                    time.sleep(1)

    def _upgrade_and_restart(self):
        """Trigger self-upgrade with user confirmation message."""
        if not self.update_info.is_update_available:
            return
        self.menu.clear()
        self.menu.console.print(
            f"\n[yellow]{get_text('update_upgrading')}[/yellow]")
        self.menu.console.print(
            f"[dim]{get_text('update_restarting')}[/dim]\n")
        time.sleep(1)
        from ai_cli.core.updater import perform_upgrade
        perform_upgrade()

    async def _install_tool_menu(self):
        """Show menu to install uninstalled tools.
        Returns True if any tool was installed successfully."""
        force_refresh = False
        
        while True:
            all_tools_config = self.config.tools
            
            if force_refresh:
                detected_tools = await self.tool_detector.detect_all_tools(
                    all_tools_config, force=True)
                self.config_manager.save(self.config)
                force_refresh = False
            else:
                cache_was_empty = self.tool_detector._is_cache_empty(
                    all_tools_config)
                detected_tools = await self.tool_detector.detect_all_tools(
                    all_tools_config)
                if cache_was_empty:
                    self.config_manager.save(self.config)
            
            detected_names = {(t.name, t.environment) for t in detected_tools}
            
            # Build list of uninstalled tools
            uninstalled = []
            for tool_config in all_tools_config:
                # Check WSL
                if (tool_config.wsl_install
                        and (tool_config.name, ToolEnvironment.WSL)
                        not in detected_names):
                    uninstalled.append({
                        "name": f"[WSL] {tool_config.display_name}",
                        "tool": tool_config,
                        "env": ToolEnvironment.WSL
                    })
                # Check Windows
                if (sys.platform == 'win32' and tool_config.win_install
                        and (tool_config.name, ToolEnvironment.WINDOWS)
                        not in detected_names):
                    uninstalled.append({
                        "name": f"[Win] {tool_config.display_name}",
                        "tool": tool_config,
                        "env": ToolEnvironment.WINDOWS
                    })
                # Check Linux
                if (sys.platform == 'linux' and tool_config.linux_install
                        and (tool_config.name, ToolEnvironment.LINUX)
                        not in detected_names):
                    uninstalled.append({
                        "name": f"[Linux] {tool_config.display_name}",
                        "tool": tool_config,
                        "env": ToolEnvironment.LINUX
                    })
                # Check macOS
                if (sys.platform == 'darwin' and tool_config.macos_install
                        and (tool_config.name, ToolEnvironment.MACOS)
                        not in detected_names):
                    uninstalled.append({
                        "name": f"[macOS] {tool_config.display_name}",
                        "tool": tool_config,
                        "env": ToolEnvironment.MACOS
                    })
            
            if not uninstalled:
                return False
            
            # Show selection menu
            selected_index = 0
            action_result = None
            
            while action_result is None:
                self.menu.clear()
                self.menu.console.print(
                    f"\n[cyan]{get_text('install')}[/cyan]\n")
                
                for i, item in enumerate(uninstalled):
                    prefix = "→ " if i == selected_index else "  "
                    self.menu.console.print(f"{prefix}{item['name']}")
                
                self.menu.console.print(
                    f"\n[dim]↑↓: {get_text('navigate')} | "
                    f"Enter: {get_text('install')} | "
                    f"Esc: {get_text('back')}[/dim]")
                
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    selected_index = max(0, selected_index - 1)
                elif event == InputEvent.DOWN:
                    selected_index = min(
                        len(uninstalled) - 1, selected_index + 1)
                elif event == InputEvent.ENTER:
                    selected = uninstalled[selected_index]
                    self.menu.clear()
                    self.menu.console.print(
                        f"\n[cyan]{get_text('installing', selected['name'])}"
                        f"[/cyan]\n")
                    
                    install_cmd = self.tool_installer._get_install_command(
                        selected['tool'], selected['env'])
                    if install_cmd:
                        self.menu.console.print(
                            f"[dim]Command: {install_cmd}[/dim]\n")
                    
                    try:
                        success = self.tool_installer.install_tool(
                            selected['tool'], selected['env'])
                        
                        if success:
                            self.menu.console.print(
                                f"\n[green]{get_text('install_success')}"
                                f"[/green]")
                            force_refresh = True
                        else:
                            self.menu.console.print(
                                f"\n[red]{get_text('install_failed', 'Unknown error')}"
                                f"[/red]")
                    except Exception as e:
                        self.menu.console.print(
                            f"\n[red]{get_text('install_failed', str(e))}"
                            f"[/red]")
                    
                    self.menu.console.print(
                        f"\n[dim]{get_text('press_key')}[/dim]")
                    self.input_handler.get_input()
                    action_result = "refresh"
                elif event == InputEvent.ESCAPE or event == InputEvent.QUIT:
                    return True
    
    def _get_current_node(self) -> Optional[ProjectNode]:
        """Get current node from path."""
        node = None
        items = self.config.projects
        
        for name in self.current_path:
            for item in items:
                if item.name == name:
                    node = item
                    items = item.children
                    break
        
        return node
    
    def _add_new_item(self) -> bool:
        """Add new project or folder. Returns True if added successfully."""
        from rich.live import Live
        from rich.text import Text
        from rich.console import Group
        
        # Step 1: Select type with up/down keys
        self.menu.clear()
        types = ["Project", "Folder"]
        selected_type = 0
        
        def build_type_display():
            lines = []
            lines.append(Text(
                f"\n=== {get_text('add_new_item')} ===\n", style="bold cyan"))
            lines.append(Text(f"{get_text('select_type')}\n", style="cyan"))
            
            for i, type_name in enumerate(types):
                icon = "📁" if type_name == "Folder" else "📄"
                prefix = "> " if i == selected_type else "  "
                style = "green" if i == selected_type else "white"
                lines.append(Text(f"{prefix}{icon} {type_name}", style=style))
            
            lines.append(Text(
                f"\n[↑↓] {get_text('navigate')}  [Enter] {get_text('confirm')}"
                f"  [Esc] {get_text('cancel')}  [Q] {get_text('quit')}",
                style="dim"))
            return Group(*lines)
        
        with Live(build_type_display(), console=self.menu.console,
                  refresh_per_second=10, screen=False) as live:
            while True:
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    selected_type = max(0, selected_type - 1)
                    live.update(build_type_display())
                elif event == InputEvent.DOWN:
                    selected_type = min(len(types) - 1, selected_type + 1)
                    live.update(build_type_display())
                elif event == InputEvent.ENTER:
                    break
                elif event == InputEvent.ESCAPE:
                    return False
                elif event == InputEvent.QUIT:
                    raise KeyboardInterrupt
        
        item_type = "project" if selected_type == 0 else "folder"
        
        # Step 2: Input name with ESC support
        self.menu.clear()
        self.menu.console.print(f"\n[cyan]{get_text('add_new_item')}[/cyan]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print(
            f"\n{get_text('type', item_type.capitalize())}")
        self.menu.console.print(
            f"\n[dim]{get_text('press_esc_cancel')}[/dim]\n")
        
        # Loop until valid name or cancel
        while True:
            prompt_key = ('project_name' if item_type == 'project'
                          else 'folder_name')
            item_name = self.input_handler.get_text_input(
                get_text(prompt_key))
            if item_name is None:
                return False
            
            if not item_name:
                self.menu.console.print(
                    f"[red]{get_text('name_required')}[/red]")
                continue
            
            # Check for duplicate names
            current_node = self._get_current_node()
            items = (current_node.children if current_node
                     else self.config.projects)
            if any(item.name == item_name for item in items):
                self.menu.console.print(
                    f"[red]{get_text('name_exists', item_name)}[/red]")
                continue
            
            break
        
        if item_type == "folder":
            new_item = ProjectNode(
                type="folder", name=item_name, path="", children=[])
            
            self.menu.console.print(
                f"\n[cyan]{get_text('folder_summary')}[/cyan]")
            self.menu.console.print(get_text('item_name', item_name))
            self.menu.console.print()
            
            confirm = self.input_handler.get_text_input(
                get_text('add_folder_confirm'))
            if confirm is None:
                return False
            if confirm and confirm.lower() != 'y':
                return False
            
            self._add_item_to_current_path(new_item)
            self.config_manager.save(self.config)
            self.menu.console.print(
                f"[green]{get_text('folder_added')}[/green]")
            time.sleep(1)
            return True
        
        # Project needs path
        current_dir = os.getcwd()
        self.menu.console.print(
            f"[dim]{get_text('current_dir_hint', current_dir)}[/dim]")
        
        project_path = self.input_handler.get_text_input(
            get_text('project_path'))
        if project_path is None:
            return False
        
        if not project_path:
            project_path = current_dir
        
        # Check if path exists
        if not os.path.exists(project_path):
            confirm = self.input_handler.get_text_input(
                get_text('path_not_exist', project_path))
            if confirm is None:
                return False
            if confirm and confirm.lower() == 'n':
                return False
            
            try:
                os.makedirs(project_path, exist_ok=True)
                self.menu.console.print(
                    f"[green]{get_text('dir_created')}[/green]")
            except Exception as e:
                self.menu.console.print(
                    f"[red]{get_text('dir_create_failed', e)}[/red]")
                time.sleep(2)
                return False
        
        # Get environment variables
        self.menu.console.print(
            f"\n[cyan]{get_text('env_vars_title')}[/cyan]")
        self.menu.console.print(
            f"[dim]{get_text('env_vars_format')}[/dim]\n")
        
        env_vars = {}
        while True:
            env_input = self.input_handler.get_text_input(
                get_text('env_var_prompt'))
            if env_input is None:
                return False
            
            if not env_input:
                break
            
            if "=" in env_input:
                key, value = env_input.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key:
                    env_vars[key] = value
                    self.menu.console.print(
                        get_text('env_added', key, value))
                else:
                    self.menu.console.print(
                        f"  [red]{get_text('env_invalid_empty')}[/red]")
            else:
                self.menu.console.print(
                    f"  [red]{get_text('env_invalid_format')}[/red]")
        
        # Create project
        new_project = ProjectNode(
            type="project",
            name=item_name,
            path=project_path,
            env=env_vars if env_vars else None
        )
        
        # Show summary
        self.menu.console.print(
            f"\n[cyan]{get_text('project_summary')}[/cyan]")
        self.menu.console.print(get_text('item_name', item_name))
        self.menu.console.print(
            get_text('project_path_label', project_path))
        if env_vars:
            self.menu.console.print(
                get_text('project_env_count', len(env_vars)))
            for key, value in env_vars.items():
                self.menu.console.print(f"    [dim]{key}={value}[/dim]")
        self.menu.console.print()
        
        confirm = self.input_handler.get_text_input(
            get_text('add_project_confirm'))
        if confirm is None:
            return False
        
        if confirm and confirm.lower() != 'y':
            return False
        
        self._add_item_to_current_path(new_project)
        self.config_manager.save(self.config)
        self.menu.console.print(
            f"[green]{get_text('project_added')}[/green]")
        time.sleep(1)
        return True
    
    def _delete_item(self, item: ProjectNode) -> bool:
        """Delete project or folder. Returns True if deleted successfully."""
        from rich.prompt import Prompt
        from ai_cli.core.projects import ProjectManager
        
        self.menu.clear()
        self.menu.console.print(
            f"\n[red]{get_text('delete_confirmation')}[/red]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print()
        
        icon = "📁" if item.type == "folder" else "📄"
        self.menu.console.print(
            f"[yellow]{get_text('item_to_delete', icon, item.name)}[/yellow]")
        
        if item.type == "folder":
            count = ProjectManager.count_children_recursive(item)
            self.menu.console.print(
                f"[yellow]{get_text('contains', count)}[/yellow]")
        else:
            self.menu.console.print(
                f"[dim]{get_text('path_label', item.path)}[/dim]")
        
        self.menu.console.print()
        self.menu.console.print(
            f"[red]{get_text('warning_cannot_undo')}[/red]")
        self.menu.console.print()
        
        try:
            confirmation = Prompt.ask(
                f"[cyan]{get_text('type_name_confirm')}[/cyan]")
            
            if confirmation == item.name:
                self._remove_item_from_current_path(item.name)
                self.config_manager.save(self.config)
                self.menu.console.print(
                    f"[green]{get_text('deleted_successfully')}[/green]")
                time.sleep(1)
                return True
            else:
                self.menu.console.print(
                    f"[yellow]{get_text('name_mismatch')}[/yellow]")
                time.sleep(1)
                return False
        except KeyboardInterrupt:
            self.menu.console.print(
                f"\n[yellow]{get_text('cancelled')}[/yellow]")
            time.sleep(1)
            return False
    
    def _add_item_to_current_path(self, item: ProjectNode) -> None:
        """Add item to current path in config."""
        if not self.current_path:
            self.config.projects.append(item)
        else:
            current_node = self._get_current_node()
            if current_node:
                current_node.children.append(item)
    
    def _remove_item_from_current_path(self, item_name: str) -> None:
        """Remove item from current path in config."""
        if not self.current_path:
            self.config.projects = [
                p for p in self.config.projects if p.name != item_name]
        else:
            current_node = self._get_current_node()
            if current_node:
                current_node.children = [
                    c for c in current_node.children
                    if c.name != item_name]