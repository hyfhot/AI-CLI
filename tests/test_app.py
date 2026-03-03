"""Integration tests for main application."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from ai_cli.models import ProjectNode, Tool, ToolEnvironment, ToolConfig


class TestApplicationIntegration:
    """Test Application class integration."""
    
    @patch('ai_cli.app.ConfigManager')
    @patch('ai_cli.app.MenuRenderer')
    @patch('ai_cli.app.InputHandler')
    @patch('ai_cli.app.get_platform_adapter')
    def test_application_initialization(self, mock_adapter, mock_input, mock_menu, mock_config):
        """Test Application initializes all components."""
        from ai_cli.app import Application
        
        app = Application()
        
        assert app.config_manager is not None
        assert app.menu is not None
        assert app.input_handler is not None
        assert app.platform_adapter is not None
    
    @patch('ai_cli.app.ConfigManager')
    @patch('ai_cli.app.MenuRenderer')
    @patch('ai_cli.app.InputHandler')
    @patch('ai_cli.app.get_platform_adapter')
    def test_get_current_node_root(self, mock_adapter, mock_input, mock_menu, mock_config):
        """Test getting root node."""
        from ai_cli.app import Application
        
        mock_config_instance = Mock()
        mock_config_instance.load.return_value = Mock(projects=[])
        mock_config.return_value = mock_config_instance
        
        app = Application()
        app.current_path = []
        
        node = app._get_current_node()
        assert node is None
    
    @patch('ai_cli.app.ConfigManager')
    @patch('ai_cli.app.MenuRenderer')
    @patch('ai_cli.app.InputHandler')
    @patch('ai_cli.app.get_platform_adapter')
    def test_launch_tool_success(self, mock_adapter, mock_input, mock_menu, mock_config):
        """Test successful tool launch."""
        from ai_cli.app import Application
        
        mock_config_instance = Mock()
        mock_config_instance.load.return_value = Mock(projects=[])
        mock_config.return_value = mock_config_instance
        
        mock_adapter_instance = Mock()
        mock_adapter.return_value = mock_adapter_instance
        
        app = Application()
        
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.LINUX,
            path="/usr/bin/test-tool"
        )
        
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="/test/project"
        )
        
        app._launch_tool(tool, project)
        
        mock_adapter_instance.launch_terminal.assert_called_once()
    
    @patch('ai_cli.app.ConfigManager')
    @patch('ai_cli.app.MenuRenderer')
    @patch('ai_cli.app.InputHandler')
    @patch('ai_cli.app.get_platform_adapter')
    def test_launch_tool_failure(self, mock_adapter, mock_input, mock_menu, mock_config):
        """Test tool launch failure handling."""
        from ai_cli.app import Application
        
        mock_config_instance = Mock()
        mock_config_instance.load.return_value = Mock(projects=[])
        mock_config.return_value = mock_config_instance
        
        mock_adapter_instance = Mock()
        mock_adapter_instance.launch_terminal.side_effect = Exception("Launch failed")
        mock_adapter.return_value = mock_adapter_instance
        
        app = Application()
        
        tool = Tool(
            name="test-tool",
            display_name="Test Tool",
            environment=ToolEnvironment.LINUX,
            path="/usr/bin/test-tool"
        )
        
        project = ProjectNode(
            type="project",
            name="Test Project",
            path="/test/project"
        )
        
        # Should not raise exception
        app._launch_tool(tool, project)
