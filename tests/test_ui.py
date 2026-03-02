"""Tests for UI modules."""
import pytest
from unittest.mock import Mock, patch
from ai_cli.ui.theme import Theme


class TestTheme:
    """Test Theme class."""
    
    def test_theme_colors(self):
        """Test theme color definitions."""
        assert Theme.PRIMARY is not None
        assert Theme.SECONDARY is not None
        assert Theme.SUCCESS is not None
        assert Theme.ERROR is not None
        assert Theme.WARNING is not None
        assert Theme.MUTED is not None
        assert Theme.HIGHLIGHT is not None
    
    def test_theme_icons(self):
        """Test theme icon definitions."""
        assert Theme.FOLDER == "📁"
        assert Theme.FILE == "📄"
        assert Theme.SUCCESS_ICON == "✅"
        assert Theme.ERROR_ICON == "❌"
        assert Theme.ARROW == "→"
    
    def test_dark_theme(self):
        """Test dark theme variant."""
        dark = Theme.dark_theme()
        
        assert "primary" in dark
        assert "secondary" in dark
        assert "success" in dark
        assert "error" in dark
        assert "warning" in dark
        assert "muted" in dark
        assert "highlight" in dark


class TestMenuRenderer:
    """Test MenuRenderer class."""
    
    @patch('ai_cli.ui.menu.Console')
    def test_menu_renderer_init(self, mock_console):
        """Test MenuRenderer initialization."""
        from ai_cli.ui.menu import MenuRenderer
        
        renderer = MenuRenderer()
        assert renderer.console is not None
    
    @patch('ai_cli.ui.menu.Console')
    def test_render_tree(self, mock_console):
        """Test tree rendering."""
        from ai_cli.ui.menu import MenuRenderer
        
        renderer = MenuRenderer()
        items = [
            {"name": "Project 1", "type": "project"},
            {"name": "Folder 1", "type": "folder"}
        ]
        
        renderer.render_tree(items, selected=0)
        assert renderer.console.print.called
    
    @patch('ai_cli.ui.menu.Console')
    def test_render_tools(self, mock_console):
        """Test tools list rendering."""
        from ai_cli.ui.menu import MenuRenderer
        
        renderer = MenuRenderer()
        tools = [
            {"name": "kiro-cli", "env": "WSL"},
            {"name": "claude", "env": "Win"}
        ]
        
        renderer.render_tools(tools, selected=0)
        assert renderer.console.print.called
    
    @patch('ai_cli.ui.menu.Console')
    def test_render_breadcrumb(self, mock_console):
        """Test breadcrumb rendering."""
        from ai_cli.ui.menu import MenuRenderer
        
        renderer = MenuRenderer()
        path = ["Home", "Projects", "Frontend"]
        
        renderer.render_breadcrumb(path)
        assert renderer.console.print.called
    
    @patch('ai_cli.ui.menu.Console')
    def test_clear(self, mock_console):
        """Test console clear."""
        from ai_cli.ui.menu import MenuRenderer
        
        renderer = MenuRenderer()
        renderer.clear()
        assert renderer.console.clear.called


class TestInputHandler:
    """Test InputHandler class."""
    
    def test_input_handler_init(self):
        """Test InputHandler initialization."""
        from ai_cli.ui.input import InputHandler
        
        handler = InputHandler()
        assert handler.bindings is not None
    
    def test_input_event_enum(self):
        """Test InputEvent enum values."""
        from ai_cli.ui.input import InputEvent
        
        assert InputEvent.UP.value == "up"
        assert InputEvent.DOWN.value == "down"
        assert InputEvent.ENTER.value == "enter"
        assert InputEvent.ESCAPE.value == "escape"
        assert InputEvent.QUIT.value == "quit"
        assert InputEvent.NEW.value == "new"
        assert InputEvent.DELETE.value == "delete"
