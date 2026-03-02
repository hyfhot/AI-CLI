"""Tool installation functionality."""
import subprocess
import sys
import os
from typing import Optional
from ai_cli.models import ToolConfig, ToolEnvironment


class ToolInstaller:
    """Handles tool installation."""
    
    def install_tool(self, tool: ToolConfig, environment: ToolEnvironment) -> bool:
        """Install a tool in the specified environment."""
        install_cmd = self._get_install_command(tool, environment)
        
        if not install_cmd:
            return False
        
        try:
            if environment == ToolEnvironment.WSL:
                # Run in WSL
                result = subprocess.run(
                    ["wsl.exe", "-e", "bash", "-ic", install_cmd],
                    check=False,
                    capture_output=False
                )
            else:
                # Run in Windows/Linux/macOS
                if sys.platform == 'win32':
                    result = subprocess.run(
                        install_cmd,
                        shell=True,
                        check=False
                    )
                else:
                    result = subprocess.run(
                        install_cmd,
                        shell=True,
                        check=False
                    )
            
            if result.returncode == 0:
                self._update_path_after_install(tool.name, environment)
                return True
            
            return False
        except Exception as e:
            print(f"Installation error: {e}")
            return False
    
    def _get_install_command(self, tool: ToolConfig, environment: ToolEnvironment) -> Optional[str]:
        """Get the installation command for a tool."""
        if environment == ToolEnvironment.WSL and tool.wsl_install:
            return tool.wsl_install
        elif environment == ToolEnvironment.WINDOWS and tool.win_install:
            return tool.win_install
        elif environment == ToolEnvironment.LINUX and tool.linux_install:
            return tool.linux_install
        elif environment == ToolEnvironment.MACOS and tool.macos_install:
            return tool.macos_install
        return None
    
    def _update_path_after_install(self, tool_name: str, environment: ToolEnvironment):
        """Update PATH after tool installation (Windows only)."""
        if sys.platform != 'win32' or environment == ToolEnvironment.WSL:
            return
        
        # Try to find the tool executable
        tool_path = self._find_tool_executable(tool_name)
        
        if not tool_path:
            return
        
        tool_dir = os.path.dirname(tool_path)
        
        # Add to user PATH
        self._add_to_user_path(tool_dir)
    
    def _find_tool_executable(self, tool_name: str) -> Optional[str]:
        """Find tool executable path."""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    ["where", tool_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
            else:
                result = subprocess.run(
                    ["which", tool_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return None
    
    def _add_to_user_path(self, directory: str):
        """Add directory to user PATH (Windows only)."""
        if sys.platform != 'win32':
            return
        
        try:
            # Get current user PATH
            result = subprocess.run(
                ["powershell", "-Command", 
                 "[Environment]::GetEnvironmentVariable('Path', 'User')"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return
            
            current_path = result.stdout.strip()
            
            # Check if already in PATH
            if directory.lower() in current_path.lower():
                return
            
            # Add to PATH
            new_path = f"{current_path};{directory}" if current_path else directory
            
            subprocess.run(
                ["powershell", "-Command",
                 f"[Environment]::SetEnvironmentVariable('Path', '{new_path}', 'User')"],
                check=False
            )
        except Exception as e:
            print(f"Failed to update PATH: {e}")
