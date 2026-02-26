# AI CLI Tools Reference

本文档列出了 AI-CLI 支持的主流 AI 编程工具及其安装配置信息。

---

## 🤖 支持的工具列表

### 1. Kiro CLI (AWS)
- **官方网站**: https://kiro.dev/cli/
- **开发商**: Amazon Web Services
- **特点**: 
  - 规范驱动的开发平台
  - 支持代理工作流
  - 集成 AWS 服务
  - 支持 Model Context Protocol (MCP)
- **安装命令**:
  - WSL/Linux: `curl -fsSL https://cli.kiro.dev/install | bash`
  - Windows: 不支持原生安装
- **验证**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **官方网站**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **开发商**: Anthropic
- **特点**:
  - 代理式编码助手
  - 100K+ 上下文窗口
  - 支持多文件操作
  - 集成 Git 工作流
  - 支持 MCP 协议
- **安装命令**:
  - Windows: `npm install -g @anthropic-ai/claude-code`
  - WSL/Linux: `npm install -g @anthropic-ai/claude-code`
- **验证**: `claude --version`
- **要求**: Node.js 18+

---

### 3. OpenAI Codex CLI
- **官方网站**: https://www.npmjs.com/package/@openai/codex
- **开发商**: OpenAI
- **特点**:
  - 轻量级编码代理
  - 本地执行，代码不上传
  - 支持自然语言命令
  - 开源项目
- **安装命令**:
  - Windows: `npm install -g @openai/codex`
  - WSL/Linux: `npm install -g @openai/codex`
- **验证**: `codex --version`
- **要求**: Node.js 18+

---

### 4. Kimi CLI (Moonshot AI)
- **官方网站**: https://pypi.org/project/kimi-cli/
- **开发商**: Moonshot AI (月之暗面)
- **特点**:
  - 终端 AI 代理
  - 支持代码读写和命令执行
  - 支持网页搜索和抓取
  - 自主规划和调整行动
- **安装命令**:
  - Windows: `pip install kimi-cli`
  - WSL/Linux: `uv tool install --python 3.13 kimi-cli`
- **验证**: `kimi --version`
- **要求**: Python 3.13+, uv (推荐)

---

### 5. Gemini CLI (Google)
- **官方网站**: https://www.npmjs.com/package/@google/gemini-cli
- **开发商**: Google
- **特点**:
  - 开源 AI 代理
  - 1M token 上下文窗口
  - 多模态 AI 能力
  - 免费使用
- **安装命令**:
  - Windows: `npm install -g @google/gemini-cli`
  - WSL/Linux: `npm install -g @google/gemini-cli`
- **验证**: `gemini --version`
- **要求**: Node.js

---

### 6. Cursor Agent CLI
- **官方网站**: https://docs.cursor.com/en/cli/installation
- **开发商**: Cursor
- **特点**:
  - 终端 AI 助手
  - 支持远程服务器和容器
  - 集成 GitHub Actions
  - 自动更新
- **安装命令**:
  - WSL/Linux: `curl https://cursor.com/install -fsS | bash`
  - Windows: 不支持原生安装
- **验证**: `cursor-agent --version`
- **使用**: `cursor-agent` 或 `agent chat "prompt"`

---

### 7. OpenCode
- **官方网站**: https://opencode.ai/docs
- **开发商**: 开源社区
- **特点**:
  - 开源 AI 编码代理
  - 隐私优先，不存储代码
  - 支持免费内置模型
  - 可连接外部 AI 提供商
  - 原生终端 UI
- **安装命令**:
  - Windows: `curl -fsSL https://opencode.ai/install.ps1 | powershell`
  - WSL/Linux: `curl -fsSL https://opencode.ai/install.sh | bash`
- **验证**: `opencode --version`

---

### 8. Aider
- **官方网站**: https://aider.chat/docs/install
- **开发商**: 开源社区
- **特点**:
  - 终端 AI 编程助手
  - 深度集成 Git
  - 支持多种 LLM (GPT-4, Claude, DeepSeek)
  - 自动代码测试
  - 预算友好 ($0.007/文件)
- **安装命令**:
  - Windows: `pip install aider-install && aider-install`
  - WSL/Linux: `pip install aider-install && aider-install`
- **验证**: `aider --version`
- **要求**: Python 3.9+, Git

---

## 📊 工具对比

| 工具 | 开发商 | 免费 | 开源 | Windows | WSL/Linux | 特色 |
|------|--------|------|------|---------|-----------|------|
| Kiro CLI | AWS | ✅ | ❌ | ❌ | ✅ | 规范驱动，AWS集成 |
| Claude Code | Anthropic | ❌ | ❌ | ✅ | ✅ | 100K上下文，MCP |
| Codex CLI | OpenAI | ❌ | ✅ | ✅ | ✅ | 本地执行，隐私 |
| Kimi CLI | Moonshot | ❌ | ❌ | ✅ | ✅ | 网页搜索，中文优化 |
| Gemini CLI | Google | ✅ | ✅ | ✅ | ✅ | 1M上下文，免费 |
| Cursor Agent | Cursor | ❌ | ❌ | ❌ | ✅ | CI/CD集成 |
| OpenCode | 社区 | ✅ | ✅ | ✅ | ✅ | 隐私优先，多模型 |
| Aider | 社区 | ✅ | ✅ | ✅ | ✅ | Git集成，多LLM |

---

## 🔧 安装前提条件

### 通用要求
- **Git**: 大多数工具需要 Git 进行版本控制
- **终端**: Windows Terminal (推荐) 或其他现代终端

### Node.js 工具 (Claude, Codex, Gemini)
- Node.js 18+ 
- npm 或 pnpm

### Python 工具 (Kimi, Aider)
- Python 3.9+ (Aider) 或 3.13+ (Kimi)
- pip 或 uv

### Shell 脚本工具 (Kiro, Cursor, OpenCode)
- bash (WSL/Linux)
- curl

---

## 💡 使用建议

### 选择工具的考虑因素

1. **预算**:
   - 免费: Gemini CLI, OpenCode, Aider
   - 付费: Claude Code, Codex CLI, Kimi CLI, Cursor Agent

2. **隐私**:
   - 本地执行: Codex CLI, OpenCode
   - 云端: 其他工具

3. **功能需求**:
   - AWS 集成: Kiro CLI
   - Git 深度集成: Aider
   - 多模型支持: OpenCode
   - 大上下文: Gemini CLI (1M), Claude Code (100K)

4. **语言偏好**:
   - 中文优化: Kimi CLI
   - 英文: 其他工具

---

## 🔄 更新配置

要添加新工具或修改现有工具配置，编辑 `config.json` 文件：

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

## 📚 参考资源

- [Kiro CLI 文档](https://kiro.dev/docs/cli/installation/)
- [Claude Code 指南](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [Codex CLI GitHub](https://github.com/openai/codex-cli)
- [Kimi CLI 文档](https://moonshotai.github.io/kimi-cli/en/)
- [Gemini CLI 官网](https://gemini-cli.click/)
- [Cursor CLI 文档](https://docs.cursor.com/en/cli/)
- [OpenCode 文档](https://opencode.ai/docs)
- [Aider 文档](https://aider.chat/docs/)

---

*最后更新: 2026-02-26*
