"""Unit tests for configuration management."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from ai_cli.config import ConfigManager
from ai_cli.models import Config


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_load_existing_config(self, temp_dir, sample_config_dict):
        """Test loading existing configuration."""
        config_file = temp_dir / "config.json"
        config_file.write_text(json.dumps(sample_config_dict))
        
        with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
            manager = ConfigManager()
            config = manager.load()
            
            assert config is not None
            assert len(config.projects) > 0
    
    def test_save_config(self, temp_dir, sample_config):
        """Test saving configuration."""
        with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
            manager = ConfigManager()
            manager.save(sample_config)
            
            config_file = temp_dir / "config.json"
            assert config_file.exists()
    
    def test_create_default_config(self, temp_dir):
        """Test creating default configuration."""
        with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
            manager = ConfigManager()
            config = manager.create_default()
            
            assert config is not None
            assert isinstance(config, Config)
    
    def test_migrate_legacy_config(self, temp_dir, legacy_config_dict):
        """Test migrating legacy flat configuration."""
        config_file = temp_dir / "config.json"
        config_file.write_text(json.dumps(legacy_config_dict))
        
        with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
            manager = ConfigManager()
            config = manager.migrate_legacy(legacy_config_dict)
            
            assert config is not None
            # Verify tree structure
            assert len(config.projects) > 0
    
    def test_load_config_with_bom(self, temp_dir, sample_config_dict):
        """Test loading configuration file with UTF-8 BOM."""
        config_file = temp_dir / "config.json"
        # Write with BOM
        config_file.write_bytes(b'\xef\xbb\xbf' + json.dumps(sample_config_dict).encode('utf-8'))
        
        with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
            manager = ConfigManager()
            config = manager.load()
            
            assert config is not None
            assert len(config.projects) > 0
