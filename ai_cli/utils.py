"""Path conversion utilities for Windows/WSL interoperability."""

import re
from typing import Literal


class PathConverter:
    """Utility class for converting paths between Windows and WSL formats."""
    
    @staticmethod
    def to_wsl_path(windows_path: str) -> str:
        """Convert Windows path to WSL path format.
        
        Args:
            windows_path: Windows-style path (e.g., 'C:\\Projects\\file.txt')
            
        Returns:
            WSL-style path (e.g., '/mnt/c/Projects/file.txt')
        """
        # Already WSL path
        if windows_path.startswith('/mnt/'):
            return windows_path
        
        # Not a Windows absolute path
        if not re.match(r'^[A-Za-z]:[\\/]', windows_path):
            return windows_path.replace('\\', '/')
        
        # Convert C:\path -> /mnt/c/path
        match = re.match(r'^([A-Za-z]):([\\/].*)', windows_path)
        if not match:
            return windows_path
            
        drive, path = match.groups()
        wsl_path = f"/mnt/{drive.lower()}{path.replace(chr(92), '/')}"  # chr(92) is backslash
        return wsl_path.rstrip('/')
    
    @staticmethod
    def to_windows_path(wsl_path: str) -> str:
        """Convert WSL path to Windows path format.
        
        Args:
            wsl_path: WSL-style path (e.g., '/mnt/c/Projects/file.txt')
            
        Returns:
            Windows-style path (e.g., 'C:\\Projects\\file.txt')
        """
        # Already Windows path
        if re.match(r'^[A-Za-z]:[\\/]', wsl_path):
            return wsl_path
        
        # Not a WSL mount path
        if not wsl_path.startswith('/mnt/'):
            return wsl_path
        
        # Convert /mnt/c/path -> C:\path
        match = re.match(r'^/mnt/([a-zA-Z])(/.*)$', wsl_path)
        if not match:
            return wsl_path
            
        drive, path = match.groups()
        windows_path = f"{drive.upper()}:{path.replace('/', chr(92))}"  # chr(92) is backslash
        return windows_path
    
    @staticmethod
    def normalize_for_environment(path: str, environment: str) -> str:
        """Normalize path for target environment.
        
        Args:
            path: Input path in any format
            environment: Target environment ('windows', 'wsl', 'linux', 'macos')
            
        Returns:
            Path normalized for the target environment
        """
        env_lower = environment.lower()
        
        if env_lower == 'wsl':
            return PathConverter.to_wsl_path(path)
        elif env_lower == 'windows':
            return PathConverter.to_windows_path(path)
        else:
            # Linux/macOS: just normalize slashes
            return path.replace('\\', '/')
