"""Menu rendering with rich console."""
from rich.console import Console, Group
from rich.tree import Tree
from rich.text import Text
from typing import List, Dict, Any
from .theme import Theme

class MenuRenderer:
    """Renders menus and navigation."""
    
    def __init__(self):
        self.console = Console()
    
    def build_tree_display(self, items: List[Dict[str, Any]], selected: int = 0, max_display: int = 15, breadcrumb: List[str] = None) -> Group:
        """Build project tree display for Live rendering."""
        lines = []
        
        # Breadcrumb
        if breadcrumb:
            bc = Text()
            for i, item in enumerate(breadcrumb):
                if i > 0:
                    bc.append(f" {Theme.ARROW} ", style=Theme.MUTED)
                bc.append(item, style=Theme.PRIMARY)
            lines.append(bc)
        
        lines.append(Text("\n=== Select Project ===\n", style="bold cyan"))
        
        if not items:
            lines.append(Text("No projects yet. Press [N] to add your first project.\n", style="dim"))
            lines.append(Text("[N] New Project  [Q] Quit", style="dim"))
            return Group(*lines)
        
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
            lines.append(Text(f"  ↑ {offset} more above", style="dim"))
        
        # Show visible items
        for i, item in enumerate(visible_items):
            actual_index = offset + i
            style = Theme.HIGHLIGHT if actual_index == selected else Theme.SECONDARY
            icon = Theme.FOLDER if item.get("type") == "folder" else Theme.FILE
            prefix = "> " if actual_index == selected else "  "
            lines.append(Text(f"{prefix}{icon} {item['name']}", style=style))
        
        # Show scroll indicator (bottom)
        if offset + max_display < total:
            remaining = total - offset - max_display
            lines.append(Text(f"  ↓ {remaining} more below", style="dim"))
        
        lines.append(Text("\n[↑↓] Select  [Enter] Enter/Confirm  [N] New  [D] Delete  [Esc] Back  [Q] Quit", style="dim"))
        return Group(*lines)
    
    def build_tools_display(self, tools: List[Dict[str, Any]], selected: int = 0, show_new_tab: bool = True, project_info: Dict[str, Any] = None, max_display: int = 15) -> Group:
        """Build tools list display for Live rendering."""
        lines = []
        
        # Show project information
        if project_info:
            lines.append(Text(f"\nProject: {project_info.get('name', 'Unknown')}", style="bold cyan"))
            if project_info.get('path'):
                lines.append(Text(f"Path: {project_info['path']}", style="dim"))
            if project_info.get('branch'):
                lines.append(Text(f"Branch: {project_info['branch']}", style="dim"))
            if project_info.get('env'):
                env_str = ', '.join([f"{k}={v}" for k, v in project_info['env'].items()])
                lines.append(Text(f"Env: {env_str}", style="dim"))
        
        lines.append(Text("\n=== Select AI Tool ===\n", style="bold cyan"))
        
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
            lines.append(Text(f"  ↑ {offset} more above", style="dim"))
        
        # Show visible tools
        for i, tool in enumerate(visible_tools):
            actual_index = offset + i
            style = Theme.HIGHLIGHT if actual_index == selected else Theme.SECONDARY
            env_label = f"[{tool.get('env', 'Win')}]"
            prefix = "> " if actual_index == selected else "  "
            lines.append(Text(f"{prefix}{env_label} {tool['name']}", style=style))
        
        # Show scroll indicator (bottom)
        if offset + max_display < total:
            remaining = total - offset - max_display
            lines.append(Text(f"  ↓ {remaining} more below", style="dim"))
        
        # Show [T] New Tab only if Windows Terminal is available
        if show_new_tab:
            lines.append(Text("\n[↑↓] Select  [Enter] Launch  [T] New Tab  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit", style="dim"))
        else:
            lines.append(Text("\n[↑↓] Select  [Enter] Launch  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit", style="dim"))
        
        return Group(*lines)
        
    def clear(self) -> None:
        """Clear console."""
        self.console.clear()
