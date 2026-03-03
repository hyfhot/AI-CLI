# AI CLI 工具参考

> 🌐 [English](TOOLS.md) | **中文** | [日本語](TOOLS.ja.md) | [Deutsch](TOOLS.de.md)

本文档列出了 AI-CLI 支持的主流 AI 编程工具及其安装和配置信息。

---

## 🤖 支持的工具列表

### 1. Kiro CLI (AWS)
- **官方网站**: https://kiro.dev/cli/
- **开发者**: Amazon Web Services
- **特性**:
  - 规范驱动的开发平台
  - 支持代理工作流
  - 集成 AWS 服务
  - 支持模型上下文协议 (MCP)
- **安装**:
  - **Linux/macOS/WSL**: `curl -fsSL https://cli.kiro.dev/install | bash`
  - **Windows**: `winget install kiro-cli`（如果可用）
- **验证**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **官方网站**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **开发者**: Anthropic
- **特性**:
  - 代理编码助手
  - 自然语言代码生成
  - 上下文感知建议
- **安装**:
  - **所有平台**: `npm install -g @anthropic-ai/claude-code`
- **验证**: `claude-code --version`

---

### 3. Cursor Agent
- **官方网站**: https://cursor.sh
- **开发者**: Cursor 团队
- **特性**:
  - AI 驱动的代码编辑器
  - 内联代码建议
  - 基于聊天的编码辅助
- **安装**:
  - **Windows**: `winget install Cursor`
  - **macOS**: `brew install --cask cursor`
  - **Linux**: 从官方网站下载
- **验证**: `cursor --version`

---

### 4. GitHub Copilot CLI
- **官方网站**: https://githubnext.com/projects/copilot-cli
- **开发者**: GitHub
- **特性**:
  - 命令行 AI 助手
  - Shell 命令建议
  - Git 工作流辅助
- **安装**:
  - **所有平台**: `npm install -g @githubnext/github-copilot-cli`
- **验证**: `github-copilot-cli --version`

---

### 5. Aider
- **官方网站**: https://aider.chat
- **开发者**: Aider 团队
- **特性**:
  - 终端中的 AI 结对编程
  - Git 集成
  - 支持多种 LLM
- **安装**:
  - **所有平台**: `pip install aider-chat`
- **验证**: `aider --version`

---

## 📝 配置示例

在 `config.json` 中添加工具：

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

## 🔧 添加自定义工具

添加新工具的步骤：

1. **查找安装命令** - 为每个平台找到安装命令
2. **确定检查命令** - 用于验证安装的命令
3. **添加到 config.json** - 按照上述格式添加

### 必需字段

- `name`: 命令名称（用于检测）
- `displayName`: UI 中的显示名称
- `checkCommand`: 验证安装的命令

### 平台特定的安装命令

- `windowsInstall`: Windows 原生安装
- `wslInstall`: WSL 环境安装
- `linuxInstall`: Linux 安装
- `macosInstall`: macOS 安装

### 可选字段

- `url`: 官方网站（显示在工具列表中）

---

## 💡 提示

1. **尽可能使用包管理器**（winget、brew、apt 等）
2. **测试检查命令** 确保它们正常工作
3. **保持 URL 更新** 供用户参考
4. **记录前置条件** 如果工具需要特定依赖

---

更多信息请参阅[主 README](../README.zh.md)。
