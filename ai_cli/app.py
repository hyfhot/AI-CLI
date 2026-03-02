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
                
                tool, new_tab = result
                self._launch_tool(tool, project, new_tab)
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
        
        self.menu.clear()
        
        while True:
            current_node = self._get_current_node()
            items = current_node.children if current_node else self.config.projects
            
            # Handle empty project list
            if not items:
                self.menu.console.print("\n[yellow]No projects configured. Press 'N' to add a project or 'Q' to quit.[/yellow]")
                event = self.input_handler.get_input()
                if event == InputEvent.NEW:
                    self.menu.console.print("\n[red]Project creation not yet implemented[/red]")
                    import time
                    time.sleep(1)
                elif event == InputEvent.QUIT:
                    return None
                continue
            
            breadcrumb = ["Home"] + self.current_path
            display = self.menu.build_tree_display(
                [{"name": item.name, "type": item.type} for item in items],
                self.selected_index,
                breadcrumb=breadcrumb
            )
            
            with Live(display, console=self.menu.console, refresh_per_second=10) as live:
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
                            break  # Exit Live context to refresh
                        else:
                            return selected
                    elif event == InputEvent.NEW:
                        self.menu.console.print("\n[red]Project creation not yet implemented[/red]")
                        import time
                        time.sleep(1)
                        break
                    elif event == InputEvent.DELETE:
                        self.menu.console.print("\n[red]Delete function not yet implemented[/red]")
                        import time
                        time.sleep(1)
                        break
                    elif event == InputEvent.ESCAPE:
                        if self.current_path:
                            self.current_path.pop()
                            self.selected_index = 0
                            break
                    elif event == InputEvent.QUIT:
                        return None
    
    async def _select_tool(self, project: ProjectNode) -> Optional[Tuple]:
        """Tool selection menu. Returns (tool, new_tab) or None."""
        from rich.live import Live
        
        # Check for git worktrees and let user select if multiple exist
        if project.path:
            try:
                from ai_cli.core.git import GitManager
                git_manager = GitManager()
                worktrees = git_manager.detect_worktrees(project.path)
                
                if len(worktrees) > 1:
                    selected_path = git_manager.select_worktree(worktrees, project.path)
                    if selected_path:
                        project.path = selected_path
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
        
        # Prepare project info
        project_info = {
            'name': project.name,
            'path': project.path,
            'env': project.env if project.env else None
        }
        
        # Detect git branch if path exists
        if project.path:
            try:
                from ai_cli.core.git import GitDetector
                git_detector = GitDetector()
                branch = git_detector.get_current_branch(project.path)
                if branch:
                    project_info['branch'] = branch
            except:
                pass
        
        # Show tool list
        tool_items = []
        for t in tools:
            tool_items.append({
                "name": t.get_display_label(),
                "env": t.environment.value
            })
        
        self.menu.clear()
        display = self.menu.build_tools_display(
            tool_items,
            self.selected_index,
            show_new_tab=self.wt_available,
            project_info=project_info
        )
        
        with Live(display, console=self.menu.console, refresh_per_second=10) as live:
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
                    return (tools[self.selected_index], False)
                elif event == InputEvent.NEW_TAB:
                    if self.wt_available:
                        return (tools[self.selected_index], True)
                elif event == InputEvent.INSTALL:
                    await self._install_tool_menu()
                    self.tool_detector.clear_cache()
                    tools = await self.tool_detector.detect_all_tools(self.config.tools)
                    if not tools:
                        return None
                    # Rebuild tool items
                    tool_items = [{"name": t.get_display_label(), "env": t.environment.value} for t in tools]
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
                        return None
                    tool_items = [{"name": t.get_display_label(), "env": t.environment.value} for t in tools]
                    live.update(self.menu.build_tools_display(
                        tool_items, self.selected_index,
                        show_new_tab=self.wt_available, project_info=project_info
                    ))
                elif event == InputEvent.ESCAPE:
                    return None
                elif event == InputEvent.QUIT:
                    raise KeyboardInterrupt
    
    def _launch_tool(self, tool: Tool, project: ProjectNode, new_tab: bool = False) -> None:
        """Launch tool in terminal."""
        try:
            self.platform_adapter.launch_terminal(tool, project, new_tab=new_tab, wt_available=self.wt_available)
            tab_mode = "new tab" if new_tab else "new window"
            print(f"Launched {tool.name} for {project.name} in {tab_mode}")
        except Exception as e:
            print(f"Failed to launch tool: {e}")
    
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
