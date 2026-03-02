"""Tests for CLI entry point."""
import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner


class TestCLI:
    """Test CLI command line interface."""
    
    def test_version_option(self):
        """Test --version option."""
        from ai_cli.cli import main
        
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    @patch('ai_cli.cli.ConfigManager')
    def test_init_option_new_config(self, mock_config):
        """Test --init option with new config."""
        from ai_cli.cli import main
        
        mock_manager = Mock()
        mock_manager.get_config_dir.return_value = Mock(
            __truediv__=lambda self, x: Mock(exists=lambda: False)
        )
        mock_config.return_value = mock_manager
        
        runner = CliRunner()
        result = runner.invoke(main, ['--init'])
        
        assert result.exit_code == 0
        assert 'created' in result.output.lower()
    
    @patch('ai_cli.cli.ConfigManager')
    def test_init_option_existing_config(self, mock_config):
        """Test --init option with existing config."""
        from ai_cli.cli import main
        
        mock_manager = Mock()
        mock_manager.get_config_dir.return_value = Mock(
            __truediv__=lambda self, x: Mock(exists=lambda: True)
        )
        mock_config.return_value = mock_manager
        
        runner = CliRunner()
        result = runner.invoke(main, ['--init'])
        
        assert result.exit_code == 0
        assert 'already exists' in result.output.lower()
    
    @patch('ai_cli.cli.subprocess.run')
    @patch('ai_cli.cli.ConfigManager')
    @patch('ai_cli.cli.platform.system', return_value='Linux')
    def test_config_option_linux(self, mock_system, mock_config, mock_subprocess):
        """Test --config option on Linux."""
        from ai_cli.cli import main
        
        mock_manager = Mock()
        mock_manager.get_config_dir.return_value = Mock(
            __truediv__=lambda self, x: Mock(exists=lambda: True, __str__=lambda s: '/path/config.json')
        )
        mock_config.return_value = mock_manager
        
        runner = CliRunner()
        result = runner.invoke(main, ['--config'])
        
        assert result.exit_code == 0
        mock_subprocess.assert_called_once()
    
    @patch('ai_cli.cli.Application')
    def test_default_run(self, mock_app):
        """Test default behavior (run application)."""
        from ai_cli.cli import main
        
        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance
        
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code == 0
        mock_app_instance.run.assert_called_once()
    
    @patch('ai_cli.cli.Application')
    def test_keyboard_interrupt(self, mock_app):
        """Test keyboard interrupt handling."""
        from ai_cli.cli import main
        
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = KeyboardInterrupt()
        mock_app.return_value = mock_app_instance
        
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code == 0
        assert 'Goodbye' in result.output
