"""Core data models for AI-CLI."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any


class ToolEnvironment(Enum):
    """Tool runtime environment."""
    WINDOWS = "windows"
    WSL = "wsl"
    LINUX = "linux"
    MACOS = "macos"


@dataclass
class ProjectNode:
    """Project tree node."""
    type: str  # "project" or "folder"
    name: str
    path: Optional[str] = None
    children: List['ProjectNode'] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "type": self.type,
            "name": self.name
        }
        if self.path:
            result["path"] = self.path
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        if self.env:
            result["env"] = self.env
        if self.description:
            result["description"] = self.description
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectNode':
        """Create from dictionary."""
        # Handle case where data might be a string (malformed config)
        if isinstance(data, str):
            raise ValueError(f"Expected dict for ProjectNode, got string: {data}")
        
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict for ProjectNode, got {type(data)}")
        
        children_data = data.get("children", [])
        
        # Ensure children_data is a list
        if not isinstance(children_data, list):
            children_data = []
        
        children = [cls.from_dict(child) for child in children_data]
        
        return cls(
            type=data.get("type", "project"),
            name=data.get("name", "Unknown"),
            path=data.get("path"),
            children=children,
            env=data.get("env", {}),
            description=data.get("description")
        )


@dataclass
class ToolConfig:
    """Tool configuration."""
    name: str
    display_name: str
    win_install: Optional[str]
    wsl_install: Optional[str]
    linux_install: Optional[str]
    macos_install: Optional[str]
    check_command: str
    url: str
    # Cache fields (stored in config file)
    win_available: bool = False
    wsl_available: bool = False
    linux_available: bool = False
    macos_available: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "name": self.name,
            "displayName": self.display_name,
            "winInstall": self.win_install,
            "wslInstall": self.wsl_install,
            "linuxInstall": self.linux_install,
            "macosInstall": self.macos_install,
            "checkCommand": self.check_command,
            "url": self.url
        }
        # Include cache fields
        if self.win_available:
            result["winAvailable"] = self.win_available
        if self.wsl_available:
            result["wslAvailable"] = self.wsl_available
        if self.linux_available:
            result["linuxAvailable"] = self.linux_available
        if self.macos_available:
            result["macosAvailable"] = self.macos_available
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolConfig':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            display_name=data.get("displayName", data["name"]),
            win_install=data.get("winInstall"),
            wsl_install=data.get("wslInstall"),
            linux_install=data.get("linuxInstall"),
            macos_install=data.get("macosInstall"),
            check_command=data["checkCommand"],
            url=data["url"],
            win_available=data.get("winAvailable", False),
            wsl_available=data.get("wslAvailable", False),
            linux_available=data.get("linuxAvailable", False),
            macos_available=data.get("macosAvailable", False)
        )


@dataclass
class Tool:
    """Detected tool instance."""
    name: str
    display_name: str
    environment: ToolEnvironment
    available: bool
    url: Optional[str] = None
    version: Optional[str] = None
    
    def get_display_label(self) -> str:
        """Get display label with environment tag."""
        env_labels = {
            ToolEnvironment.WINDOWS: "[Win]",
            ToolEnvironment.WSL: "[WSL]",
            ToolEnvironment.LINUX: "",
            ToolEnvironment.MACOS: ""
        }
        label = env_labels.get(self.environment, "")
        return f"{label} {self.display_name}".strip()


@dataclass
class Settings:
    """Global settings."""
    language: str = "auto"
    terminal_emulator: str = "default"
    theme: str = "default"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "language": self.language,
            "terminalEmulator": self.terminal_emulator,
            "theme": self.theme
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create from dictionary."""
        return cls(
            language=data.get("language", "auto"),
            terminal_emulator=data.get("terminalEmulator", "default"),
            theme=data.get("theme", "default")
        )


@dataclass
class Config:
    """Complete configuration."""
    projects: List[ProjectNode]
    tools: List[ToolConfig]
    settings: Settings
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "projects": [proj.to_dict() for proj in self.projects],
            "tools": [tool.to_dict() for tool in self.tools],
            "settings": self.settings.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create from dictionary."""
        projects = [ProjectNode.from_dict(p) for p in data.get("projects", [])]
        tools = [ToolConfig.from_dict(t) for t in data.get("tools", [])]
        settings = Settings.from_dict(data.get("settings", {}))
        
        return cls(
            projects=projects,
            tools=tools,
            settings=settings
        )
