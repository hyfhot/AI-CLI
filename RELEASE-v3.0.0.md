# AI-CLI v3.0.0 - Python Edition 🎉

> 🚀 **Complete rewrite in Python with enhanced features and better cross-platform support**

AI-CLI v3.0.0 marks a major milestone - a complete rewrite from PowerShell to Python, bringing modern async architecture, improved performance, and enhanced user experience.

## 🌟 What's New

### 🏗️ Complete Rewrite
- **Python 3.8+**: Modern, maintainable codebase
- **Async/Await**: Parallel tool detection for better performance
- **Rich Library**: Beautiful terminal UI with colors and formatting
- **Comprehensive Tests**: 80%+ test coverage with pytest

### ⚡ Performance Improvements
- **Async Detection**: Tools detected in parallel (5-10x faster)
- **Smart Caching**: Config-based cache with no time expiry
- **Background Detection**: Non-blocking startup
- **Instant Refresh**: Cache updates only when needed

### 🎨 Enhanced User Experience
- **Modern UI**: Powered by Rich library with smooth animations
- **Better Feedback**: Real-time progress indicators
- **Cleaner Navigation**: Improved keyboard shortcuts
- **Error Handling**: Better error messages and recovery

### 🌍 Improved Internationalization
- **Complete Translations**: All UI strings properly translated
- **4 Languages**: English, Chinese (中文), Japanese (日本語), German (Deutsch)
- **Auto-Detection**: Automatically selects system language
- **Easy Extension**: Simple to add new languages

### 🔧 Better Tool Management
- **One-Click Install**: Press `I` to install missing tools
- **Smart Detection**: Platform-specific detection logic
- **Cache Management**: Press `R` to refresh tool list
- **Environment Support**: Windows, WSL, Linux, macOS

## 📦 Installation

### Quick Install

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Install with pip
pip install -e ".[dev]"

# Initialize configuration
ai-cli --init

