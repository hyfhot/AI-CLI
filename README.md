# AI-CLI (Python Edition)

> 🌐 **English** | [中文](README.zh.md)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** is a cross-platform terminal launcher for managing multiple AI coding assistants. Seamlessly switch between tools like Kiro CLI, Claude Code, Cursor Agent, and more.

## ✨ Features

- 🌍 **Cross-Platform**: Windows, Linux, macOS
- 🔄 **WSL Support**: Seamless Windows ↔ WSL environment switching
- 📁 **Tree Structure**: Organize projects in folders
- ⚡ **Async Detection**: Fast tool detection with async/await
- 🎨 **Rich UI**: Beautiful terminal interface with keyboard shortcuts
- 🔧 **Auto Path Conversion**: Automatic Windows ↔ WSL path translation
- 🌳 **Git Worktree**: Detect and manage Git worktrees
- 🎯 **Environment Variables**: Project-specific env var injection
- 🛠️ **Tool Installation**: Press I key to install uninstalled tools
- 🔄 **Manual Refresh**: Press R key to refresh tool list
- 🌐 **Multi-language**: Support for English, Chinese, Japanese, German
- 🔗 **Tool URLs**: Display tool website URLs in selection menu

## 🚀 Quick Start

### Installation

```bash
# Using installation script (recommended)
# Windows:
powershell -ExecutionPolicy Bypass -File install.ps1

# Linux/macOS:
bash install.sh

# Or manual installation:
pip install -e ".[dev]"
```

### Initialize Configuration

```bash
ai-cli --init
```

### Run

```bash
ai-cli
```

## 📖 Usage

### Commands

```bash
ai-cli              # Start interactive interface
ai-cli --init       # Initialize configuration
ai-cli --config     # Edit configuration file
ai-cli --uninstall  # Uninstall AI-CLI
ai-cli --version    # Show version
ai-cli --help       # Show help
```

### Keyboard Shortcuts

**Project Selection**:
- `↑↓` - Navigate
- `Enter` - Select project / Enter folder
- `Esc` - Go back
- `N` - New project
- `D` - Delete project
- `Q` - Quit

**Tool Selection**:
- `↑↓` - Navigate
- `Enter` - Launch tool (new window)
- `Ctrl+Enter` - Launch tool (new tab)
- `I` - Install tool
- `R` - Refresh tools
- `Esc` - Go back
- `Q` - Quit

## 🔧 Configuration

Configuration file location:
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

Example configuration:

```json
{
  "projects": [
    {
      "type": "folder",
      "name": "My Projects",
      "children": [
        {
          "type": "project",
          "name": "Web App",
          "path": "/path/to/project",
          "env": {
            "API_KEY": "your-key"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
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
```

## 🏗️ Architecture

```
ai_cli/
├── models.py          # Data models
├── config.py          # Configuration management
├── utils.py           # Path conversion utilities
├── app.py             # Main application
├── cli.py             # CLI entry point
├── core/
│   ├── tools.py       # Tool detection
│   ├── projects.py    # Project management
│   └── git.py         # Git integration
├── ui/
│   ├── theme.py       # Theme configuration
│   ├── menu.py        # Menu rendering
│   └── input.py       # Keyboard input
└── platform/
    ├── base.py        # Abstract adapter
    ├── windows.py     # Windows adapter
    ├── linux.py       # Linux adapter
    ├── macos.py       # macOS adapter
    └── factory.py     # Platform factory
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=ai_cli

# Run specific test
pytest tests/test_models.py
```

## 📝 Development

### Requirements

- Python 3.8+
- Dependencies: rich, prompt-toolkit, click, platformdirs

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Create worktree for Python version
git worktree add ../ai-cli-multi-platform python-migration

# Install dependencies
cd ../ai-cli-multi-platform
pip install -e ".[dev]"

# Run tests
pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Original Project**: [AI-CLI (PowerShell)](https://github.com/hyfhot/AI-CLI)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Terminal UI
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Keyboard input
- [Click](https://github.com/pallets/click) - CLI framework

---

**Made with ❤️ by AI-CLI Team**
