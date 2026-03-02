"""Main application logic."""
import asyncio
import subprocess
import sys
from typing import Optional, List
from ai_cli.config import ConfigManager
from ai_cli.models import Config, ProjectNode, Tool
from ai_cli.ui.menu import MenuRenderer
from ai_cli.ui.input import InputHandler, InputEvent
from ai_cli.platform.factory import get_platform_adapter
from ai_cli.core.tools import ToolDetector


class Application:
    """Main application class."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        self.menu = MenuRenderer()
        self.input_handler = InputHandler()
        self.platform_adapter = get_platform_adapter()
        self.tool_detector = ToolDetector()  # Single instance with cache
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
    
    def _select_project(self) -> Optional[ProjectNode]:
        """Project selection menu. Returns None only on Q (quit)."""
        while True:
            try:
                current_node = self._get_current_node()
                
                self.menu.clear()
                self.menu.render_breadcrumb(["Home"] + self.current_path)
                
                items = current_node.children if current_node else self.config.projects
                
                # Handle empty project list
                if not items:
                    self.menu.console.print("\n[yellow]No projects configured. Press 'N' to add a project or 'Q' to quit.[/yellow]")
                    event = self.input_handler.get_input()
                    if event == InputEvent.NEW:
                        # TODO: Add project creation
                        self.menu.console.print("\n[red]Project creation not yet implemented[/red]")
                        import time
                        time.sleep(1)
                    elif event == InputEvent.QUIT:
                        return None
                    continue
                
                self.menu.render_tree([{"name": item.name, "type": item.type} for item in items], self.selected_index)
                
                event = self.input_handler.get_input()
                
                if event == InputEvent.UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif event == InputEvent.DOWN:
                    self.selected_index = min(len(items) - 1, self.selected_index + 1)
                elif event == InputEvent.ENTER:
                    selected = items[self.selected_index]
                    if selected.type == "folder":
                        self.current_path.append(selected.name)
                        self.selected_index = 0
                    else:
                        return selected
                elif event == InputEvent.NEW:
                    # TODO: Add project/folder creation
                    self.menu.console.print("\n[red]Project creation not yet implemented[/red]")
                    import time
                    time.sleep(1)
                elif event == InputEvent.DELETE:
                    # TODO: Add delete confirmation
                    self.menu.console.print("\n[red]Delete function not yet implemented[/red]")
                    import time
                    time.sleep(1)
                elif event == InputEvent.ESCAPE:
                    # ESC only goes back, never quits
                    if self.current_path:
                        self.current_path.pop()
                        self.selected_index = 0
                    # If at root, do nothing (stay in menu)
                elif event == InputEvent.QUIT:
                    # Q always quits
                    return None
            except Exception as e:
                self.menu.console.print(f"\n[red]Error: {e}[/red]")
                import time
                time.sleep(1)
    
    async def _select_tool(self, project: ProjectNode) -> Optional[tuple]:
        """Tool selection menu. Returns (tool, new_tab) or None."""
        # Detect tools with progress indicator (uses cache if available)
        self.menu.console.print("[yellow]Detecting tools...[/yellow]")
        tools = await self.tool_detector.detect_all_tools(self.config.tools)
        
        if not tools:
            self.menu.console.print("\n[red]No AI tools detected. Press 'I' to install tools or 'Q' to quit.[/red]")
            import time
            time.sleep(2)
            return None
        
        self.selected_index = 0
        
        while True:
            self.menu.clear()
            self.menu.render_tools([{"name": t.get_display_label(), "env": t.environment.value} for t in tools], 
                                  self.selected_index, 
                                  show_new_tab=self.wt_available)
            
            event = self.input_handler.get_input()
            
            if event == InputEvent.UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event == InputEvent.DOWN:
                self.selected_index = min(len(tools) - 1, self.selected_index + 1)
            elif event == InputEvent.ENTER:
                return (tools[self.selected_index], False)
            elif event == InputEvent.NEW_TAB:
                if self.wt_available:
                    return (tools[self.selected_index], True)
                # Ignore T key if wt not available
            elif event == InputEvent.ESCAPE:
                # ESC returns to project selection
                return None
            elif event == InputEvent.QUIT:
                # Q quits the program - raise exception to exit main loop
                raise KeyboardInterrupt
            elif event == InputEvent.RUN:
                self.menu.console.print("\n[yellow]Refreshing tools...[/yellow]")
                self.tool_detector.clear_cache()
                tools = await self.tool_detector.detect_all_tools(self.config.tools)
                if not tools:
                    self.menu.console.print("\n[red]No tools detected.[/red]")
                    import time
                    time.sleep(1)
                    return None
    
    def _launch_tool(self, tool: Tool, project: ProjectNode, new_tab: bool = False) -> None:
        """Launch tool in terminal."""
        try:
            self.platform_adapter.launch_terminal(tool, project, new_tab=new_tab, wt_available=self.wt_available)
            tab_mode = "new tab" if new_tab else "new window"
            print(f"Launched {tool.name} for {project.name} in {tab_mode}")
        except Exception as e:
            print(f"Failed to launch tool: {e}")
    
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
