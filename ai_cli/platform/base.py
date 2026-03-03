"""Platform adapter abstract base class."""
from abc import ABC, abstractmethod
from typing import Optional

class PlatformAdapter(ABC):
    """Abstract base class for platform-specific terminal operations."""
    
    @abstractmethod
    def launch_terminal(self, tool: str, project: str, new_tab: bool = False) -> None:
        """Launch terminal with specified tool and project."""
        pass
    
    @abstractmethod
    def get_shell_command(self, tool: str, project: str) -> str:
        """Generate shell command for tool and project."""
        pass
    
    @abstractmethod
    def set_terminal_title(self, title: str) -> None:
        """Set terminal window title."""
        pass
