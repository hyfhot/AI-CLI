"""Windows platform adapter."""
import subprocess
import sys
from typing import Optional
from ai_cli.models import Tool, ProjectNode, ToolEnvironment
from ai_cli.utils import PathConverter
from .base import PlatformAdapter


class WindowsPlatformAdapter(PlatformAdapter):
    """Windows platform adapter with WSL support."""
    
    def launch_terminal(self, tool: Tool, project: ProjectNode, new_tab: bool = False, wt_available: bool = False) -> None:
        """Launch terminal with tool and project."""
        title = f"{tool.name} - {project.name}"
        
        if tool.environment == ToolEnvironment.WSL:
            wsl_path = PathConverter.to_wsl_path(project.path)
            env_vars = []
            
            if project.env:
                for key, value in project.env.items():
                    if ':\\' in value or ':\\\\' in value:
                        value = PathConverter.to_wsl_path(value)
                    env_vars.append(f"export {key}='{value}'")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            wsl_command = f"cd '{wsl_path}'; {env_prefix}{tool.name}; exec bash"
            
            # Launch WSL
            if new_tab and wt_available:
                # Windows Terminal new tab
                cmd = ["wt", "-w", "0", "new-tab", "--title", title, "wsl", "-e", "bash", "-ic", wsl_command]
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
            title_cmd = f"title {title}"
            command = f"{env_prefix}cd /d {project.path} && {title_cmd} && {tool.name}"
            
            if new_tab and wt_available:
                cmd = ["wt", "-w", "0", "new-tab", "--title", title, "cmd.exe", "/k", command]
                subprocess.Popen(cmd)
            else:
                cmd = ["cmd.exe", "/k", command]
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    def get_shell_command(self, tool: Tool, project: ProjectNode) -> str:
        """Generate shell command."""
        title = f"{tool.name} - {project.name}"
        
        if tool.environment == ToolEnvironment.WSL:
            wsl_path = PathConverter.to_wsl_path(project.path)
            env_vars = []
            
            if project.env:
                for key, value in project.env.items():
                    # Convert Windows paths in env vars to WSL paths
                    if ':\\' in value or ':\\\\' in value:
                        value = PathConverter.to_wsl_path(value)
                    env_vars.append(f"export {key}='{value}'")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            title_cmd = f"echo -ne '\\033]0;{title}\\007'"
            return f"{env_prefix}cd {wsl_path} && {title_cmd} && {tool.name}"
        else:
            env_vars = []
            if project.env:
                for key, value in project.env.items():
                    env_vars.append(f"set {key}={value}")
            
            env_prefix = " && ".join(env_vars) + " && " if env_vars else ""
            title_cmd = f"title {title}"
            return f"{env_prefix}cd /d {project.path} && {title_cmd} && {tool.name}"
    
    def set_terminal_title(self, title: str) -> None:
        """Set terminal title."""
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
