# AI-CLI (Python Edition)

> 🌐 **English** | [中文](README.zh.md) | [日本語](README.ja.md)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** is a cross-platform terminal launcher for managing multiple AI coding assistants. Seamlessly switch between tools like Kiro CLI, Claude Code, Cursor Agent, and more.

## ✨ Core Features

### 🌍 Cross-Platform Support
- **Windows**: Native support + WSL integration
- **Linux**: Full support for all major distributions
- **macOS**: Support for Terminal.app and iTerm2

### 🔄 Deep WSL Integration
- Automatic WSL environment detection
- Automatic Windows ↔ WSL path conversion
- Launch WSL tools from Windows
- Launch Windows tools from WSL

### 📁 Project Management
- **Tree Structure**: Organize projects in folders
- **Git Worktree**: Auto-detect and select Git worktrees
- **Environment Variables**: Configure per-project environment variables
- **Path Normalization**: Automatic handling of different platform path formats

### ⚡ Tool Detection & Management
- **Async Detection**: Parallel tool detection using async/await
- **Smart Caching**: Background detection with result caching
- **One-Click Install**: Press `I` to install missing tools
- **Manual Refresh**: Press `R` to refresh tool list
- **Environment Recognition**: Auto-detect Windows, WSL, Linux, macOS environments

### 🎨 User Interface
- **Rich UI**: Beautiful terminal interface powered by Rich library
- **Keyboard Navigation**: Full keyboard shortcut support
- **Real-time Feedback**: Display tool detection and installation progress
- **Theme Support**: Customizable color themes

### 🌐 Internationalization
- **Multi-language**: English, Chinese, Japanese, German
- **Auto-detection**: Automatically select based on system language
- **Configurable**: Manually specify language in config file

## 🚀 Quick Start

### Installation

#### Using Installation Script (Recommended)

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

#### Manual Installation

```bash
# Clone repository
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# If using Git worktree
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# Install dependencies
pip install -e ".[dev]"
```

### Initialize Configuration

```bash
ai-cli --init
```

This creates a default configuration file with common AI tool configurations.

### Run

```bash
ai-cli
```

## 📖 Usage

### Command Line Options

```bash
ai-cli              # Start interactive interface
ai-cli --init       # Initialize configuration file
ai-cli --config     # Edit configuration file
ai-cli --uninstall  # Uninstall AI-CLI
ai-cli --version    # Show version information
ai-cli --help       # Show help information
```

### Keyboard Shortcuts

#### Project Selection Screen

| Key | Function |
|-----|----------|
| `↑` / `↓` | Navigate up/down |
| `Enter` | Select project / Enter folder |
| `Esc` | Go back to parent folder |
| `N` | Create new project or folder |
| `D` | Delete selected project or folder |
| `Q` | Quit application |

#### Tool Selection Screen

| Key | Function |
|-----|----------|
| `↑` / `↓` | Navigate up/down |
| `Enter` | Launch tool (new window) |
| `Ctrl+Enter` | Launch tool (new tab) |
| `I` | Install missing tools |
| `R` | Refresh tool list |
| `Esc` | Return to project selection |
| `Q` | Quit application |

### Workflow

1. **Launch**: Run `ai-cli`
2. **Select Project**: Use arrow keys to select a project, press `Enter` to confirm
3. **Select Tool**: Choose the AI tool you want to use
4. **Start Working**: Tool launches in a new window or tab

## 🔧 Configuration Guide

### Configuration File Location

- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### Configuration File Structure

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
            "API_KEY": "your-api-key",
            "DEBUG": "true"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "windowsInstall": "winget install kiro-cli",
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

### Project Configuration

#### Project Types

**Folder**:
```json
{
  "type": "folder",
  "name": "Project Group Name",
  "children": [...]
}
```

**Project**:
```json
{
  "type": "project",
  "name": "Project Name",
  "path": "/absolute/path/to/project",
  "env": {
    "KEY": "value"
  }
}
```

#### Environment Variables

Configure independent environment variables for each project:

