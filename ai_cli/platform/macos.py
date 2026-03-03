"""macOS platform adapter."""
import subprocess
import shlex
import sys
from typing import Optional
from ai_cli.models import Tool, ProjectNode
from .base import PlatformAdapter


class MacOSPlatformAdapter(PlatformAdapter):
    """macOS platform adapter."""
    
    def launch_terminal(self, tool: Tool, project: ProjectNode, new_tab: bool = False) -> None:
        """Launch terminal with tool and project."""
        command = self.get_shell_command(tool, project)
        escaped_cmd = command.replace('"', '\\"')
        
        if self._has_iterm():
            if new_tab:
                script = f'tell app "iTerm" to tell current window to create tab with default profile command "{escaped_cmd}"'
            else:
                script = f'tell app "iTerm" to create window with default profile command "{escaped_cmd}"'
        else:
            if new_tab:
                script = f'tell app "Terminal" to do script "{escaped_cmd}" in window 1'
            else:
                script = f'tell app "Terminal" to do script "{escaped_cmd}"'
        
        subprocess.run(["osascript", "-e", script])
    
    def get_shell_command(self, tool: Tool, project: ProjectNode) -> str:
        """Generate shell command."""
        title = f"{tool.name} - {project.name}"
        parts = [f"cd {shlex.quote(project.path)}"]
        
        if project.env:
            for key, value in project.env.items():
                parts.append(f"export {key}={shlex.quote(value)}")
        
        parts.append(f"echo -ne '\\033]0;{title}\\007'")
        parts.append(tool.name)
        
        return " && ".join(parts)
    
    def set_terminal_title(self, title: str) -> None:
        """Set terminal title."""
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
    
    def _has_iterm(self) -> bool:
        """Check if iTerm2 is installed."""
        try:
            result = subprocess.run(
                ["osascript", "-e", 'tell app "iTerm" to get version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
