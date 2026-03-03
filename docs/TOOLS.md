# AI CLI Tools Reference

> 🌐 **English** | [中文](TOOLS.zh.md) | [日本語](TOOLS.ja.md) | [Deutsch](TOOLS.de.md)

This document lists the mainstream AI programming tools supported by AI-CLI along with their installation and configuration information.

---

## 🤖 Supported Tools List

### 1. Kiro CLI (AWS)
- **Official Website**: https://kiro.dev/cli/
- **Developer**: Amazon Web Services
- **Features**:
  - Specification-driven development platform
  - Supports agentic workflows
  - Integrated AWS services
  - Supports Model Context Protocol (MCP)
- **Installation**:
  - **Linux/macOS/WSL**: `curl -fsSL https://cli.kiro.dev/install | bash`
  - **Windows**: `winget install kiro-cli` (if available)
- **Verification**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **Official Website**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **Developer**: Anthropic
- **Features**:
  - Agentic coding assistant
  - Natural language code generation
  - Context-aware suggestions
- **Installation**:
  - **All platforms**: `npm install -g @anthropic-ai/claude-code`
- **Verification**: `claude-code --version`

---

### 3. Cursor Agent
- **Official Website**: https://cursor.sh
- **Developer**: Cursor Team
- **Features**:
  - AI-powered code editor
  - Inline code suggestions
  - Chat-based coding assistance
- **Installation**:
  - **Windows**: `winget install Cursor`
  - **macOS**: `brew install --cask cursor`
  - **Linux**: Download from official website
- **Verification**: `cursor --version`

---

### 4. GitHub Copilot CLI
- **Official Website**: https://githubnext.com/projects/copilot-cli
- **Developer**: GitHub
- **Features**:
  - Command-line AI assistant
  - Shell command suggestions
  - Git workflow assistance
- **Installation**:
  - **All platforms**: `npm install -g @githubnext/github-copilot-cli`
- **Verification**: `github-copilot-cli --version`

---

### 5. Aider
- **Official Website**: https://aider.chat
- **Developer**: Aider Team
- **Features**:
  - AI pair programming in terminal
  - Git integration
  - Multiple LLM support
- **Installation**:
  - **All platforms**: `pip install aider-chat`
- **Verification**: `aider --version`

---

## 📝 Configuration Example

Add tools to your `config.json`:

```json
{
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
    },
    {
      "name": "cursor",
      "displayName": "Cursor Agent",
      "windowsInstall": "winget install Cursor",
      "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
      "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
      "macosInstall": "brew install --cask cursor",
      "checkCommand": "cursor --version",
      "url": "https://cursor.sh"
    },
    {
      "name": "aider",
      "displayName": "Aider",
      "windowsInstall": "pip install aider-chat",
      "wslInstall": "pip install aider-chat",
      "linuxInstall": "pip install aider-chat",
      "macosInstall": "pip install aider-chat",
      "checkCommand": "aider --version",
      "url": "https://aider.chat"
    }
  ]
}
```

---

## 🔧 Adding Custom Tools

To add a new tool:

1. **Find installation commands** for each platform
2. **Determine check command** to verify installation
3. **Add to config.json** following the format above

### Required Fields

- `name`: Command name (used for detection)
- `displayName`: Display name in UI
- `checkCommand`: Command to verify installation

### Platform-Specific Install Commands

- `windowsInstall`: Windows native installation
- `wslInstall`: WSL environment installation
- `linuxInstall`: Linux installation
- `macosInstall`: macOS installation

### Optional Fields

- `url`: Official website (displayed in tool list)

---

## 💡 Tips

1. **Use package managers** when possible (winget, brew, apt, etc.)
2. **Test check commands** to ensure they work correctly
3. **Keep URLs updated** for user reference
4. **Document prerequisites** if tools need specific dependencies

---

For more information, see the [main README](../README.md).
