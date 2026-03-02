"""Unit tests for data models."""

import pytest
from ai_cli.models import (
    ToolEnvironment,
    ProjectNode,
    ToolConfig,
    Tool,
    Settings,
    Config
)


class TestToolEnvironment:
    """Test ToolEnvironment enum."""
    
    def test_enum_values(self):
        """Test enum has correct values."""
        assert ToolEnvironment.WINDOWS.value == "windows"
        assert ToolEnvironment.WSL.value == "wsl"
        assert ToolEnvironment.LINUX.value == "linux"
        assert ToolEnvironment.MACOS.value == "macos"


class TestProjectNode:
    """Test ProjectNode dataclass."""
    
    def test_create_project(self):
        """Test creating a project node."""
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="/path/to/project"
        )
        assert project.type == "project"
        assert project.name == "Test Project"
        assert project.path == "/path/to/project"
        assert project.children == []
        assert project.env == {}
    
    def test_create_folder(self):
        """Test creating a folder node."""
        folder = ProjectNode(
            type="folder",
            name="Test Folder"
        )
        assert folder.type == "folder"
        assert folder.path is None
    
    def test_to_dict(self):
        """Test serialization to dict."""
        project = ProjectNode(
            type="project",
            name="Test",
            path="/test",
            env={"KEY": "value"}
        )
        data = project.to_dict()
        
        assert data["type"] == "project"
        assert data["name"] == "Test"
        assert data["path"] == "/test"
        assert data["env"] == {"KEY": "value"}
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "type": "project",
            "name": "Test",
            "path": "/test",
            "env": {"KEY": "value"}
        }
        project = ProjectNode.from_dict(data)
        
        assert project.type == "project"
        assert project.name == "Test"
        assert project.path == "/test"
        assert project.env == {"KEY": "value"}
    
    def test_recursive_structure(self):
        """Test recursive tree structure."""
        child1 = ProjectNode(type="project", name="Child1", path="/child1")
        child2 = ProjectNode(type="project", name="Child2", path="/child2")
        
        parent = ProjectNode(
            type="folder",
            name="Parent",
            children=[child1, child2]
        )
        
        assert len(parent.children) == 2
        assert parent.children[0].name == "Child1"
        
        # Test serialization with children
        data = parent.to_dict()
        assert len(data["children"]) == 2
        
        # Test deserialization with children
        restored = ProjectNode.from_dict(data)
        assert len(restored.children) == 2
        assert restored.children[0].name == "Child1"


class TestToolConfig:
    """Test ToolConfig dataclass."""
    
    def test_create_tool_config(self):
        """Test creating tool configuration."""
        config = ToolConfig(
            name="test-tool",
            display_name="Test Tool",
            win_install="npm install -g test-tool",
            wsl_install="npm install -g test-tool",
            linux_install="npm install -g test-tool",
            macos_install="brew install test-tool",
            check_command="test-tool --version",
            url="https://test-tool.com"
        )
        
        assert config.name == "test-tool"
        assert config.display_name == "Test Tool"
    
    def test_to_dict(self):
        """Test serialization."""
        config = ToolConfig(
            name="test",
            display_name="Test",
            win_install="win cmd",
            wsl_install=None,
            linux_install="linux cmd",
            macos_install=None,
            check_command="test --version",
            url="https://test.com"
        )
        data = config.to_dict()
        
        assert data["name"] == "test"
        assert data["displayName"] == "Test"
        assert data["winInstall"] == "win cmd"
        assert data["wslInstall"] is None
    
    def test_from_dict(self):
        """Test deserialization."""
        data = {
            "name": "test",
            "displayName": "Test",
            "winInstall": "win cmd",
            "wslInstall": None,
            "linuxInstall": "linux cmd",
            "macosInstall": None,
            "checkCommand": "test --version",
            "url": "https://test.com"
        }
        config = ToolConfig.from_dict(data)
        
        assert config.name == "test"
        assert config.win_install == "win cmd"


