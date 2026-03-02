"""Configuration management for AI-CLI."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from .models import Config, ProjectNode, ToolConfig, Settings


class ConfigManager:
    """Manages configuration loading, saving, and migration."""
    
    def __init__(self):
        self.config_dir = self.get_config_dir()
        self.config_file = self.config_dir / "config.json"
    
    def get_config_dir(self) -> Path:
        """Get cross-platform configuration directory."""
        if sys.platform == 'win32':
            import os
            base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            config_dir = base / 'AI-CLI'
        elif sys.platform == 'darwin':
            config_dir = Path.home() / 'Library' / 'Application Support' / 'ai-cli'
        else:
            import os
            base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
            config_dir = base / 'ai-cli'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def load(self) -> Config:
        """Load configuration from file."""
        try:
            if not self.config_file.exists():
                return self.create_default()
            
            # Use utf-8-sig to handle BOM
            with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            # Check if legacy flat config needs migration
            if self._needs_migration(data):
                data = self.migrate_legacy(data)
                config = Config.from_dict(data)
                self.save(config)
                return config
            
            return Config.from_dict(data)
        
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to load config: {e}")
        except FileNotFoundError:
            return self.create_default()
    
    def save(self, config: Config) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
        except (OSError, TypeError) as e:
            raise RuntimeError(f"Failed to save config: {e}")
    
    def create_default(self) -> Config:
        """Create default configuration."""
        default_config = Config(
            projects=[],
            tools=[
                ToolConfig(
                    name="kiro-cli",
                    display_name="Kiro CLI",
                    win_install=None,
                    wsl_install="curl -fsSL https://cli.kiro.dev/install | bash",
                    linux_install="curl -fsSL https://cli.kiro.dev/install | bash",
                    macos_install="brew install kiro-cli",
                    check_command="kiro-cli --version",
                    url="https://kiro.dev/cli/"
                ),
                ToolConfig(
                    name="claude",
                    display_name="Claude Code",
                    win_install="npm install -g @anthropic-ai/claude-code",
                    wsl_install="npm install -g @anthropic-ai/claude-code",
                    linux_install="npm install -g @anthropic-ai/claude-code",
                    macos_install="npm install -g @anthropic-ai/claude-code",
                    check_command="claude --version",
                    url="https://www.npmjs.com/package/@anthropic-ai/claude-code"
                ),
                ToolConfig(
                    name="codex",
                    display_name="OpenAI Codex",
                    win_install="npm install -g @openai/codex",
                    wsl_install="npm install -g @openai/codex",
                    linux_install="npm install -g @openai/codex",
                    macos_install="npm install -g @openai/codex",
                    check_command="codex --version",
                    url="https://www.npmjs.com/package/@openai/codex"
                ),
                ToolConfig(
                    name="kimi",
                    display_name="Kimi CLI",
                    win_install="pip install kimi-cli",
                    wsl_install="uv tool install --python 3.13 kimi-cli",
                    linux_install="pip install kimi-cli",
                    macos_install="pip install kimi-cli",
                    check_command="kimi --version",
                    url="https://pypi.org/project/kimi-cli/"
                ),
                ToolConfig(
                    name="gemini",
                    display_name="Gemini CLI",
                    win_install="npm install -g @google/gemini-cli",
                    wsl_install="npm install -g @google/gemini-cli",
                    linux_install="npm install -g @google/gemini-cli",
                    macos_install="npm install -g @google/gemini-cli",
                    check_command="gemini --version",
                    url="https://www.npmjs.com/package/@google/gemini-cli"
                ),
                ToolConfig(
                    name="cursor-agent",
                    display_name="Cursor Agent",
                    win_install=None,
                    wsl_install="curl https://cursor.com/install -fsS | bash",
                    linux_install="curl https://cursor.com/install -fsS | bash",
                    macos_install="curl https://cursor.com/install -fsS | bash",
                    check_command="cursor-agent --version",
                    url="https://docs.cursor.com/en/cli/installation"
                ),
                ToolConfig(
                    name="opencode",
                    display_name="OpenCode",
                    win_install="curl -fsSL https://opencode.ai/install.ps1 | powershell",
                    wsl_install="curl -fsSL https://opencode.ai/install.sh | bash",
                    linux_install="curl -fsSL https://opencode.ai/install.sh | bash",
                    macos_install="curl -fsSL https://opencode.ai/install.sh | bash",
                    check_command="opencode --version",
                    url="https://opencode.ai/docs"
                ),
                ToolConfig(
                    name="aider",
                    display_name="Aider",
                    win_install="pip install aider-install; aider-install",
                    wsl_install="curl -LsSf https://aider.chat/install.sh | sh",
                    linux_install="curl -LsSf https://aider.chat/install.sh | sh",
                    macos_install="brew install aider",
                    check_command="aider --version",
                    url="https://aider.chat/docs/install"
                ),
            ],
            settings=Settings()
        )
        
        self.save(default_config)
        return default_config
    
    def _needs_migration(self, data: Dict[str, Any]) -> bool:
        """Check if configuration needs migration from flat to tree structure."""
        projects = data.get("projects", [])
        if not projects:
            return False
        
        # Check if any project lacks 'type' field (old format)
        return any("type" not in proj for proj in projects)
    
    def migrate_legacy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate legacy flat configuration to tree structure."""
        migrated_projects = []
        
        for proj in data.get("projects", []):
            if "type" not in proj:
                # Old format: convert to new format
                migrated_proj = {
                    "type": "project",
                    "name": proj["name"],
                    "path": proj.get("path"),
                }
                if "env" in proj:
                    migrated_proj["env"] = proj["env"]
                if "description" in proj:
                    migrated_proj["description"] = proj["description"]
                
                migrated_projects.append(migrated_proj)
            else:
                # Already new format
                migrated_projects.append(proj)
        
        return {
            "projects": migrated_projects,
            "tools": data.get("tools", []),
            "settings": data.get("settings", {})
        }