```json
{
  "type": "project",
  "name": "API Project",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "API_BASE_URL": "https://api.example.com",
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

### Tool Configuration

#### Required Fields

- `name`: Tool command name (used for detection)
- `displayName`: Display name
- `checkCommand`: Command to check if tool is installed

#### Installation Commands (by Platform)

- `windowsInstall`: Windows native installation command
- `wslInstall`: WSL environment installation command
- `linuxInstall`: Linux installation command
- `macosInstall`: macOS installation command

#### Optional Fields

- `url`: Tool's official website (displayed in tool list)

#### Example Configuration

```json
{
  "name": "cursor",
  "displayName": "Cursor Agent",
  "windowsInstall": "winget install Cursor",
  "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
  "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
  "macosInstall": "brew install --cask cursor",
  "checkCommand": "cursor --version",
  "url": "https://cursor.sh"
}
```

### Settings Options

#### language

- `auto`: Auto-detect system language (default)
- `en`: English
- `zh`: Chinese
- `ja`: Japanese
- `de`: German

#### terminalEmulator

- `default`: Use system default terminal (default)
- `wt`: Windows Terminal (Windows only)
- `iterm`: iTerm2 (macOS only)
- `gnome-terminal`: GNOME Terminal (Linux only)
- `konsole`: Konsole (Linux only)

#### theme

- `default`: Default dark theme
- More themes coming in future versions

## 🏗️ Project Architecture

### Directory Structure

```
ai_cli/
├── __init__.py        # Package initialization
├── cli.py             # CLI entry point
├── app.py             # Main application logic
├── models.py          # Data models
├── config.py          # Configuration management
├── utils.py           # Path conversion utilities
├── core/              # Core functionality modules
│   ├── __init__.py
│   ├── tools.py       # Tool detection
│   ├── projects.py    # Project management
│   ├── git.py         # Git integration
│   └── installer.py   # Tool installation
├── ui/                # User interface modules
│   ├── __init__.py
│   ├── theme.py       # Theme configuration
│   ├── menu.py        # Menu rendering
│   └── input.py       # Keyboard input handling
├── platform/          # Platform adapter modules
│   ├── __init__.py
│   ├── base.py        # Abstract base class
│   ├── windows.py     # Windows adapter
│   ├── linux.py       # Linux adapter
│   ├── macos.py       # macOS adapter
│   └── factory.py     # Platform factory
└── i18n/              # Internationalization modules
    ├── __init__.py
    └── manager.py     # Language manager
```

### Core Module Descriptions

#### models.py - Data Models

Defines all data structures:
- `Config`: Main configuration object
- `Settings`: Settings options
- `ProjectNode`: Project node (supports tree structure)
- `Tool`: Tool object
- `ToolConfig`: Tool configuration
- `ToolEnvironment`: Tool runtime environment enum

#### config.py - Configuration Management

- Cross-platform config file path handling
- Config file loading and saving
- Migration from legacy config versions
- Default config creation

#### app.py - Main Application

- Application main loop
- Project selection logic
- Tool selection logic
- Tool launch logic
- Project and folder CRUD operations

#### core/tools.py - Tool Detection

- Async parallel tool detection
- Platform-specific detection logic
- Windows native tool detection
- WSL tool detection
- Tool cache management

#### core/git.py - Git Integration

- Detect Git worktrees
- Display branch status
- Interactive worktree selection

#### core/installer.py - Tool Installation

- Select installation command by platform
- Execute installation process
- Post-installation path updates
- Find installed tools

#### ui/menu.py - Menu Rendering

- Render project tree
- Render tool list
- Display breadcrumb navigation
- Clear screen and refresh

#### ui/input.py - Keyboard Input

- Cross-platform keyboard input handling
- Different implementations for Windows and Unix
- Text input support
- Special key handling

#### platform/ - Platform Adapters

- Abstract platform interface
- Windows-specific implementation (Windows Terminal support)
- Linux-specific implementation (multiple terminal support)
- macOS-specific implementation (iTerm2 support)
- Platform factory pattern

#### i18n/manager.py - Internationalization

- Language detection
- Translation dictionary management
- Text retrieval interface

## 🔍 Advanced Features

### Git Worktree Support

When a project path is a Git worktree, AI-CLI will:

1. Auto-detect all worktrees
2. Display branch and status for each worktree
3. Allow selection of the worktree to use
4. Show ahead/behind commit counts for branches

### WSL Path Conversion

AI-CLI automatically handles path conversion between Windows and WSL:

- Windows path: `C:\Users\username\project`
- WSL path: `/mnt/c/Users/username/project`

Conversion is bidirectional, supporting:
- Launch WSL tools from Windows
- Launch Windows tools from WSL

### Async Tool Detection

Tool detection uses async parallel processing:

1. **On Startup**: Quickly display interface, detect tools in background
2. **Caching**: Detection results are cached to avoid repeated checks
3. **Refresh**: Press `R` to clear cache and re-detect

### Environment Variable Injection

Environment variables configured for each project are injected when launching tools:

```json
{
  "type": "project",
  "name": "API Project",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "DEBUG": "true"
  }
}
```

When launching a tool, these environment variables are added to the tool's runtime environment.

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::TestConfig::test_from_dict

# Show verbose output
pytest -v

# Show print output
pytest -s
```

