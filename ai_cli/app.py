"""Main application logic."""
import asyncio
import subprocess
import sys
import time
from typing import Optional, List, Tuple
from ai_cli.config import ConfigManager
from ai_cli.models import Config, ProjectNode, Tool, ToolEnvironment
from ai_cli.ui.menu import MenuRenderer
from ai_cli.ui.input import InputHandler, InputEvent
from ai_cli.platform.factory import get_platform_adapter
from ai_cli.core.tools import ToolDetector
from ai_cli.core.installer import ToolInstaller
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
        
        # Detect Windows Terminal availability once at startup
        self.wt_available = self._check_wt_available()
    
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
                
                tool, new_tab, working_path = result
                # Create temporary project with working_path
                from copy import copy
                temp_project = copy(project)
                temp_project.path = working_path
                self._launch_tool(tool, temp_project, new_tab)
            except KeyboardInterrupt:
                break
            except Exception as e:
                import traceback
                self.menu.console.print(f"\n[red]Error: {e}[/red]")
                self.menu.console.print(f"[dim]{traceback.format_exc()}[/dim]")
                import time
                time.sleep(3)
                break
    
    async def _start_background_detection(self):
        """Start background tool detection."""
        self.tool_detector.start_background_detection(self.config.tools)
    
    def _select_project(self) -> Optional[ProjectNode]:
        """Project selection menu. Returns None only on Q (quit)."""
        from rich.live import Live
        
        while True:
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            
            # Ensure selected_project_index is within bounds
            if items:
                self.selected_project_index = min(self.selected_project_index, len(items) - 1)
            else:
                self.selected_project_index = 0
            
            self.menu.clear()
            
            breadcrumb = ["Home"] + self.current_path
            
            # Build item list with path and children count
            item_list = []
            for item in items:
                item_dict = {
                    "name": item.name,
                    "type": item.type,
                    "path": item.path if item.type == "project" else None,
                    "children_count": len(item.children) if (item.type == "folder" and hasattr(item, 'children') and item.children) else 0
                }
                item_list.append(item_dict)
            
            display = self.menu.build_tree_display(
                item_list,
                self.selected_project_index,
                breadcrumb=breadcrumb
            )
            
            result = None
            with Live(display, console=self.menu.console, refresh_per_second=10, screen=True) as live:
                while True:
                    event = self.input_handler.get_input()
                    
                    if event == InputEvent.UP:
                        self.selected_project_index = max(0, self.selected_project_index - 1)
                        live.update(self.menu.build_tree_display(
                            item_list,
                            self.selected_project_index,
                            breadcrumb=breadcrumb
                        ))
                    elif event == InputEvent.DOWN:
                        self.selected_project_index = min(len(items) - 1, self.selected_project_index + 1)
                        live.update(self.menu.build_tree_display(
                            item_list,
                            self.selected_project_index,
                            breadcrumb=breadcrumb
                        ))
                    elif event == InputEvent.ENTER:
                        selected = items[self.selected_project_index]
                        if selected.type == "folder":
                            self.current_path.append(selected.name)
                            self.selected_project_index = 0  # Reset when entering folder
                            break
                        else:
                            result = selected
                            # Don't reset selected_index - keep it for when we return
                            break
                    elif event == InputEvent.NEW:
                        # Exit Live context before showing add dialog
                        result = "__ADD_NEW__"
                        break
                    elif event == InputEvent.DELETE:
                        # Exit Live context before showing delete dialog
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
                    # Refresh and continue
                    pass
                continue
            elif result == "__DELETE__":
                selected = items[self.selected_project_index]
                if self._delete_item(selected):
                    # Refresh and continue
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
            try:
                from ai_cli.core.git import GitManager
                git_manager = GitManager()
                worktrees = git_manager.detect_worktrees(working_path)
                
                if len(worktrees) > 1:
                    selected_path = git_manager.select_worktree(worktrees, working_path)
                    if selected_path:
                        working_path = selected_path
                    else:
                        return None
                    self.menu.clear()
            except Exception as e:
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
            detecting_lines.append(Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}", style="bold cyan"))
            if project_info.get('path'):
                detecting_lines.append(Text(f"{get_text('path_label').format(project_info['path'])}", style="dim"))
            if project_info.get('env'):
                env_str = ', '.join(f"{k}={v}" for k, v in project_info['env'].items())
                detecting_lines.append(Text(f"{get_text('env_label').format(env_str)}", style="dim"))
            if project_info.get('branch'):
                detecting_lines.append(Text(f"{get_text('branch_label').format(project_info['branch'])}", style="dim"))
        
        detecting_lines.append(Text(f"\n=== {get_text('select_tool')} ===\n", style="bold cyan"))
        detecting_lines.append(Text(f"  {get_text('detecting_tools')}", style="yellow"))
        detecting_display = Group(*detecting_lines)
        
        with Live(detecting_display, console=self.menu.console, refresh_per_second=10, screen=False) as live:
            # Detect tools with progress indicator (uses cache from config if available)
            cache_was_empty = self.tool_detector._is_cache_empty(self.config.tools)
            tools = await self.tool_detector.detect_all_tools(self.config.tools)
            
            # Save config if detection was performed
            if cache_was_empty:
                self.config_manager.save(self.config)
            
            if not tools:
                self.menu.clear()
                self.menu.console.print(f"\n[red]{get_text('no_tools')}[/red]")
                time.sleep(2)
                return None
            
            self.selected_tool_index = 0
            
            # Show tool list
            tool_items = []
            for t in tools:
                tool_items.append({
                    "name": t.display_name,  # Use display_name without env label
                    "env": t.environment.value  # Pass env separately
                })
            
            # Update with actual tool list
            display = self.menu.build_tools_display(
                tool_items,
                self.selected_tool_index,
                show_new_tab=self.wt_available,
                project_info=project_info
            )
            live.update(display)
        
        result = None
        with Live(display, console=self.menu.console, refresh_per_second=10, screen=True) as live:
            while True:
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    self.selected_tool_index = max(0, self.selected_tool_index - 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.DOWN:
                    self.selected_tool_index = min(len(tools) - 1, self.selected_tool_index + 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.ENTER:
                    result = (tools[self.selected_tool_index], False, working_path)
                    break
                elif event == InputEvent.NEW_TAB:
                    if self.wt_available:
                        result = (tools[self.selected_tool_index], True, working_path)
                        break
                elif event == InputEvent.INSTALL:
                    all_installed = not await self._install_tool_menu()
                    # Force detection and save config if tools were installed
                    if not all_installed:
                        tools = await self.tool_detector.detect_all_tools(self.config.tools, force=True)
                        self.config_manager.save(self.config)
                    else:
                        # Check if cache was empty before detection
                        cache_was_empty = self.tool_detector._is_cache_empty(self.config.tools)
                        tools = await self.tool_detector.detect_all_tools(self.config.tools)
                        if cache_was_empty:
                            self.config_manager.save(self.config)
                    
                    if not tools:
                        result = None
                        break
                    tool_items = [{"name": t.display_name, "env": t.environment.value} for t in tools]
                    
                    # Show message if all tools were already installed
                    if all_installed:
                        from rich.text import Text
                        from rich.console import Group
                        
                        msg_lines = []
                        if project_info:
                            msg_lines.append(Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}", style="bold cyan"))
                            if project_info.get('path'):
                                msg_lines.append(Text(f"{get_text('path_label').format(project_info['path'])}", style="dim"))
                            if project_info.get('env'):
                                env_str = ', '.join(f"{k}={v}" for k, v in project_info['env'].items())
                                msg_lines.append(Text(f"{get_text('env_label').format(env_str)}", style="dim"))
                            if project_info.get('branch'):
                                msg_lines.append(Text(f"{get_text('branch_label').format(project_info['branch'])}", style="dim"))
                        
                        msg_lines.append(Text(f"\n=== {get_text('select_tool')} ===\n", style="bold cyan"))
                        msg_lines.append(Text(f"  {get_text('all_tools_installed')}", style="green"))
                        live.update(Group(*msg_lines))
                        
                        # Wait 2 seconds then show tool list
                        import asyncio
                        await asyncio.sleep(2)
                    
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.RUN:
                    # Show detecting message
                    from rich.text import Text
                    from rich.console import Group
                    
                    detecting_lines = []
                    if project_info:
                        detecting_lines.append(Text(f"\n{get_text('project_label').format(project_info.get('name', 'Unknown'))}", style="bold cyan"))
                        if project_info.get('path'):
                            detecting_lines.append(Text(f"{get_text('path_label').format(project_info['path'])}", style="dim"))
                        if project_info.get('env'):
                            env_str = ', '.join(f"{k}={v}" for k, v in project_info['env'].items())
                            detecting_lines.append(Text(f"{get_text('env_label').format(env_str)}", style="dim"))
                        if project_info.get('branch'):
                            detecting_lines.append(Text(f"{get_text('branch_label').format(project_info['branch'])}", style="dim"))
                    
                    detecting_lines.append(Text(f"\n=== {get_text('select_tool')} ===\n", style="bold cyan"))
                    detecting_lines.append(Text(f"  {get_text('refreshing')}", style="yellow"))
                    live.update(Group(*detecting_lines))
                    
                    # Force detection and save config
                    tools = await self.tool_detector.detect_all_tools(self.config.tools, force=True)
                    self.config_manager.save(self.config)
                    
                    if not tools:
                        self.menu.console.print(f"\n[red]{get_text('no_tools')}[/red]")
                        time.sleep(1)
                        result = None
                        break
                    tool_items = [{"name": t.display_name, "env": t.environment.value} for t in tools]
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_tool_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.ESCAPE:
                    result = None
                    break
                elif event == InputEvent.QUIT:
                    raise KeyboardInterrupt
        
        return result
    
    def _launch_tool(self, tool: Tool, project: ProjectNode, new_tab: bool = False) -> None:
        """Launch tool in terminal."""
        import time
        from rich.live import Live
        from rich.text import Text
        
        try:
            self.platform_adapter.launch_terminal(tool, project, new_tab=new_tab, wt_available=self.wt_available)
            tab_mode = "new tab" if new_tab else "new window"
            self.menu.console.print(f"\n[green]✓ Launched {tool.name} for {project.name} in {tab_mode}[/green]")
            
            # Use Text objects to avoid markup interpretation
            from rich.text import Text
            self.menu.console.print(Text(get_text('tool_label').format(tool.name), style="dim"))
            self.menu.console.print(Text(get_text('project_label').format(project.name), style="dim"))
            self.menu.console.print(Text(get_text('path_label').format(project.path), style="dim"))
            
            # Display project environment variables if any
            if project.env:
                env_str = ', '.join(f"{k}={v}" for k, v in project.env.items())
                self.menu.console.print(Text(get_text('env_label').format(env_str), style="dim"))
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console, refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(get_text('returning_to_selection').format(i), style="yellow"))
                    time.sleep(1)
        except Exception as e:
            self.menu.console.print(f"\n[red]{get_text('failed_to_launch').format(e)}[/red]")
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console, refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(get_text('returning_to_selection').format(i), style="yellow"))
                    time.sleep(1)
    
    async def _install_tool_menu(self):
        """Show menu to install uninstalled tools. Returns True if tools were installed."""
        # Get all tools and check which are not installed
        all_tools_config = self.config.tools
        cache_was_empty = self.tool_detector._is_cache_empty(all_tools_config)
        detected_tools = await self.tool_detector.detect_all_tools(all_tools_config)
        
        # Save config if detection was performed
        if cache_was_empty:
            self.config_manager.save(self.config)
        
        detected_names = {(t.name, t.environment) for t in detected_tools}
        
        # Build list of uninstalled tools
        uninstalled = []
        for tool_config in all_tools_config:
            # Check WSL
            if tool_config.wsl_install and (tool_config.name, ToolEnvironment.WSL) not in detected_names:
                uninstalled.append({
                    "name": f"[WSL] {tool_config.display_name}",
                    "tool": tool_config,
                    "env": ToolEnvironment.WSL
                })
            # Check Windows
            if sys.platform == 'win32' and tool_config.win_install and (tool_config.name, ToolEnvironment.WINDOWS) not in detected_names:
                uninstalled.append({
                    "name": f"[Win] {tool_config.display_name}",
                    "tool": tool_config,
                    "env": ToolEnvironment.WINDOWS
                })
            # Check Linux
            if sys.platform == 'linux' and tool_config.linux_install and (tool_config.name, ToolEnvironment.LINUX) not in detected_names:
                uninstalled.append({
                    "name": f"[Linux] {tool_config.display_name}",
                    "tool": tool_config,
                    "env": ToolEnvironment.LINUX
                })
            # Check macOS
            if sys.platform == 'darwin' and tool_config.macos_install and (tool_config.name, ToolEnvironment.MACOS) not in detected_names:
                uninstalled.append({
                    "name": f"[macOS] {tool_config.display_name}",
                    "tool": tool_config,
                    "env": ToolEnvironment.MACOS
                })
        
        if not uninstalled:
            return False  # Return False to indicate all tools installed
        
        # Show selection menu
        selected_index = 0
        while True:
            self.menu.clear()
            self.menu.console.print(f"\n[cyan]{get_text('install')}[/cyan]\n")
            
            for i, item in enumerate(uninstalled):
                prefix = "→ " if i == selected_index else "  "
                self.menu.console.print(f"{prefix}{item['name']}")
            
            self.menu.console.print(f"\n[dim]↑↓: Navigate | Enter: {get_text('install')} | Esc: {get_text('back')}[/dim]")
            
            event = self.input_handler.get_input()
            
            if event == InputEvent.UP:
                selected_index = max(0, selected_index - 1)
            elif event == InputEvent.DOWN:
                selected_index = min(len(uninstalled) - 1, selected_index + 1)
            elif event == InputEvent.ENTER:
                # Install selected tool
                selected = uninstalled[selected_index]
                self.menu.clear()
                self.menu.console.print(f"\n[cyan]{get_text('installing', selected['name'])}[/cyan]\n")
                
                success = self.tool_installer.install_tool(selected['tool'], selected['env'])
                
                if success:
                    self.menu.console.print(f"\n[green]{get_text('install_success')}[/green]")
                else:
                    self.menu.console.print(f"\n[red]{get_text('install_failed', 'Unknown error')}[/red]")
                
                self.menu.console.print(f"\n[dim]{get_text('press_key')}[/dim]")
                self.input_handler.get_input()
                return True  # Return True to indicate installation was attempted
            elif event == InputEvent.ESCAPE or event == InputEvent.QUIT:
                return True  # Return True to continue normal flow
    
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
        import os
        from rich.live import Live
        from rich.text import Text
        from rich.console import Group
        
        # Step 1: Select type with up/down keys
        self.menu.clear()
        types = ["Project", "Folder"]
        selected_type = 0
        
        def build_type_display():
            lines = []
            lines.append(Text(f"\n=== {get_text('add_new_item')} ===\n", style="bold cyan"))
            lines.append(Text(f"{get_text('select_type')}\n", style="cyan"))
            
            for i, type_name in enumerate(types):
                icon = "📁" if type_name == "Folder" else "📄"
                prefix = "> " if i == selected_type else "  "
                style = "green" if i == selected_type else "white"
                lines.append(Text(f"{prefix}{icon} {type_name}", style=style))
            
            lines.append(Text("\n[↑↓] Navigate  [Enter] Confirm  [Esc] Cancel  [Q] Quit", style="dim"))
            return Group(*lines)
        
        with Live(build_type_display(), console=self.menu.console, refresh_per_second=10, screen=False) as live:
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
        self.menu.console.print(f"\n{get_text('type', item_type.capitalize())}")
        self.menu.console.print(f"\n[dim]{get_text('press_esc_cancel')}[/dim]\n")
        
        # Loop until valid name or cancel
        while True:
            prompt_key = 'project_name' if item_type == 'project' else 'folder_name'
            item_name = self.input_handler.get_text_input(get_text(prompt_key))
            if item_name is None:
                return False
            
            if not item_name:
                self.menu.console.print(f"[red]{get_text('name_required')}[/red]")
                continue
            
            # Check for duplicate names
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            if any(item.name == item_name for item in items):
                self.menu.console.print(f"[red]{get_text('name_exists', item_name)}[/red]")
                continue
            
            # Valid name, break the loop
            break
        
        if item_type == "folder":
            # Create folder
            new_item = ProjectNode(type="folder", name=item_name, path="", children=[])
            
            self.menu.console.print(f"\n[cyan]{get_text('folder_summary')}[/cyan]")
            self.menu.console.print(get_text('item_name', item_name))
            self.menu.console.print()
            
            confirm = self.input_handler.get_text_input(get_text('add_folder_confirm'))
            if confirm is None:
                return False
            if confirm and confirm.lower() != 'y':
                return False
            
            self._add_item_to_current_path(new_item)
            self.config_manager.save(self.config)
            self.menu.console.print(f"[green]{get_text('folder_added')}[/green]")
            time.sleep(1)
            return True
        
        # Project needs path
        current_dir = os.getcwd()
        self.menu.console.print(f"[dim]{get_text('current_dir_hint', current_dir)}[/dim]")
        
        project_path = self.input_handler.get_text_input(get_text('project_path'))
        if project_path is None:
            return False
        
        if not project_path:
            project_path = current_dir
        
        # Check if path exists
        if not os.path.exists(project_path):
            confirm = self.input_handler.get_text_input(get_text('path_not_exist', project_path))
            if confirm is None:
                return False
            if confirm and confirm.lower() == 'n':
                return False
            
            try:
                os.makedirs(project_path, exist_ok=True)
                self.menu.console.print(f"[green]{get_text('dir_created')}[/green]")
            except Exception as e:
                self.menu.console.print(f"[red]{get_text('dir_create_failed', e)}[/red]")
                time.sleep(2)
                return False
        
        # Get environment variables
        self.menu.console.print(f"\n[cyan]{get_text('env_vars_title')}[/cyan]")
        self.menu.console.print(f"[dim]{get_text('env_vars_format')}[/dim]\n")
        
        env_vars = {}
        while True:
            env_input = self.input_handler.get_text_input(get_text('env_var_prompt'))
            if env_input is None:
                return False
            
            if not env_input:
                break
            
            if "=" in env_input:
                key, value = env_input.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key:  # Ensure key is not empty
                    env_vars[key] = value
                    self.menu.console.print(get_text('env_added', key, value))
                else:
                    self.menu.console.print(f"  [red]{get_text('env_invalid_empty')}[/red]")
            else:
                self.menu.console.print(f"  [red]{get_text('env_invalid_format')}[/red]")
        
        # Create project
        new_project = ProjectNode(
            type="project",
            name=item_name,
            path=project_path,
            env=env_vars if env_vars else None
        )
        
        # Show summary
        self.menu.console.print(f"\n[cyan]{get_text('project_summary')}[/cyan]")
        self.menu.console.print(get_text('item_name', item_name))
        self.menu.console.print(get_text('project_path_label', project_path))
        if env_vars:
            self.menu.console.print(get_text('project_env_count', len(env_vars)))
            for key, value in env_vars.items():
                self.menu.console.print(f"    [dim]{key}={value}[/dim]")
        self.menu.console.print()
        
        confirm = self.input_handler.get_text_input(get_text('add_project_confirm'))
        if confirm is None:
            return False
        
        # Empty input or 'y'/'Y' means yes, anything else means no
        if confirm and confirm.lower() != 'y':
            return False
        
        self._add_item_to_current_path(new_project)
        self.config_manager.save(self.config)
        self.menu.console.print(f"[green]{get_text('project_added')}[/green]")
        time.sleep(1)
        return True
    
    def _delete_item(self, item: ProjectNode) -> bool:
        """Delete project or folder. Returns True if deleted successfully."""
        from rich.prompt import Prompt
        from ai_cli.core.projects import ProjectManager
        
        self.menu.clear()
        self.menu.console.print(f"\n[red]{get_text('delete_confirmation')}[/red]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print()
        
        icon = "📁" if item.type == "folder" else "📄"
        self.menu.console.print(f"[yellow]{get_text('item_to_delete', icon, item.name)}[/yellow]")
        
        if item.type == "folder":
            count = ProjectManager.count_children_recursive(item)
            self.menu.console.print(f"[yellow]{get_text('contains', count)}[/yellow]")
        else:
            self.menu.console.print(f"[dim]{get_text('path_label', item.path)}[/dim]")
        
        self.menu.console.print()
        self.menu.console.print(f"[red]{get_text('warning_cannot_undo')}[/red]")
        self.menu.console.print()
        
        try:
            confirmation = Prompt.ask(f"[cyan]{get_text('type_name_confirm')}[/cyan]")
            
            if confirmation == item.name:
                self._remove_item_from_current_path(item.name)
                self.config_manager.save(self.config)
                self.menu.console.print(f"[green]{get_text('deleted_successfully')}[/green]")
                time.sleep(1)
                return True
            else:
                self.menu.console.print(f"[yellow]{get_text('name_mismatch')}[/yellow]")
                time.sleep(1)
                return False
        except KeyboardInterrupt:
            self.menu.console.print(f"\n[yellow]{get_text('cancelled')}[/yellow]")
            time.sleep(1)
            return False
    
    def _add_item_to_current_path(self, item: ProjectNode) -> None:
        """Add item to current path in config."""
        if not self.current_path:
            # Add to root
            self.config.projects.append(item)
        else:
            # Navigate to current folder and add
            current_node = self._get_current_node()
            if current_node:
                current_node.children.append(item)
    
    def _remove_item_from_current_path(self, item_name: str) -> None:
        """Remove item from current path in config."""
        if not self.current_path:
            # Remove from root
            self.config.projects = [p for p in self.config.projects if p.name != item_name]
        else:
            # Navigate to current folder and remove
            current_node = self._get_current_node()
            if current_node:
                current_node.children = [c for c in current_node.children if c.name != item_name]
