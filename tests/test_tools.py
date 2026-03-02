"""Unit tests for tool detection."""

import pytest
from unittest.mock import patch, AsyncMock
from ai_cli.core.tools import WindowsToolDetector, LinuxToolDetector, MacOSToolDetector


class TestToolDetection:
    """Test tool detection across platforms."""
    
    @pytest.mark.asyncio
    async def test_windows_native_detection(self):
        """Test Windows native tool detection."""
        with patch('shutil.which', return_value='C:\\Program Files\\Git\\bin\\git.exe'):
            detector = WindowsToolDetector()
            result = await detector.detect_tool('git')
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_wsl_tool_detection(self):
        """Test WSL tool detection from Windows."""
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'/usr/bin/git', b'')
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            detector = WindowsToolDetector()
            result = await detector.detect_wsl_tool('git')
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_linux_tool_detection(self):
        """Test Linux tool detection."""
        with patch('shutil.which', return_value='/usr/bin/git'):
            detector = LinuxToolDetector()
            result = await detector.detect_tool('git')
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_macos_tool_detection(self):
        """Test macOS tool detection."""
        with patch('shutil.which', return_value='/usr/local/bin/git'):
            detector = MacOSToolDetector()
            result = await detector.detect_tool('git')
            
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_tool_not_found(self):
        """Test tool not found scenario."""
        with patch('shutil.which', return_value=None):
            detector = LinuxToolDetector()
            result = await detector.detect_tool('nonexistent-tool')
            
            assert result is None
