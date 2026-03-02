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
        
    def render_tree(self, items: List[Dict[str, Any]], selected: int = 0, max_display: int = 15) -> None:
        """Render project tree structure with scrolling."""
        self.console.print("\n[bold cyan]=== Select Project ===[/bold cyan]\n")
        
        if not items:
            self.console.print("[dim]No projects yet. Press [N] to add your first project.[/dim]\n")
            self.console.print("[dim][N] New Project  [Q] Quit[/dim]")
            return
        
        # Calculate scroll window
        total = len(items)
        if total <= max_display:
            visible_items = items
            offset = 0
        else:
            offset = max(0, min(selected - max_display // 2, total - max_display))
            visible_items = items[offset:offset + max_display]
        
        # Show scroll indicator (top)
        if offset > 0:
            self.console.print(f"[dim]  ↑ {offset} more above[/dim]")
        
        # Show visible items
        for i, item in enumerate(visible_items):
            actual_index = offset + i
            style = Theme.HIGHLIGHT if actual_index == selected else Theme.SECONDARY
            icon = Theme.FOLDER if item.get("type") == "folder" else Theme.FILE
            prefix = "> " if actual_index == selected else "  "
            self.console.print(f"{prefix}{icon} {item['name']}", style=style)
        
        # Show scroll indicator (bottom)
        if offset + max_display < total:
            remaining = total - offset - max_display
            self.console.print(f"[dim]  ↓ {remaining} more below[/dim]")
        
        self.console.print("\n[dim][↑↓] Select  [Enter] Enter/Confirm  [N] New  [D] Delete  [Esc] Back  [Q] Quit[/dim]")
        
    def render_tools(self, tools: List[Dict[str, Any]], selected: int = 0, show_new_tab: bool = True, project_info: Dict[str, Any] = None, max_display: int = 15) -> None:
        """Render tools list with project information and scrolling."""
        
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
        
        # Calculate scroll window
        total = len(tools)
        if total <= max_display:
            visible_tools = tools
            offset = 0
        else:
            offset = max(0, min(selected - max_display // 2, total - max_display))
            visible_tools = tools[offset:offset + max_display]
        
        # Show scroll indicator (top)
        if offset > 0:
            self.console.print(f"[dim]  ↑ {offset} more above[/dim]")
        
        # Show visible tools
        for i, tool in enumerate(visible_tools):
            actual_index = offset + i
            style = Theme.HIGHLIGHT if actual_index == selected else Theme.SECONDARY
            env_label = f"[{tool.get('env', 'Win')}]"
            prefix = "> " if actual_index == selected else "  "
            self.console.print(f"{prefix}{env_label} {tool['name']}", style=style)
        
        # Show scroll indicator (bottom)
        if offset + max_display < total:
            remaining = total - offset - max_display
            self.console.print(f"[dim]  ↓ {remaining} more below[/dim]")
        
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
