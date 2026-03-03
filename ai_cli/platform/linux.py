"""Linux platform adapter."""
import shutil
import subprocess
import sys
from typing import Optional
from ai_cli.models import Tool, ProjectNode
from .base import PlatformAdapter


class LinuxPlatformAdapter(PlatformAdapter):
    """Linux platform adapter."""
    
    def launch_terminal(self, tool: Tool, project: ProjectNode, new_tab: bool = False) -> None:
        """Launch terminal with tool and project."""
        terminal = self._detect_terminal()
        if not terminal:
            raise RuntimeError("No terminal emulator found")
        
        command = self.get_shell_command(tool, project)
        
        if "gnome-terminal" in terminal:
            subprocess.Popen([terminal, "--", "bash", "-c", command])
        elif "konsole" in terminal:
            subprocess.Popen([terminal, "-e", "bash", "-c", command])
        else:  # xterm, x-terminal-emulator
            subprocess.Popen([terminal, "-e", "bash", "-c", command])
    
    def get_shell_command(self, tool: Tool, project: ProjectNode) -> str:
        """Generate shell command."""
        title = f"{tool.name} - {project.name}"
        parts = [f"cd {project.path}"]
        
        if project.env:
            for key, value in project.env.items():
                parts.append(f"export {key}='{value}'")
        
        parts.append(f"echo -ne '\\033]0;{title}\\007'")
        parts.append(tool.name)
        
        return " && ".join(parts)
    
    def set_terminal_title(self, title: str) -> None:
        """Set terminal title."""
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
    
    def _detect_terminal(self) -> Optional[str]:
        """Detect available terminal emulator."""
        terminals = ["gnome-terminal", "konsole", "xterm", "x-terminal-emulator"]
        for terminal in terminals:
            path = shutil.which(terminal)
            if path:
                return path
        return None
