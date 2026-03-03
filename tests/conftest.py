"""Pytest configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

from ai_cli.models import ProjectNode, ToolConfig, Settings, Config


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_project() -> ProjectNode:
    """Create a sample project node."""
    return ProjectNode(
        type="project",
        name="Test Project",
        path="/test/project",
        env={"API_KEY": "test-key"}
    )


@pytest.fixture
def sample_folder() -> ProjectNode:
    """Create a sample folder node with children."""
    child1 = ProjectNode(type="project", name="Child1", path="/test/child1")
    child2 = ProjectNode(type="project", name="Child2", path="/test/child2")
    
    return ProjectNode(
        type="folder",
        name="Test Folder",
        children=[child1, child2]
    )


@pytest.fixture
def sample_tool_config() -> ToolConfig:
    """Create a sample tool configuration."""
    return ToolConfig(
        name="test-tool",
        display_name="Test Tool",
        win_install="npm install -g test-tool",
        wsl_install="npm install -g test-tool",
        linux_install="npm install -g test-tool",
        macos_install="brew install test-tool",
        check_command="test-tool --version",
        url="https://test-tool.com"
    )


@pytest.fixture
def sample_config(sample_project: ProjectNode, sample_tool_config: ToolConfig) -> Config:
    """Create a sample complete configuration."""
    return Config(
        projects=[sample_project],
        tools=[sample_tool_config],
        settings=Settings()
    )


@pytest.fixture
def sample_config_dict() -> dict:
    """Create a sample configuration dictionary."""
    return {
        "projects": [
            {
                "type": "project",
                "name": "Test Project",
                "path": "/test/project",
                "env": {"API_KEY": "test-key"}
            }
        ],
        "tools": [
            {
                "name": "kiro-cli",
                "displayName": "Kiro CLI",
                "winInstall": None,
                "wslInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
                "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
                "macosInstall": "brew install kiro-cli",
                "checkCommand": "kiro-cli --version",
                "url": "https://kiro.dev/cli/"
            }
        ],
        "settings": {
            "language": "auto",
            "terminalEmulator": "default",
            "theme": "default"
        }
    }


@pytest.fixture
def legacy_config_dict() -> dict:
    """Create a legacy flat configuration dictionary."""
    return {
        "projects": [
            {
                "name": "Old Project",
                "path": "/old/project",
                "env": {"KEY": "value"}
            }
        ],
        "tools": [],
        "settings": {}
    }
