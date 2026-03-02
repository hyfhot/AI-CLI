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
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        
        # Initialize i18n
        from ai_cli.i18n import init_language
        language = self.config.settings.language if hasattr(self.config.settings, 'language') else 'auto'
        init_language(language)
        
        self.menu = MenuRenderer()
        self.input_handler = InputHandler()
        self.platform_adapter = get_platform_adapter()
        self.tool_detector = ToolDetector()  # Single instance with cache
        self.tool_installer = ToolInstaller()  # Tool installer
        self.current_path: List[str] = []
        self.selected_index = 0
        
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
                print(f"Error: {e}")
    
    async def _start_background_detection(self):
        """Start background tool detection."""
        self.tool_detector.start_background_detection(self.config.tools)
    
    def _select_project(self) -> Optional[ProjectNode]:
        """Project selection menu. Returns None only on Q (quit)."""
        from rich.live import Live
        
        while True:
            self.menu.clear()
            
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            
            # Handle empty project list
            if not items:
                self.menu.console.print("\n[yellow]No projects configured. Press 'N' to add a project or 'Q' to quit.[/yellow]")
                event = self.input_handler.get_input()
                if event == InputEvent.NEW:
                    if self._add_new_item():
                        # After adding, continue to show the menu
                        continue
                    else:
                        continue
                elif event == InputEvent.QUIT:
                    return None
                continue
            
            breadcrumb = ["Home"] + self.current_path
            display = self.menu.build_tree_display(
                [{"name": item.name, "type": item.type} for item in items],
                self.selected_index,
                breadcrumb=breadcrumb
            )
            
            result = None
            with Live(display, console=self.menu.console, refresh_per_second=10, screen=True) as live:
                while True:
                    event = self.input_handler.get_input()
                    
                    if event == InputEvent.UP:
                        self.selected_index = max(0, self.selected_index - 1)
                        live.update(self.menu.build_tree_display(
                            [{"name": item.name, "type": item.type} for item in items],
                            self.selected_index,
                            breadcrumb=breadcrumb
                        ))
                    elif event == InputEvent.DOWN:
                        self.selected_index = min(len(items) - 1, self.selected_index + 1)
                        live.update(self.menu.build_tree_display(
                            [{"name": item.name, "type": item.type} for item in items],
                            self.selected_index,
                            breadcrumb=breadcrumb
                        ))
                    elif event == InputEvent.ENTER:
                        selected = items[self.selected_index]
                        if selected.type == "folder":
                            self.current_path.append(selected.name)
                            self.selected_index = 0
                            break
                        else:
                            result = selected
                            break
                    elif event == InputEvent.NEW:
                        if self._add_new_item():
                            # Refresh items after adding
                            current_node = self._get_current_node()
                            items = current_node.children if current_node else self.config.projects
                            self.selected_index = min(self.selected_index, len(items) - 1) if items else 0
                        break
                    elif event == InputEvent.DELETE:
                        selected = items[self.selected_index]
                        if self._delete_item(selected):
                            # Refresh items after deletion
                            current_node = self._get_current_node()
                            items = current_node.children if current_node else self.config.projects
                            self.selected_index = min(self.selected_index, len(items) - 1) if items else 0
                        break
                    elif event == InputEvent.ESCAPE:
                        if self.current_path:
                            self.current_path.pop()
                            self.selected_index = 0
                            break
                    elif event == InputEvent.QUIT:
                        result = None
                        break
            
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
        
        # Detect tools with progress indicator (uses cache if available)
        self.menu.console.print(f"[yellow]{get_text('detecting_tools')}[/yellow]")
        tools = await self.tool_detector.detect_all_tools(self.config.tools)
        
        if not tools:
            self.menu.console.print(f"\n[red]{get_text('no_tools')}[/red]")
            time.sleep(2)
            return None
        
        self.selected_index = 0
        
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
        
        # Show tool list
        tool_items = []
        for t in tools:
            tool_items.append({
                "name": t.get_display_label()
            })
        
        self.menu.clear()
        display = self.menu.build_tools_display(
            tool_items,
            self.selected_index,
            show_new_tab=self.wt_available,
            project_info=project_info
        )
        
        result = None
        with Live(display, console=self.menu.console, refresh_per_second=10, screen=True) as live:
            while True:
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    self.selected_index = max(0, self.selected_index - 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.DOWN:
                    self.selected_index = min(len(tools) - 1, self.selected_index + 1)
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.ENTER:
                    result = (tools[self.selected_index], False, working_path)
                    break
                elif event == InputEvent.NEW_TAB:
                    if self.wt_available:
                        result = (tools[self.selected_index], True, working_path)
                        break
                elif event == InputEvent.INSTALL:
                    await self._install_tool_menu()
                    self.tool_detector.clear_cache()
                    tools = await self.tool_detector.detect_all_tools(self.config.tools)
                    if not tools:
                        result = None
                        break
                    tool_items = [{"name": t.get_display_label()} for t in tools]
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.RUN:
                    self.menu.console.print(f"\n[yellow]{get_text('refreshing')}[/yellow]")
                    self.tool_detector.clear_cache()
                    tools = await self.tool_detector.detect_all_tools(self.config.tools)
                    if not tools:
                        self.menu.console.print(f"\n[red]{get_text('no_tools')}[/red]")
                        time.sleep(1)
                        result = None
                        break
                    tool_items = [{"name": t.get_display_label()} for t in tools]
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_index,
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
            self.menu.console.print(f"[dim]Tool: {tool.name}[/dim]")
            self.menu.console.print(f"[dim]Project: {project.name}[/dim]")
            self.menu.console.print(f"[dim]Path: {project.path}[/dim]")
            self.menu.console.print(f"[dim]Environment: {tool.environment.value}[/dim]")
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console, refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(f"Returning to project selection in {i} seconds...", style="yellow"))
                    time.sleep(1)
        except Exception as e:
            self.menu.console.print(f"\n[red]✗ Failed to launch tool: {e}[/red]")
            
            # Countdown 5 seconds with live update
            with Live(Text(""), console=self.menu.console, refresh_per_second=4) as live:
                for i in range(5, 0, -1):
                    live.update(Text(f"Returning to project selection in {i} seconds...", style="yellow"))
                    time.sleep(1)
    
    async def _install_tool_menu(self):
        """Show menu to install uninstalled tools."""
        # Get all tools and check which are not installed
        all_tools_config = self.config.tools
        detected_tools = await self.tool_detector.detect_all_tools(all_tools_config)
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
            self.menu.console.print(f"\n[green]{get_text('install_success')}[/green]")
            time.sleep(1)
            return
        
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
                return
            elif event == InputEvent.ESCAPE or event == InputEvent.QUIT:
                return
    
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
        from rich.prompt import Prompt, Confirm
        
        self.menu.clear()
        self.menu.console.print("\n[cyan]Add New Item[/cyan]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print()
        
        # Select type
        self.menu.console.print("[cyan]Select Type:[/cyan]")
        self.menu.console.print("  1. Project")
        self.menu.console.print("  2. Folder")
        self.menu.console.print("\n[dim]Press ESC to cancel[/dim]")
        
        type_choice = None
        while type_choice is None:
            event = self.input_handler.get_input()
            if event == InputEvent.QUIT or event == InputEvent.ESCAPE:
                return False
            # Check for number keys
            import sys
            if sys.platform == 'win32':
                # On Windows, we need to handle this differently
                pass
            # For now, use prompt
            break
        
        self.menu.clear()
        self.menu.console.print("\n[cyan]Add New Item[/cyan]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print("\n[dim](Press Ctrl+C to cancel)[/dim]\n")
        
        try:
            # Get type
            type_input = Prompt.ask("[cyan]Type[/cyan] (1=Project, 2=Folder)", default="1")
            if type_input not in ["1", "2"]:
                self.menu.console.print("[red]Invalid type[/red]")
                time.sleep(1)
                return False
            
            item_type = "project" if type_input == "1" else "folder"
            
            # Get name
            item_name = Prompt.ask(f"[cyan]{item_type.capitalize()} Name[/cyan]")
            if not item_name or not item_name.strip():
                self.menu.console.print("[red]Name is required[/red]")
                time.sleep(1)
                return False
            
            item_name = item_name.strip()
            
            # Check for duplicate names
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            if any(item.name == item_name for item in items):
                self.menu.console.print(f"[red]Name '{item_name}' already exists in current location[/red]")
                time.sleep(2)
                return False
            
            if item_type == "folder":
                # Create folder
                new_item = ProjectNode(type="folder", name=item_name, path="", children=[])
                
                self.menu.console.print("\n[cyan]Folder Summary:[/cyan]")
                self.menu.console.print(f"  Name: {item_name}")
                self.menu.console.print()
                
                if Confirm.ask("[yellow]Add this folder?[/yellow]", default=True):
                    self._add_item_to_current_path(new_item)
                    self.config_manager.save(self.config)
                    self.menu.console.print("[green]Folder added successfully![/green]")
                    time.sleep(1)
                    return True
                return False
            
            # Project needs path
            current_dir = os.getcwd()
            self.menu.console.print(f"[dim](Press Enter to use current directory: {current_dir})[/dim]")
            
            project_path = Prompt.ask("[cyan]Project Path[/cyan]", default=current_dir)
            if not project_path:
                project_path = current_dir
            
            # Check if path exists
            if not os.path.exists(project_path):
                if Confirm.ask(f"[yellow]Path does not exist: {project_path}\nCreate it?[/yellow]", default=False):
                    try:
                        os.makedirs(project_path, exist_ok=True)
                        self.menu.console.print("[green]Directory created successfully[/green]")
                    except Exception as e:
                        self.menu.console.print(f"[red]Failed to create directory: {e}[/red]")
                        time.sleep(2)
                        return False
                else:
                    return False
            
            # Get environment variables
            self.menu.console.print("\n[cyan]Environment Variables (optional)[/cyan]")
            self.menu.console.print("[dim]Format: KEY=VALUE, one per line, empty line to finish[/dim]\n")
            
            env_vars = {}
            while True:
                env_input = Prompt.ask("[cyan]Env Var[/cyan]", default="")
                if not env_input:
                    break
                
                if "=" in env_input:
                    key, value = env_input.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    env_vars[key] = value
                    self.menu.console.print(f"  [green]Added: {key}={value}[/green]")
                else:
                    self.menu.console.print("  [red]Invalid format. Use KEY=VALUE[/red]")
            
            # Create project
            new_project = ProjectNode(
                type="project",
                name=item_name,
                path=project_path,
                env=env_vars if env_vars else None
            )
            
            # Show summary
            self.menu.console.print("\n[cyan]Project Summary:[/cyan]")
            self.menu.console.print(f"  Name: {item_name}")
            self.menu.console.print(f"  Path: {project_path}")
            if env_vars:
                self.menu.console.print(f"  Env Vars: {len(env_vars)} variable(s)")
                for key, value in env_vars.items():
                    self.menu.console.print(f"    [dim]{key}={value}[/dim]")
            self.menu.console.print()
            
            if Confirm.ask("[yellow]Add this project?[/yellow]", default=True):
                self._add_item_to_current_path(new_project)
                self.config_manager.save(self.config)
                self.menu.console.print("[green]Project added successfully![/green]")
                time.sleep(1)
                return True
            else:
                self.menu.console.print("[yellow]Cancelled[/yellow]")
                time.sleep(1)
                return False
                
        except KeyboardInterrupt:
            self.menu.console.print("\n[yellow]Cancelled[/yellow]")
            time.sleep(1)
            return False
        except Exception as e:
            self.menu.console.print(f"\n[red]Error: {e}[/red]")
            time.sleep(2)
            return False
    
    def _delete_item(self, item: ProjectNode) -> bool:
        """Delete project or folder. Returns True if deleted successfully."""
        from rich.prompt import Prompt
        from ai_cli.core.projects import ProjectManager
        
        self.menu.clear()
        self.menu.console.print("\n[red]Delete Confirmation[/red]")
        self.menu.console.print("=" * 60, style="dim")
        self.menu.console.print()
        
        icon = "📁" if item.type == "folder" else "📄"
        self.menu.console.print(f"[yellow]Item to delete: {icon} {item.name}[/yellow]")
        
        if item.type == "folder":
            count = ProjectManager.count_children_recursive(item)
            self.menu.console.print(f"[yellow]Contains: {count} item(s)[/yellow]")
        else:
            self.menu.console.print(f"[dim]Path: {item.path}[/dim]")
        
        self.menu.console.print()
        self.menu.console.print("[red]⚠️  WARNING: This action cannot be undone![/red]")
        self.menu.console.print()
        
        try:
            confirmation = Prompt.ask(f"[cyan]Type the name to confirm deletion[/cyan]")
            
            if confirmation == item.name:
                self._remove_item_from_current_path(item.name)
                self.config_manager.save(self.config)
                self.menu.console.print("[green]Deleted successfully![/green]")
                time.sleep(1)
                return True
            else:
                self.menu.console.print("[yellow]Name mismatch. Deletion cancelled.[/yellow]")
                time.sleep(1)
                return False
        except KeyboardInterrupt:
            self.menu.console.print("\n[yellow]Cancelled[/yellow]")
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
