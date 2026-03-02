"""Theme configuration for AI-CLI."""
from rich.style import Style
from typing import Dict

class Theme:
    """Color schemes and icons."""
    
    # Colors
    PRIMARY = Style(color="cyan")
    SECONDARY = Style(color="blue")
    SUCCESS = Style(color="green")
    ERROR = Style(color="red")
    WARNING = Style(color="yellow")
    MUTED = Style(color="bright_black")
    HIGHLIGHT = Style(color="white", bgcolor="blue")
    
    # Icons
    FOLDER = "📁"
    FILE = "📄"
    SUCCESS_ICON = "✅"
    ERROR_ICON = "❌"
    ARROW = "→"
    
    @classmethod
    def dark_theme(cls) -> Dict[str, Style]:
        """Dark theme variant."""
        return {
            "primary": Style(color="bright_cyan"),
            "secondary": Style(color="bright_blue"),
            "success": Style(color="bright_green"),
            "error": Style(color="bright_red"),
            "warning": Style(color="bright_yellow"),
            "muted": Style(color="gray50"),
            "highlight": Style(color="black", bgcolor="bright_cyan")
        }
