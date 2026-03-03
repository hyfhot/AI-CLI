"""Platform adapter factory."""
import platform
from typing import Type
from .base import PlatformAdapter
from .windows import WindowsPlatformAdapter
from .linux import LinuxPlatformAdapter
from .macos import MacOSPlatformAdapter


def get_platform_adapter() -> PlatformAdapter:
    """Get platform adapter for current system."""
    system = platform.system()
    
    if system == "Windows":
        return WindowsPlatformAdapter()
    elif system == "Linux":
        return LinuxPlatformAdapter()
    elif system == "Darwin":
        return MacOSPlatformAdapter()
    else:
        raise RuntimeError(f"Unsupported platform: {system}")