class TestTool:
    """Test Tool dataclass."""
    
    def test_create_tool(self):
        """Test creating detected tool."""
        tool = Tool(
            name="kiro-cli",
            display_name="Kiro CLI",
            environment=ToolEnvironment.WSL,
            available=True,
            version="1.0.0"
        )
        
        assert tool.name == "kiro-cli"
        assert tool.environment == ToolEnvironment.WSL
        assert tool.available is True
    
    def test_get_display_label_wsl(self):
        """Test display label for WSL tool."""
        tool = Tool(
            name="kiro-cli",
            display_name="Kiro CLI",
            environment=ToolEnvironment.WSL,
            available=True
        )
        
        assert tool.get_display_label() == "[WSL] Kiro CLI"
    
    def test_get_display_label_windows(self):
        """Test display label for Windows tool."""
        tool = Tool(
            name="claude",
            display_name="Claude Code",
            environment=ToolEnvironment.WINDOWS,
            available=True
        )
        
        assert tool.get_display_label() == "[Win] Claude Code"
    
    def test_get_display_label_linux(self):
        """Test display label for Linux tool (no prefix)."""
        tool = Tool(
            name="aider",
            display_name="Aider",
            environment=ToolEnvironment.LINUX,
            available=True
        )
        
        assert tool.get_display_label() == "Aider"


class TestSettings:
    """Test Settings dataclass."""
    
    def test_create_settings(self):
        """Test creating settings with defaults."""
        settings = Settings()
        
        assert settings.language == "auto"
        assert settings.terminal_emulator == "default"
        assert settings.theme == "default"
    
    def test_to_dict(self):
        """Test serialization."""
        settings = Settings(language="en", terminal_emulator="wt", theme="dark")
        data = settings.to_dict()
        
        assert data["language"] == "en"
        assert data["terminalEmulator"] == "wt"
        assert data["theme"] == "dark"
    
    def test_from_dict(self):
        """Test deserialization."""
        data = {
            "language": "zh",
            "terminalEmulator": "gnome-terminal",
            "theme": "light"
        }
        settings = Settings.from_dict(data)
        
        assert settings.language == "zh"
        assert settings.terminal_emulator == "gnome-terminal"


class TestConfig:
    """Test Config dataclass."""
    
    def test_create_config(self):
        """Test creating complete configuration."""
        config = Config(
            projects=[],
            tools=[],
            settings=Settings()
        )
        
        assert config.projects == []
        assert config.tools == []
        assert isinstance(config.settings, Settings)
    
    def test_to_dict(self):
        """Test serialization of complete config."""
        project = ProjectNode(type="project", name="Test", path="/test")
        tool = ToolConfig(
            name="test",
            display_name="Test",
            win_install=None,
            wsl_install=None,
            linux_install="test",
            macos_install=None,
            check_command="test --version",
            url="https://test.com"
        )
        
        config = Config(
            projects=[project],
            tools=[tool],
            settings=Settings()
        )
        
        data = config.to_dict()
        
        assert len(data["projects"]) == 1
        assert len(data["tools"]) == 1
        assert "settings" in data
    
    def test_from_dict(self):
        """Test deserialization of complete config."""
        data = {
            "projects": [
                {"type": "project", "name": "Test", "path": "/test"}
            ],
            "tools": [
                {
                    "name": "test",
                    "displayName": "Test",
                    "winInstall": None,
                    "wslInstall": None,
                    "linuxInstall": "test",
                    "macosInstall": None,
                    "checkCommand": "test --version",
                    "url": "https://test.com"
                }
            ],
            "settings": {
                "language": "auto",
                "terminalEmulator": "default",
                "theme": "default"
            }
        }
        
        config = Config.from_dict(data)
        
        assert len(config.projects) == 1
        assert len(config.tools) == 1
        assert config.projects[0].name == "Test"
        assert config.tools[0].name == "test"
