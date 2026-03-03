"""Tool detection and management."""
import asyncio
import shutil
import subprocess
import sys
from typing import List, Optional
from ai_cli.models import Tool, ToolConfig, ToolEnvironment


class WindowsToolDetector:
    """Windows platform tool detector (supports Windows + WSL)."""
    
    @staticmethod
    def is_wsl_available() -> bool:
        """Check if WSL is available."""
        try:
            result = subprocess.run(
                ["wsl.exe", "-e", "true"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    async def detect_windows_tools_batch(self, tools_config: List[ToolConfig]) -> None:
        """Detect Windows tools and update config."""
        for tool_config in tools_config:
            if not tool_config.win_install:
                tool_config.win_available = False
                continue
            
            tool_path = shutil.which(tool_config.name)
            tool_config.win_available = tool_path is not None
    
    async def detect_wsl_tools_batch(self, tools_config: List[ToolConfig]) -> None:
        """Detect WSL tools and update config."""
        if not self.is_wsl_available():
            for tool_config in tools_config:
                tool_config.wsl_available = False
            return
        
        # Batch check all WSL tools in one command
        wsl_tools = [tc for tc in tools_config if tc.wsl_install]
        if not wsl_tools:
            return
        
        tool_names = ' '.join([tc.name for tc in wsl_tools])
        check_script = f"for t in {tool_names}; do if command -v $t >/dev/null 2>&1; then echo $t; fi; done"
        
        try:
            result = subprocess.run(
                ["wsl.exe", "-e", "bash", "-ic", check_script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            available_tools = set()
            if result.returncode == 0 and result.stdout:
                available_tools = set(line.strip() for line in result.stdout.strip().split('\n') if line.strip())
            
            for tool_config in wsl_tools:
                tool_config.wsl_available = tool_config.name in available_tools
        except:
            for tool_config in wsl_tools:
                tool_config.wsl_available = False
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> None:
        """Detect all tools and update config in place."""
        await asyncio.gather(
            self.detect_windows_tools_batch(tools_config),
            self.detect_wsl_tools_batch(tools_config)
        )


class LinuxToolDetector:
    """Linux platform tool detector."""
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> None:
        """Detect all tools on Linux and update config in place."""
        for tool_config in tools_config:
            if not tool_config.linux_install:
                tool_config.linux_available = False
                continue
            
            tool_path = shutil.which(tool_config.name)
            tool_config.linux_available = tool_path is not None


class MacOSToolDetector:
    """macOS platform tool detector."""
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> None:
        """Detect all tools on macOS and update config in place."""
        for tool_config in tools_config:
            if not tool_config.macos_install:
                tool_config.macos_available = False
                continue
            
            tool_path = shutil.which(tool_config.name)
            tool_config.macos_available = tool_path is not None


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
        self._background_task: Optional[asyncio.Task] = None
    
    async def detect_all_tools(self, tools_config: List[ToolConfig], force: bool = False) -> List[Tool]:
        """
        Detect all tools on current platform.
        
        Args:
            tools_config: List of tool configurations (will be updated in place)
            force: If True, cancel background task and run detection immediately
        
        Returns:
            List of available tools
        """
        # Check if cache is empty (no detection has been done yet)
        cache_empty = self._is_cache_empty(tools_config)
        
        if force or cache_empty:
            # Cancel background task if running
            if self._background_task and not self._background_task.done():
                self._background_task.cancel()
                try:
                    await self._background_task
                except asyncio.CancelledError:
                    pass
                self._background_task = None
            
            # Run detection and update config
            await self.detector.detect_all_tools(tools_config)
        
        # Build tool list from cached config
        return self._build_tool_list(tools_config)
    
    def _is_cache_empty(self, tools_config: List[ToolConfig]) -> bool:
        """Check if cache is empty (no detection has been done)."""
        if sys.platform == 'win32':
            # Check if any tool has cache data
            return not any(tc.win_available or tc.wsl_available for tc in tools_config)
        elif sys.platform == 'linux':
            return not any(tc.linux_available for tc in tools_config)
        elif sys.platform == 'darwin':
            return not any(tc.macos_available for tc in tools_config)
        return True
    
    def _build_tool_list(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """Build tool list from config cache."""
        tools = []
        
        for tool_config in tools_config:
            # Windows environment
            if sys.platform == 'win32':
                if tool_config.wsl_available:
                    tools.append(Tool(
                        name=tool_config.name,
                        display_name=tool_config.display_name,
                        environment=ToolEnvironment.WSL,
                        available=True,
                        url=tool_config.url
                    ))
                if tool_config.win_available:
                    tools.append(Tool(
                        name=tool_config.name,
                        display_name=tool_config.display_name,
                        environment=ToolEnvironment.WINDOWS,
                        available=True,
                        url=tool_config.url
                    ))
            # Linux environment
            elif sys.platform == 'linux':
                if tool_config.linux_available:
                    tools.append(Tool(
                        name=tool_config.name,
                        display_name=tool_config.display_name,
                        environment=ToolEnvironment.LINUX,
                        available=True,
                        url=tool_config.url
                    ))
            # macOS environment
            elif sys.platform == 'darwin':
                if tool_config.macos_available:
                    tools.append(Tool(
                        name=tool_config.name,
                        display_name=tool_config.display_name,
                        environment=ToolEnvironment.MACOS,
                        available=True,
                        url=tool_config.url
                    ))
        
        return tools
    
    def start_background_detection(self, tools_config: List[ToolConfig]) -> None:
        """Start background tool detection (non-blocking)."""
        # Don't start if already running
        if self._background_task and not self._background_task.done():
            return
        
        self._background_task = asyncio.create_task(self._background_detect(tools_config))
    
    async def _background_detect(self, tools_config: List[ToolConfig]) -> None:
        """Background detection task."""
        try:
            await self.detector.detect_all_tools(tools_config)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass  # Silent fail for background task
    
    def is_background_complete(self) -> bool:
        """Check if background detection is complete."""
        return self._background_task is not None and self._background_task.done()
    
    def cleanup_background_task(self) -> None:
        """Clean up completed background task."""
        if self._background_task and self._background_task.done():
            self._background_task = None
