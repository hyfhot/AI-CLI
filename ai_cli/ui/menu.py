"""Menu rendering with rich console."""
from rich.console import Console
from rich.tree import Tree
from rich.text import Text
from typing import List, Dict, Any
from .theme import Theme

class MenuRenderer:
    """Renders menus and navigation."""
    
    def __init__(self):
        self.console = Console()
        
    def render_tree(self, items: List[Dict[str, Any]], selected: int = 0) -> None:
        """Render project tree structure."""
        self.console.print("\n[bold cyan]=== Select Project ===[/bold cyan]\n")
        
        for i, item in enumerate(items):
            style = Theme.HIGHLIGHT if i == selected else Theme.SECONDARY
            icon = Theme.FOLDER if item.get("type") == "folder" else Theme.FILE
            prefix = "> " if i == selected else "  "
            self.console.print(f"{prefix}{icon} {item['name']}", style=style)
        
        self.console.print("\n[dim][↑↓] Select  [Enter] Enter/Confirm  [N] New  [D] Delete  [Esc] Back  [Q] Quit[/dim]")
        
    def render_tools(self, tools: List[Dict[str, Any]], selected: int = 0, show_new_tab: bool = True, project_info: Dict[str, Any] = None) -> None:
        """Render tools list with project information."""
        
        # Show project information
        if project_info:
            self.console.print(f"\n[bold cyan]Project:[/bold cyan] {project_info.get('name', 'Unknown')}")
            if project_info.get('path'):
                self.console.print(f"[dim]Path: {project_info['path']}[/dim]")
            if project_info.get('branch'):
                self.console.print(f"[dim]Branch: {project_info['branch']}[/dim]")
            if project_info.get('env'):
                env_str = ', '.join([f"{k}={v}" for k, v in project_info['env'].items()])
                self.console.print(f"[dim]Env: {env_str}[/dim]")
        
        self.console.print("\n[bold cyan]=== Select AI Tool ===[/bold cyan]\n")
        
        for i, tool in enumerate(tools):
            style = Theme.HIGHLIGHT if i == selected else Theme.SECONDARY
            env_label = f"[{tool.get('env', 'Win')}]"
            prefix = "> " if i == selected else "  "
            
            # Show tool name only
            self.console.print(f"{prefix}{env_label} {tool['name']}", style=style)
        
        # Show [T] New Tab only if Windows Terminal is available
        if show_new_tab:
            self.console.print("\n[dim][↑↓] Select  [Enter] Launch  [T] New Tab  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit[/dim]")
        else:
            self.console.print("\n[dim][↑↓] Select  [Enter] Launch  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit[/dim]")
            
    def render_breadcrumb(self, path: List[str]) -> None:
        """Render navigation breadcrumb."""
        if not path:
            return
            
        breadcrumb = Text()
        for i, item in enumerate(path):
            if i > 0:
                breadcrumb.append(f" {Theme.ARROW} ", style=Theme.MUTED)
            breadcrumb.append(item, style=Theme.PRIMARY)
            
        self.console.print(breadcrumb)
        
    def clear(self) -> None:
        """Clear console."""
        self.console.clear()
