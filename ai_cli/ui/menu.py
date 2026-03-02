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
            bc = Text("  ")
            for i, item in enumerate(breadcrumb):
                if i > 0:
                    bc.append(f" {Theme.ARROW} ", style=Theme.MUTED)
                bc.append(item, style=Theme.PRIMARY)
            lines.append(bc)
            lines.append(Text())  # Empty line
        
        lines.append(Text("  Select Project"))
        lines.append(Text("  " + "=" * 60, style="dim"))
        lines.append(Text())  # Empty line
        
        if not items:
            lines.append(Text("  (Empty folder)", style="dim"))
            lines.append(Text())  # Empty line
            
            # Show appropriate menu based on location
            if breadcrumb and len(breadcrumb) > 1:
                lines.append(Text("  [N] New  [Esc] Back  [Q] Quit", style="dim"))
            else:
                lines.append(Text("  [N] New  [Q] Quit", style="dim"))
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
            
            # Ensure item is a dict
            if not isinstance(item, dict):
                continue
            
            icon = Theme.FOLDER if item.get("type") == "folder" else Theme.FILE
            prefix = "> " if actual_index == selected else "  "
            
            # Build item line
            line = Text()
            line.append(f"{prefix}{icon} {item.get('name', 'Unknown')}", style=style)
            
            # Add path or children count in gray
            if item.get("type") == "folder":
                # Show children count for folders
                children_count = item.get("children_count", 0)
                line.append(f" ({children_count} item(s))", style="dim")
            elif item.get("path"):
                # Show path for projects
                line.append(f" ({item.get('path')})", style="dim")
            
            lines.append(line)
        
        # Show scroll indicator (bottom)
        if offset + max_display < total:
            remaining = total - offset - max_display
            lines.append(Text(f"  ↓ {remaining} more below", style="dim"))
        
        lines.append(Text())  # Empty line
        
        # Show menu hint
        hint = "  [↑↓] Navigate  [Enter] Select  [N] New  [D] Delete"
        if breadcrumb and len(breadcrumb) > 1:  # Show Back only when not at root
            hint += "  [Esc] Back"
        hint += "  [Q] Quit"
        lines.append(Text(hint, style="dim"))
        
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
            prefix = "> " if actual_index == selected else "  "
            
            # Only show env label on Windows (to distinguish Win/Wsl)
            import sys
            if sys.platform == 'win32':
                env = tool.get('env', 'windows')
                env_label = f"[{'Wsl' if env == 'wsl' else 'Win'}] "
            else:
                env_label = ""
            
            lines.append(Text(f"{prefix}{env_label}{tool['name']}", style=style))
        
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
