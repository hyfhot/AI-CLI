"""Unit tests for path conversion utilities."""

import pytest
from ai_cli.utils import PathConverter


class TestPathConverter:
    """Test PathConverter class."""
    
    def test_to_wsl_path_basic(self):
        """Test basic Windows to WSL conversion."""
        result = PathConverter.to_wsl_path("C:\\Projects\\test")
        assert result == "/mnt/c/Projects/test"
    
    def test_to_wsl_path_different_drives(self):
        """Test conversion with different drive letters."""
        assert PathConverter.to_wsl_path("D:\\Code\\app") == "/mnt/d/Code/app"
        assert PathConverter.to_wsl_path("E:\\Data") == "/mnt/e/Data"
    
    def test_to_wsl_path_forward_slash(self):
        """Test conversion with forward slashes."""
        result = PathConverter.to_wsl_path("C:/Projects/test")
        assert result == "/mnt/c/Projects/test"
    
    def test_to_wsl_path_already_wsl(self):
        """Test that WSL paths are not converted."""
        wsl_path = "/mnt/c/Projects/test"
        result = PathConverter.to_wsl_path(wsl_path)
        assert result == wsl_path
    
    def test_to_wsl_path_relative(self):
        """Test relative paths."""
        result = PathConverter.to_wsl_path("relative/path")
        assert result == "relative/path"
    
    def test_to_wsl_path_trailing_slash(self):
        """Test paths with trailing slashes."""
        result = PathConverter.to_wsl_path("C:\\Projects\\")
        assert result == "/mnt/c/Projects"
    
    def test_to_windows_path_basic(self):
        """Test basic WSL to Windows conversion."""
        result = PathConverter.to_windows_path("/mnt/c/Projects/test")
        assert result == "C:\\Projects\\test"
    
    def test_to_windows_path_different_drives(self):
        """Test conversion with different drive letters."""
        assert PathConverter.to_windows_path("/mnt/d/Code/app") == "D:\\Code\\app"
        assert PathConverter.to_windows_path("/mnt/e/Data") == "E:\\Data"
    
    def test_to_windows_path_already_windows(self):
        """Test that Windows paths are not converted."""
        win_path = "C:\\Projects\\test"
        result = PathConverter.to_windows_path(win_path)
        assert result == win_path
    
    def test_to_windows_path_not_mount(self):
        """Test non-mount WSL paths."""
        result = PathConverter.to_windows_path("/home/user/project")
        assert result == "/home/user/project"
    
    def test_normalize_for_environment_wsl(self):
        """Test normalization for WSL environment."""
        result = PathConverter.normalize_for_environment("C:\\Projects\\test", "wsl")
        assert result == "/mnt/c/Projects/test"
    
    def test_normalize_for_environment_windows(self):
        """Test normalization for Windows environment."""
        result = PathConverter.normalize_for_environment("/mnt/c/Projects/test", "windows")
        assert result == "C:\\Projects\\test"
    
    def test_normalize_for_environment_linux(self):
        """Test normalization for Linux environment."""
        result = PathConverter.normalize_for_environment("C:\\Projects\\test", "linux")
        assert result == "C:/Projects/test"
    
    def test_normalize_for_environment_macos(self):
        """Test normalization for macOS environment."""
        result = PathConverter.normalize_for_environment("/Users/test", "macos")
        assert result == "/Users/test"
    
    def test_round_trip_conversion(self):
        """Test round-trip conversion Windows -> WSL -> Windows."""
        original = "C:\\Projects\\MyApp"
        wsl = PathConverter.to_wsl_path(original)
        back = PathConverter.to_windows_path(wsl)
        assert back == original
    
    def test_case_insensitive_drive(self):
        """Test that drive letters are handled case-insensitively."""
        result1 = PathConverter.to_wsl_path("c:\\Projects")
        result2 = PathConverter.to_wsl_path("C:\\Projects")
        assert result1 == result2 == "/mnt/c/Projects"
    
    def test_empty_path(self):
        """Test empty path handling."""
        assert PathConverter.to_wsl_path("") == ""
        assert PathConverter.to_windows_path("") == ""
    
    def test_complex_path(self):
        """Test complex paths with multiple directories."""
        win_path = "C:\\Users\\Developer\\Projects\\AI-CLI\\src\\main.py"
        wsl_path = "/mnt/c/Users/Developer/Projects/AI-CLI/src/main.py"
        
        assert PathConverter.to_wsl_path(win_path) == wsl_path
        assert PathConverter.to_windows_path(wsl_path) == win_path