### Test Coverage

```bash
# Run tests with coverage report
pytest --cov=ai_cli

# Generate HTML coverage report
pytest --cov=ai_cli --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test File Descriptions

- `test_models.py`: Data model tests
- `test_config.py`: Configuration management tests
- `test_utils.py`: Path conversion tests
- `test_platform.py`: Platform adapter tests
- `test_git.py`: Git integration tests
- `test_tools.py`: Tool detection tests
- `test_projects.py`: Project management tests
- `test_ui.py`: UI component tests
- `test_app.py`: Application integration tests
- `test_cli.py`: CLI entry point tests

## 📝 Development Guide

### Requirements

- **Python**: 3.8 or higher
- **Dependencies**:
  - `rich`: Terminal UI rendering
  - `prompt-toolkit`: Keyboard input handling
  - `click`: CLI framework
  - `platformdirs`: Cross-platform paths

### Development Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 2. Create Python version worktree (if needed)
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 3. Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Install development dependencies
pip install -e ".[dev]"

# 5. Run tests to verify environment
pytest
```

### Code Style

Project follows PEP 8 style guide:

```bash
# Install code checking tools
pip install flake8 black mypy

# Run code checks
flake8 ai_cli tests

# Auto-format code
black ai_cli tests

# Type checking
mypy ai_cli
```

### Adding New Tools

Add new tool configuration in `config.json`:

```json
{
  "name": "new-tool",
  "displayName": "New Tool",
  "windowsInstall": "winget install new-tool",
  "wslInstall": "curl -fsSL https://example.com/install | bash",
  "linuxInstall": "curl -fsSL https://example.com/install | bash",
  "macosInstall": "brew install new-tool",
  "checkCommand": "new-tool --version",
  "url": "https://example.com"
}
```

### Adding New Languages

Add translations in `ai_cli/i18n/manager.py`:

```python
translations = {
    'new_lang': {
        'app_title': 'AI-CLI',
        'select_project': 'Select Project',
        # ... other translations
    }
}
```

### Debugging Tips

```bash
# Enable debug mode
ai-cli --debug

# Use Python debugger
python -m pdb -m ai_cli.cli

# View detailed logs
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🐛 Troubleshooting

### Windows Issues

**Issue**: Cannot detect Windows Terminal
```bash
# Solution: Ensure Windows Terminal is installed
winget install Microsoft.WindowsTerminal
```

**Issue**: WSL tool detection fails
```bash
# Solution: Ensure WSL is enabled
wsl --install
```

### Linux Issues

**Issue**: Terminal emulator detection fails
```bash
# Solution: Install supported terminal
sudo apt install gnome-terminal  # Ubuntu/Debian
sudo dnf install gnome-terminal  # Fedora
```

### macOS Issues

**Issue**: iTerm2 not detected
```bash
# Solution: Ensure iTerm2 is installed
brew install --cask iterm2
```

### General Issues

**Issue**: Config file corrupted
```bash
# Solution: Reinitialize configuration
ai-cli --init
```

**Issue**: Tool detection cache stale
```bash
# Solution: Press R key in tool selection screen to refresh
```

## 🤝 Contributing

We welcome all forms of contribution!

### Ways to Contribute

1. **Report Bugs**: Submit issues on [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)
2. **Feature Requests**: Propose new feature ideas
3. **Code Contributions**: Submit Pull Requests
4. **Documentation**: Improve docs and examples
5. **Translations**: Add new language support

### Pull Request Process

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Fix bug
docs: Documentation update
style: Code formatting
refactor: Code refactoring
test: Test related
chore: Build/toolchain updates
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- **Original Project**: [AI-CLI (PowerShell Edition)](https://github.com/hyfhot/AI-CLI)
- **Documentation**: [docs/](docs/)
- **Issue Tracker**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## 🙏 Acknowledgments

Thanks to these open source projects:

- [Rich](https://github.com/Textualize/rich) - Powerful terminal UI library
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive command-line tools
- [Click](https://github.com/pallets/click) - Python CLI framework
- [platformdirs](https://github.com/platformdirs/platformdirs) - Cross-platform directory paths

## 📊 Project Status

- **Version**: Beta
- **Python Version**: 3.8+
- **Platforms**: Windows, Linux, macOS
- **Maintenance**: Actively developed

## 🗺️ Roadmap

- [ ] Support more AI tools
- [ ] Plugin system
- [ ] Config file validation
- [ ] More theme options
- [ ] Tool usage statistics
- [ ] Cloud config sync
- [ ] Project template support

---

**Made with ❤️ by AI-CLI Team**
