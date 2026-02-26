🌐 [English](TOOLS.md) | [中文](TOOLS.zh.md) | [日本語](TOOLS.ja.md)

# AI CLI Tools Reference

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
- **Installation Command**:
  - WSL/Linux: `curl -fsSL https://cli.kiro.dev/install | bash`
  - Windows: Native installation not supported
- **Verification**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **Official Website**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **Developer**: Anthropic
- **Features**:
  - Agentic coding assistant
  - 100K+ context window
  - Multi-file operation support
  - Integrated Git workflows
  - MCP protocol support
- **Installation Command**:
  - Windows: `npm install -g @anthropic-ai/claude-code`
  - WSL/Linux: `npm install -g @anthropic-ai/claude-code`
- **Verification**: `claude --version`
- **Requirements**: Node.js 18+

---

### 3. OpenAI Codex CLI
- **Official Website**: https://www.npmjs.com/package/@openai/codex
- **Developer**: OpenAI
- **Features**:
  - Lightweight coding agent
  - Local execution, code not uploaded
  - Natural language command support
  - Open source project
- **Installation Command**:
  - Windows: `npm install -g @openai/codex`
  - WSL/Linux: `npm install -g @openai/codex`
- **Verification**: `codex --version`
- **Requirements**: Node.js 18+

---

### 4. Kimi CLI (Moonshot AI)
- **Official Website**: https://pypi.org/project/kimi-cli/
- **Developer**: Moonshot AI
- **Features**:
  - Terminal AI agent
  - Supports code read/write and command execution
  - Supports web search and scraping
  - Autonomous planning and action adjustment
- **Installation Command**:
  - Windows: `pip install kimi-cli`
  - WSL/Linux: `uv tool install --python 3.13 kimi-cli`
- **Verification**: `kimi --version`
- **Requirements**: Python 3.13+, uv (recommended)

---

### 5. Gemini CLI (Google)
- **Official Website**: https://www.npmjs.com/package/@google/gemini-cli
- **Developer**: Google
- **Features**:
  - Open source AI agent
  - 1M token context window
  - Multimodal AI capabilities
  - Free to use
- **Installation Command**:
  - Windows: `npm install -g @google/gemini-cli`
  - WSL/Linux: `npm install -g @google/gemini-cli`
- **Verification**: `gemini --version`
- **Requirements**: Node.js

---

### 6. Cursor Agent CLI
- **Official Website**: https://docs.cursor.com/en/cli/installation
- **Developer**: Cursor
- **Features**:
  - Terminal AI assistant
  - Supports remote servers and containers
  - Integrated GitHub Actions
  - Auto-update
- **Installation Command**:
  - WSL/Linux: `curl https://cursor.com/install -fsS | bash`
  - Windows: Native installation not supported
- **Verification**: `cursor-agent --version`
- **Usage**: `cursor-agent` or `agent chat "prompt"`

---

### 7. OpenCode
- **Official Website**: https://opencode.ai/docs
- **Developer**: Open Source Community
- **Features**:
  - Open source AI coding agent
  - Privacy-first, code not stored
  - Supports free built-in models
  - Can connect to external AI providers
  - Native terminal UI
- **Installation Command**:
  - Windows: `curl -fsSL https://opencode.ai/install.ps1 | powershell`
  - WSL/Linux: `curl -fsSL https://opencode.ai/install.sh | bash`
- **Verification**: `opencode --version`

---

### 8. Aider
- **Official Website**: https://aider.chat/docs/install
- **Developer**: Open Source Community
- **Features**:
  - Terminal AI programming assistant
  - Deep Git integration
  - Supports multiple LLMs (GPT-4, Claude, DeepSeek)
  - Automatic code testing
  - Budget-friendly ($0.007/file)
- **Installation Command**:
  - Windows: `pip install aider-install && aider-install`
  - WSL/Linux: `pip install aider-install && aider-install`
- **Verification**: `aider --version`
- **Requirements**: Python 3.9+, Git

---

## 📊 Tools Comparison

| Tool | Developer | Free | Open Source | Windows | WSL/Linux | Features |
|------|--------|------|------|---------|-----------|------|
| Kiro CLI | AWS | ✅ | ❌ | ❌ | ✅ | Specification-driven, AWS integration |
| Claude Code | Anthropic | ❌ | ❌ | ✅ | ✅ | 100K context, MCP |
| Codex CLI | OpenAI | ❌ | ✅ | ✅ | ✅ | Local execution, privacy |
| Kimi CLI | Moonshot | ❌ | ❌ | ✅ | ✅ | Web search, Chinese optimized |
| Gemini CLI | Google | ✅ | ✅ | ✅ | ✅ | 1M context, free |
| Cursor Agent | Cursor | ❌ | ❌ | ❌ | ✅ | CI/CD integration |
| OpenCode | Community | ✅ | ✅ | ✅ | ✅ | Privacy-first, multi-model |
| Aider | Community | ✅ | ✅ | ✅ | ✅ | Git integration, multi-LLM |

---

## 🔧 Prerequisites

### General Requirements
- **Git**: Most tools require Git for version control
- **Terminal**: Windows Terminal (recommended) or other modern terminals

### Node.js Tools (Claude, Codex, Gemini)
- Node.js 18+
- npm or pnpm

### Python Tools (Kimi, Aider)
- Python 3.9+ (Aider) or 3.13+ (Kimi)
- pip or uv

### Shell Script Tools (Kiro, Cursor, OpenCode)
- bash (WSL/Linux)
- curl

---

## 💡 Usage Recommendations

### Factors for Choosing Tools

1. **Budget**:
   - Free: Gemini CLI, OpenCode, Aider
   - Paid: Claude Code, Codex CLI, Kimi CLI, Cursor Agent

2. **Privacy**:
   - Local execution: Codex CLI, OpenCode
   - Cloud-based: Other tools

3. **Feature Requirements**:
   - AWS integration: Kiro CLI
   - Deep Git integration: Aider
   - Multi-model support: OpenCode
   - Large context: Gemini CLI (1M), Claude Code (100K)

4. **Language Preference**:
   - Chinese optimized: Kimi CLI
   - English: Other tools

---

## 🔄 Update Configuration

To add new tools or modify existing tool configurations, edit the `config.json` file:

```json
{
  "name": "tool-command",
  "displayName": "Tool Display Name",
  "winInstall": "Windows install command or null",
  "wslInstall": "WSL/Linux install command or null",
  "checkCommand": "tool-command --version",
  "url": "https://official-website.com"
}
```

---

## 📚 Reference Resources

- [Kiro CLI Documentation](https://kiro.dev/docs/cli/installation/)
- [Claude Code Guide](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [Codex CLI GitHub](https://github.com/openai/codex-cli)
- [Kimi CLI Documentation](https://moonshotai.github.io/kimi-cli/en/)
- [Gemini CLI Official Site](https://gemini-cli.click/)
- [Cursor CLI Documentation](https://docs.cursor.com/en/cli/)
- [OpenCode Documentation](https://opencode.ai/docs)
- [Aider Documentation](https://aider.chat/docs/)

---

*Last updated: 2026-02-26*
