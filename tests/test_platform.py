"""Tests for platform adapters."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_cli.models import Tool, ProjectNode, ToolEnvironment


class TestPlatformFactory:
    """Test platform factory."""
    
    @patch('ai_cli.platform.factory.platform.system', return_value='Windows')
    def test_get_windows_adapter(self, mock_system):
        """Test getting Windows adapter."""
        from ai_cli.platform.factory import get_platform_adapter
        from ai_cli.platform.windows import WindowsPlatformAdapter
        
        adapter = get_platform_adapter()
        assert isinstance(adapter, WindowsPlatformAdapter)
    
    @patch('ai_cli.platform.factory.platform.system', return_value='Linux')
    def test_get_linux_adapter(self, mock_system):
        """Test getting Linux adapter."""
        from ai_cli.platform.factory import get_platform_adapter
        from ai_cli.platform.linux import LinuxPlatformAdapter
        
        adapter = get_platform_adapter()
        assert isinstance(adapter, LinuxPlatformAdapter)
    
    @patch('ai_cli.platform.factory.platform.system', return_value='Darwin')
    def test_get_macos_adapter(self, mock_system):
        """Test getting macOS adapter."""
        from ai_cli.platform.factory import get_platform_adapter
        from ai_cli.platform.macos import MacOSPlatformAdapter
        
        adapter = get_platform_adapter()
        assert isinstance(adapter, MacOSPlatformAdapter)
    
    @patch('ai_cli.platform.factory.platform.system', return_value='Unknown')
    def test_unsupported_platform(self, mock_system):
        """Test unsupported platform raises error."""
        from ai_cli.platform.factory import get_platform_adapter
        
        with pytest.raises(RuntimeError):
            get_platform_adapter()


class TestWindowsPlatformAdapter:
    """Test Windows platform adapter."""
    
    def test_get_shell_command_windows(self):
        """Test Windows shell command generation."""
        from ai_cli.platform.windows import WindowsPlatformAdapter
        
        adapter = WindowsPlatformAdapter()
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.WINDOWS,
            path="C:\\tools\\test.exe"
        )
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="C:\\Projects\\test",
            env={"KEY": "value"}
        )
        
        command = adapter.get_shell_command(tool, project)
        
        assert "cd /d C:\\Projects\\test" in command
        assert "set KEY=value" in command
        assert "test-tool" in command
    
    def test_get_shell_command_wsl(self):
        """Test WSL shell command generation."""
        from ai_cli.platform.windows import WindowsPlatformAdapter
        
        adapter = WindowsPlatformAdapter()
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.WSL,
            path="/usr/bin/test-tool"
        )
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="C:\\Projects\\test",
            env={"KEY": "value"}
        )
        
        command = adapter.get_shell_command(tool, project)
        
        assert "/mnt/c/Projects/test" in command
        assert "export KEY=" in command
        assert "test-tool" in command


class TestLinuxPlatformAdapter:
    """Test Linux platform adapter."""
    
    @patch('ai_cli.platform.linux.shutil.which', return_value='/usr/bin/gnome-terminal')
    def test_detect_terminal(self, mock_which):
        """Test terminal detection."""
        from ai_cli.platform.linux import LinuxPlatformAdapter
        
        adapter = LinuxPlatformAdapter()
        terminal = adapter._detect_terminal()
        
        assert terminal == '/usr/bin/gnome-terminal'
    
    def test_get_shell_command(self):
        """Test Linux shell command generation."""
        from ai_cli.platform.linux import LinuxPlatformAdapter
        
        adapter = LinuxPlatformAdapter()
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.LINUX,
            path="/usr/bin/test-tool"
        )
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="/home/user/project",
            env={"KEY": "value"}
        )
        
        command = adapter.get_shell_command(tool, project)
        
        assert "cd /home/user/project" in command
        assert "export KEY=" in command
        assert "test-tool" in command


class TestMacOSPlatformAdapter:
    """Test macOS platform adapter."""
    
    @patch('ai_cli.platform.macos.subprocess.run')
    def test_has_iterm_true(self, mock_run):
        """Test iTerm2 detection when installed."""
        from ai_cli.platform.macos import MacOSPlatformAdapter
        
        mock_run.return_value = Mock(returncode=0)
        adapter = MacOSPlatformAdapter()
        
        assert adapter._has_iterm() is True
    
    @patch('ai_cli.platform.macos.subprocess.run')
    def test_has_iterm_false(self, mock_run):
        """Test iTerm2 detection when not installed."""
        from ai_cli.platform.macos import MacOSPlatformAdapter
        
        mock_run.return_value = Mock(returncode=1)
        adapter = MacOSPlatformAdapter()
        
        assert adapter._has_iterm() is False
    
    def test_get_shell_command(self):
        """Test macOS shell command generation."""
        from ai_cli.platform.macos import MacOSPlatformAdapter
        
        adapter = MacOSPlatformAdapter()
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.MACOS,
            path="/usr/local/bin/test-tool"
        )
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="/Users/user/project",
            env={"KEY": "value"}
        )
        
        command = adapter.get_shell_command(tool, project)
        
        assert "cd " in command
        assert "export KEY=" in command
        assert "test-tool" in command
