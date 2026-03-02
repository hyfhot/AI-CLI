"""Tool detection module for AI-CLI."""

import asyncio
import sys
import shutil
import subprocess
import time
from typing import List, Optional, Dict

from ..models import Tool, ToolConfig, ToolEnvironment


class WindowsToolDetector:
    """Windows platform tool detector (supports Windows + WSL)."""
    
    def __init__(self):
        self._cache: Optional[List[Tool]] = None
        self._cache_time: Optional[float] = None
        self._cache_ttl = 30  # 30 seconds cache
    
    @staticmethod
    def is_wsl_available() -> bool:
        """Check if WSL is available."""
        try:
            result = subprocess.run(
                ["wsl.exe", "--status"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def detect_windows_tools_batch(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Batch detect Windows tools."""
        tools = []
        
        for tool_config in tools_config:
            if not tool_config.win_install:
                continue
            
            tool_path = shutil.which(tool_config.name)
            if tool_path:
                tools.append(Tool(
                    name=tool_config.name,
                    display_name=tool_config.display_name,
                    environment=ToolEnvironment.WINDOWS,
                    available=True,
                    url=tool_config.url,
                    version=None
                ))
        
        return tools
    
    async def detect_wsl_tools_batch(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Batch detect WSL tools with single WSL call."""
        if not self.is_wsl_available():
            return []
        
        wsl_tools = [t for t in tools_config if t.wsl_install]
        if not wsl_tools:
            return []
        
        # Single WSL call to check all tools
        tool_names = ' '.join([t.name for t in wsl_tools])
        check_script = f"for t in {tool_names}; do if command -v $t >/dev/null 2>&1; then echo $t; fi; done"
        
        try:
            result = await asyncio.create_subprocess_exec(
                'wsl.exe', '-e', 'bash', '-ic', check_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(result.communicate(), timeout=3.0)
            
            available_names = set(line.strip() for line in stdout.decode().strip().split('\n') if line.strip())
            
            tools = []
            for tool_config in wsl_tools:
                if tool_config.name in available_names:
                    tools.append(Tool(
                        name=tool_config.name,
                        display_name=tool_config.display_name,
                        environment=ToolEnvironment.WSL,
                        available=True,
                        url=tool_config.url,
                        version=None
                    ))
            
            return tools
        except (asyncio.TimeoutError, Exception):
            return []
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Detect all tools with caching."""
        # Check cache
        if self._cache is not None and self._cache_time is not None:
            if time.time() - self._cache_time < self._cache_ttl:
                return self._cache
        
        # Detect Windows and WSL tools in parallel
        win_tools_task = self.detect_windows_tools_batch(tools_config)
        wsl_tools_task = self.detect_wsl_tools_batch(tools_config)
        
        win_tools, wsl_tools = await asyncio.gather(win_tools_task, wsl_tools_task)
        
        all_tools = win_tools + wsl_tools
        
        # Update cache
        self._cache = all_tools
        self._cache_time = time.time()
        
        return all_tools


class LinuxToolDetector:
    """Linux platform tool detector."""
    
    def __init__(self):
        self._cache: Optional[List[Tool]] = None
        self._cache_time: Optional[float] = None
        self._cache_ttl = 30
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Detect all tools on Linux with caching."""
        if self._cache is not None and self._cache_time is not None:
            if time.time() - self._cache_time < self._cache_ttl:
                return self._cache
        
        tools = []
        
        for tool_config in tools_config:
            if not tool_config.linux_install:
                continue
            
            tool_path = shutil.which(tool_config.name)
            if tool_path:
                tools.append(Tool(
                    name=tool_config.name,
                    display_name=tool_config.display_name,
                    environment=ToolEnvironment.LINUX,
                    available=True,
                    url=tool_config.url,
                    version=None
                ))
        
        self._cache = tools
        self._cache_time = time.time()
        
        return tools


class MacOSToolDetector:
    """macOS platform tool detector."""
    
    def __init__(self):
        self._cache: Optional[List[Tool]] = None
        self._cache_time: Optional[float] = None
        self._cache_ttl = 30
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Detect all tools on macOS with caching."""
        if self._cache is not None and self._cache_time is not None:
            if time.time() - self._cache_time < self._cache_ttl:
                return self._cache
        
        tools = []
        
        for tool_config in tools_config:
            if not tool_config.macos_install:
                continue
            
            tool_path = shutil.which(tool_config.name)
            if tool_path:
                tools.append(Tool(
                    name=tool_config.name,
                    display_name=tool_config.display_name,
                    environment=ToolEnvironment.MACOS,
                    available=True,
                    url=tool_config.url,
                    version=None
                ))
        
        self._cache = tools
        self._cache_time = time.time()
        
        return tools


class ToolDetector:
    """Unified tool detector interface."""
    
    def __init__(self):
        """Initialize detector based on platform."""
        if sys.platform == 'win32':
            self.detector = WindowsToolDetector()
        elif sys.platform == 'darwin':
            self.detector = MacOSToolDetector()
        else:
            self.detector = LinuxToolDetector()
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Detect all tools on current platform."""
        return await self.detector.detect_all_tools(tools_config)
    
    def clear_cache(self):
        """Clear detection cache."""
        self.detector._cache = None
        self.detector._cache_time = None
