"""Windows platform adapter."""
import re
import shlex
import subprocess
import sys
from typing import Optional
from ai_cli.models import Tool, ProjectNode, ToolEnvironment
from ai_cli.utils import PathConverter
from .base import PlatformAdapter


def _sanitize_cmd_title(title: str) -> str:
    """Sanitize a string for use in cmd.exe 'title' command.
    
    Removes characters that cmd.exe interprets as metacharacters.
    """
    # Remove cmd metacharacters: & | > < ^ % ( )
    return re.sub(r'[&|><^%()"]', '', title)


def _quote_cmd_path(path: str) -> str:
    """Quote a path for use in cmd.exe commands."""
    return f'"{path}"'


class WindowsPlatformAdapter(PlatformAdapter):
    """Windows platform adapter with WSL support."""
    
    def launch_terminal(self, tool: Tool, project: ProjectNode, new_tab: bool = False, wt_available: bool = False) -> None:
        """Launch terminal with tool and project."""
        safe_title = _sanitize_cmd_title(f"{tool.name} - {project.name}")
        
        if tool.environment == ToolEnvironment.WSL:
            wsl_path = PathConverter.to_wsl_path(project.path)
            env_vars = []
            
            if project.env:
                for key, value in project.env.items():
                    if ':\\' in value or ':\\\\' in value:
                        value = PathConverter.to_wsl_path(value)
                    env_vars.append(f"export {key}={shlex.quote(value)}")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            wsl_command = f"cd {shlex.quote(wsl_path)}; {env_prefix}{tool.name}; exec bash"
            
            # Launch WSL
            if new_tab and wt_available:
                # Windows Terminal new tab
                cmd = ["wt", "-w", "0", "new-tab", "--title", safe_title, "wsl", "-e", "bash", "-ic", wsl_command]
                subprocess.Popen(cmd)
            else:
                # New window with wsl.exe
                cmd = ["wsl.exe", "-e", "bash", "-ic", wsl_command]
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            env_vars = []
            if project.env:
                for key, value in project.env.items():
                    env_vars.append(f"set {key}={value}")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            title_cmd = f"title {safe_title}"
            command = f"{env_prefix}cd /d {_quote_cmd_path(project.path)} && {title_cmd} && {tool.name}"
            
            if new_tab and wt_available:
                cmd = ["wt", "-w", "0", "new-tab", "--title", safe_title, "cmd.exe", "/k", command]
                subprocess.Popen(cmd)
            else:
                cmd = ["cmd.exe", "/k", command]
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    def get_shell_command(self, tool: Tool, project: ProjectNode) -> str:
        """Generate shell command."""
        safe_title = _sanitize_cmd_title(f"{tool.name} - {project.name}")
        
        if tool.environment == ToolEnvironment.WSL:
            wsl_path = PathConverter.to_wsl_path(project.path)
            env_vars = []
            
            if project.env:
                for key, value in project.env.items():
                    # Convert Windows paths in env vars to WSL paths
                    if ':\\' in value or ':\\\\' in value:
                        value = PathConverter.to_wsl_path(value)
                    env_vars.append(f"export {key}={shlex.quote(value)}")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            title_cmd = f"echo -ne '\\033]0;{safe_title}\\007'"
            return f"{env_prefix}cd {shlex.quote(wsl_path)} && {title_cmd} && {tool.name}"
        else:
            env_vars = []
            if project.env:
                for key, value in project.env.items():
                    env_vars.append(f"set {key}={value}")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            title_cmd = f"title {safe_title}"
            return f"{env_prefix}cd /d {_quote_cmd_path(project.path)} && {title_cmd} && {tool.name}"
    
    def set_terminal_title(self, title: str) -> None:
        """Set terminal title."""
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