# Run
ai-cli
```

### Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for worktree support)

## ✨ Key Features

### 🛠️ Tool Detection & Management
- **Async Parallel Detection**: Detect all tools simultaneously
- **Smart Caching**: Results cached in config file
- **Background Detection**: Non-blocking startup
- **One-Click Install**: Install missing tools with `I` key
- **Manual Refresh**: Press `R` to re-detect tools
- **Multi-Environment**: Windows, WSL, Linux, macOS support

### 📁 Project Management
- **Tree Structure**: Organize projects in folders
- **Git Worktree**: Auto-detect and select worktrees
- **Environment Variables**: Per-project env var injection
- **Path Normalization**: Automatic Windows ↔ WSL path conversion
- **CRUD Operations**: Create, delete projects and folders

### 🎨 User Interface
- **Rich Terminal UI**: Beautiful colors and formatting
- **Keyboard Navigation**: Full keyboard shortcut support
- **Live Updates**: Real-time progress indicators
- **Smooth Animations**: No screen flicker
- **Breadcrumb Navigation**: Always know where you are

### 🌐 Internationalization
- **English**: Full support
- **中文 (Chinese)**: Complete translation
- **日本語 (Japanese)**: Complete translation
- **Deutsch (German)**: Complete translation
- **Auto-Detection**: Based on system locale
- **CLI Override**: `ai-cli --lang zh`

### 🔌 Platform Support
- **Windows**: Native + WSL integration
- **Linux**: All major distributions
- **macOS**: Terminal.app + iTerm2
- **WSL**: Deep integration with path conversion

## 🎯 Supported Tools

- **Kiro CLI** - AI coding assistant
- **Claude Code** - Anthropic's coding assistant
- **Cursor Agent** - AI-powered code editor
- **OpenAI Codex** - OpenAI's coding model
- **Kimi CLI** - Moonshot AI assistant
- **Gemini CLI** - Google's AI assistant
- **OpenCode** - Open-source AI coding tool
- **Aider** - AI pair programming
- **And more...** - Easy to add custom tools

## 📖 Usage

### Command Line Options

```bash
ai-cli                    # Start interactive interface
ai-cli --init             # Initialize configuration
ai-cli --config           # Edit configuration file
ai-cli --lang zh          # Start with Chinese language
ai-cli --version          # Show version
ai-cli --help             # Show help
```

### Keyboard Shortcuts

#### Project Selection
- `↑` / `↓` - Navigate
- `Enter` - Select project / Enter folder
- `Esc` - Go back to parent folder
- `N` - Create new project or folder
- `D` - Delete selected item
- `Q` - Quit application

#### Tool Selection
- `↑` / `↓` - Navigate
- `Enter` - Launch tool (new window)
- `T` - Launch tool (new tab)
- `I` - Install missing tools
- `R` - Refresh tool list
- `Esc` - Return to project selection
- `Q` - Quit application

## 🔧 Configuration

### Configuration File Location

- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### Example Configuration

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

## 📚 Documentation

- [README (English)](README.md)
- [README (中文)](README.zh.md)
- [README (日本語)](README.ja.md)
- [README (Deutsch)](README.de.md)
- [Installation Guide](docs/INSTALL-GUIDE.md)
- [Tool Configuration](docs/TOOLS.md)
- [Changelog](CHANGELOG.md)

## 🔄 Migration from v2.0.0

### What's Changed

1. **Language**: PowerShell → Python
2. **Installation**: Now uses pip instead of PowerShell script
3. **Configuration**: Format remains compatible (minor additions)
4. **Performance**: Significantly faster with async detection
5. **UI**: More polished with Rich library

### Migration Steps

1. **Install Python 3.8+** if not already installed
2. **Backup your config**: Copy your existing `config.json`
3. **Install v3.0.0**: Run `pip install -e .` in the repo
4. **Copy config**: Place your config in the new location
5. **Run**: Execute `ai-cli` to start

### Config Compatibility

Your v2.0.0 config will work with v3.0.0! The new version adds optional cache fields but maintains backward compatibility.

**New optional fields** (auto-populated on first run):
```json
{
  "tools": [
    {
      "name": "kiro-cli",
      "win_available": true,
      "wsl_available": true,
      "linux_available": false,
      "macos_available": false
    }
  ]
}
```

## 🐛 Bug Fixes

- ✅ Fixed first-run experience with empty cache
- ✅ Fixed all hardcoded English strings in UI
- ✅ Fixed environment variable display (now shows project env vars)
- ✅ Fixed config save after tool detection
- ✅ Fixed cache empty check logic
- ✅ Fixed duplicate environment labels in tool list
- ✅ Fixed tool selection UI text (Launch vs New Window)

## 🏗️ Technical Details

### Architecture

```
ai_cli/
├── app.py              # Main application logic
├── cli.py              # CLI entry point
├── config.py           # Configuration management
├── models.py           # Data models
├── utils.py            # Path utilities
├── core/               # Core functionality
│   ├── tools.py        # Tool detection
│   ├── projects.py     # Project management
│   ├── git.py          # Git integration
│   └── installer.py    # Tool installation
├── ui/                 # User interface
│   ├── menu.py         # Menu rendering
│   ├── input.py        # Keyboard input
│   └── theme.py        # Theme configuration
├── platform/           # Platform adapters
│   ├── windows.py      # Windows support
│   ├── linux.py        # Linux support
│   └── macos.py        # macOS support
└── i18n/               # Internationalization
    └── manager.py      # Language manager
```

### Dependencies

- **rich**: Terminal UI rendering
- **prompt-toolkit**: Keyboard input handling
- **click**: CLI framework
- **platformdirs**: Cross-platform paths
- **pytest**: Testing framework (dev)

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_cli

# Run specific test
pytest tests/test_models.py
```

## 🤝 Contributing

We welcome contributions! Please see:
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Development Setup](README.md#development-guide)

## 📊 Project Stats

- **Lines of Code**: ~10,000+ (Python)
- **Test Coverage**: 80%+
- **Languages**: 4 (EN, ZH, JA, DE)
- **Platforms**: 4 (Windows, WSL, Linux, macOS)
- **Supported Tools**: 14+

## 🙏 Acknowledgments

- **PowerShell Edition**: Thanks to all v2.0 users and contributors
- **Rich Library**: For the beautiful terminal UI
- **Python Community**: For excellent async/await support
- **All Contributors**: Your feedback made this possible!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/hyfhot/AI-CLI
- **Issues**: https://github.com/hyfhot/AI-CLI/issues
- **Discussions**: https://github.com/hyfhot/AI-CLI/discussions
- **v2.0.0 (PowerShell)**: https://github.com/hyfhot/AI-CLI/releases/tag/v2.0.0

---

**🎉 Enjoy AI-CLI v3.0.0! Happy coding with AI assistants!**
