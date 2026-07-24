"""Menu rendering with rich console."""
from rich.console import Console, Group
from rich.tree import Tree
from rich.text import Text
from typing import List, Dict, Any
from .theme import Theme
from ai_cli.i18n import get_text

class MenuRenderer:
    """Renders menus and navigation."""
    
    def __init__(self):
        self.console = Console()
    
    @staticmethod
    def _build_update_banner(update_info) -> str:
        """Build update notification string if update is available."""
        if not update_info:
            return ""
        checked = getattr(update_info, 'checked', False)
        if not checked:
            return ""
        if getattr(update_info, 'is_update_available', False):
            latest = getattr(update_info, 'latest_version', '')
            return get_text('update_available', new=latest)
        return ""

    def build_tree_display(self, items: List[Dict[str, Any]], selected: int = 0, max_display: int = 15, breadcrumb: List[str] = None, update_info=None) -> Group:
        """Build project tree display for Live rendering."""
        lines = []
        
        # Update notification banner
        banner = self._build_update_banner(update_info)
        if banner:
            lines.append(Text(f"  {banner}", style="bold yellow"))
        
        # Breadcrumb
        if breadcrumb:
            bc = Text("  ")
            for i, item in enumerate(breadcrumb):
                if i > 0:
                    bc.append(f" {Theme.ARROW} ", style=Theme.MUTED)
                bc.append(item, style=Theme.PRIMARY)
            lines.append(bc)
            lines.append(Text())  # Empty line
        
        lines.append(Text(f"  {get_text('select_project')}"))
        lines.append(Text("  " + "=" * 60, style="dim"))
        lines.append(Text())  # Empty line
        
        if not items:
            lines.append(Text("  (Empty folder)", style="dim"))
            lines.append(Text())  # Empty line
            
            # Show appropriate menu based on location
            if breadcrumb and len(breadcrumb) > 1:
                lines.append(Text(f"  [N] {get_text('new')}  [Esc] {get_text('back')}  [Q] {get_text('quit')}", style="dim"))
            else:
                lines.append(Text(f"  [N] {get_text('new')}  [Q] {get_text('quit')}", style="dim"))
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
            lines.append(Text(f"  {get_text('more_above', offset)}", style="dim"))
        
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
            lines.append(Text(f"  {get_text('more_below', remaining)}", style="dim"))
        
        lines.append(Text())  # Empty line
        
        # Show menu hint
        hint = f"  [↑↓] {get_text('navigate')}  [Enter] {get_text('select')}  [N] {get_text('new')}  [D] {get_text('delete')}"
        if breadcrumb and len(breadcrumb) > 1:  # Show Back only when not at root
            hint += f"  [Esc] {get_text('back')}"
        if update_info and getattr(update_info, 'is_update_available', False):
            hint += f"  [U] {get_text('upgrade')}"
        hint += f"  [Q] {get_text('quit')}"
        lines.append(Text(hint, style="dim"))
        
        return Group(*lines)
    
    def build_tools_display(self, tools: List[Dict[str, Any]], selected: int = 0, show_new_tab: bool = True,
                            project_info: Dict[str, Any] = None, max_display: int = 15, update_info=None,
                            usage_counts: Dict = None, sort_mode: str = "usage", sort_descending: bool = True) -> Group:
        """Build tools list display for Live rendering."""
        lines = []
        
        # Update notification banner
        banner = self._build_update_banner(update_info)
        if banner:
            lines.append(Text(f"  {banner}", style="bold yellow"))
        
        # Show project information
        if project_info:
            lines.append(Text(f"\n{get_text('project_label', project_info.get('name', 'Unknown'))}", style="bold cyan"))
            if project_info.get('path'):
                lines.append(Text(f"{get_text('path_label', project_info['path'])}", style="dim"))
            if project_info.get('branch'):
                lines.append(Text(f"{get_text('branch_label', project_info['branch'])}", style="dim"))
            if project_info.get('env'):
                env_str = ', '.join([f"{k}={v}" for k, v in project_info['env'].items()])
                lines.append(Text(f"{get_text('env_label', env_str)}", style="dim"))
        
        lines.append(Text(f"\n=== {get_text('select_tool')} ===\n", style="bold cyan"))
        # Sort indicator
        if sort_mode == "usage":
            sort_key = 'sort_usage_desc' if sort_descending else 'sort_usage_asc'
        else:
            sort_key = 'sort_name_desc' if sort_descending else 'sort_name_asc'
        lines.append(Text(f"  {get_text(sort_key)}  [{get_text('sort_hint')}]", style="dim"))
        lines.append(Text())
        
        if usage_counts is None:
            usage_counts = {}

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
            lines.append(Text(f"  {get_text('more_above', offset)}", style="dim"))
        
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
            lines.append(Text(f"  {get_text('more_below', remaining)}", style="dim"))
        
        has_update = update_info and getattr(update_info, 'is_update_available', False)
        update_hint = f"  [U] {get_text('upgrade')}" if has_update else ""
        # Show [T] New Tab only if Windows Terminal is available
        if show_new_tab:
            lines.append(Text(f"\n[↑↓] {get_text('select')}  [Enter] {get_text('launch')}  [T] {get_text('launch_new_tab')}  [I] {get_text('install')}  [R] {get_text('refresh')}  [S] {get_text('sort_hint')}{update_hint}  [Esc] {get_text('back')}  [Q] {get_text('quit')}", style="dim"))
        else:
            lines.append(Text(f"\n[↑↓] {get_text('select')}  [Enter] {get_text('launch')}  [I] {get_text('install')}  [R] {get_text('refresh')}  [S] {get_text('sort_hint')}{update_hint}  [Esc] {get_text('back')}  [Q] {get_text('quit')}", style="dim"))
        
        return Group(*lines)
        
    def clear(self) -> None:
        """Clear console."""
        self.console.clear()