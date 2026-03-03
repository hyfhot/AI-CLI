# AI-CLI v2.0.0 - PowerShell Edition (Final Release)

> 🎉 **Final stable release of PowerShell Edition before Python migration**

AI-CLI PowerShell Edition has served the community well. This is the last stable release before we transition to the Python Edition (v3.0.0) for better cross-platform support and modern features.

## 🌟 Highlights

- ✅ **Stable & Production-Ready**: Battle-tested PowerShell implementation
- 🌍 **Cross-Platform**: Windows, WSL, Linux, macOS support
- 🛠️ **Tool Management**: Detect and launch multiple AI coding assistants
- 📁 **Project Organization**: Tree-structured project management
- 🌐 **Multi-Language**: English, Chinese, Japanese, German

## 📦 Installation

### Windows (PowerShell)

```powershell
# Download and run installer
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Linux/macOS

```bash
# Clone repository
git clone -b AI-CLI-2.0 https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Run directly
./ai-cli.ps1
```

## ✨ Features

### Tool Detection & Management
- Automatic detection of installed AI tools
- Support for multiple environments (Windows, WSL, Linux, macOS)
- One-click tool installation
- Manual refresh capability

### Project Management
- Tree-structured project organization
- Folder support for grouping projects
- Git worktree integration
- Per-project environment variables

### User Interface
- Interactive terminal UI
- Keyboard navigation
- Real-time tool detection feedback
- Multi-language support

### Supported Tools
- Kiro CLI
- Claude Code
- Cursor Agent
- OpenAI Codex
- Kimi CLI
- Gemini CLI
- OpenCode
- Aider
- And more...

## 🔧 Configuration

Configuration file location:
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux/macOS**: `~/.config/ai-cli/config.json`

Example configuration:
```json
{
  "projects": [
    {
      "type": "project",
      "name": "My Project",
      "path": "/path/to/project",
      "env": {
        "API_KEY": "your-key"
      }
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    }
  ]
}
```

## 📚 Documentation

- [Installation Guide](docs/INSTALL-GUIDE.md)
- [Tool Configuration](docs/TOOLS.md)
- [README (English)](README.md)
- [README (中文)](README.zh.md)
- [README (日本語)](README.ja.md)
- [README (Deutsch)](README.de.md)

## 🔄 Migration to v3.0.0

If you want to upgrade to the new Python Edition (v3.0.0), please see:
- [Migration Guide](https://github.com/hyfhot/AI-CLI/releases/tag/v3.0.0)
- Python 3.8+ required
- Configuration format remains compatible

## 🐛 Known Issues

- PowerShell performance limitations on large tool lists
- Limited async capabilities compared to Python version
- Some terminal emulators may have compatibility issues

## 💡 Why v2.0.0?

This release is tagged as v2.0.0 to represent the mature, stable state of the PowerShell Edition. The previous versions (v2.3.x) were incremental improvements, and this consolidates all those improvements into a final stable release.

## 🙏 Acknowledgments

Thank you to all contributors and users who have helped make AI-CLI PowerShell Edition a success. We're excited to bring you even better features in the Python Edition (v3.0.0)!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**For the latest features and improvements, check out [v3.0.0 - Python Edition](https://github.com/hyfhot/AI-CLI/releases/tag/v3.0.0)!**
