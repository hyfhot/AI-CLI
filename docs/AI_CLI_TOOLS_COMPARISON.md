# AI CLI 工具完整对比分析

> 本文档详细分析 AI-CLI 支持的所有 AI 编程助手工具，包括使用方式、参数说明和功能对比。
> 
> 更新时间：2026-03-05

## 目录

- [工具概览](#工具概览)
- [详细使用说明](#详细使用说明)
- [功能对比表](#功能对比表)
- [选择建议](#选择建议)

---

## 工具概览

AI-CLI 当前支持 **9 款** AI 编程助手工具：

| 工具 | 开发商 | 类型 | 开源 | 主要特点 |
|------|--------|------|------|----------|
| **Kiro CLI** | AWS | 终端 AI 助手 | ❌ | 规格驱动开发、企业级支持 |
| **Claude Code** | Anthropic | 终端 AI 助手 | ❌ | 强大的代码理解、MCP 集成 |
| **Cursor Agent** | Cursor | IDE + CLI | ❌ | 预测编辑、IDE 深度集成 |
| **Aider** | 开源社区 | 终端 AI 助手 | ✅ | Git 原生、多模型支持 |
| **OpenCode** | 开源社区 | 终端 AI 助手 | ✅ | 多提供商、LSP 支持 |
| **OpenAI Codex CLI** | OpenAI | 终端 AI 助手 | ✅ | GPT-4o/o1 支持、推理模型 |
| **Kimi CLI** | Moonshot AI | 终端 AI 助手 | ✅ | 中文优化、技能系统 |
| **Qwen Code** | Alibaba | 终端 AI 助手 | ✅ | Qwen3-Coder 优化、多语言 |
| **Gemini CLI** | Google | 终端 AI 助手 | ✅ | 多模态、免费额度大 |

---

## 详细使用说明

### 1. Kiro CLI

**官方网站**: https://kiro.dev/cli/

#### 安装方式

```bash
# macOS
brew install kiro-cli

# Linux/WSL
curl -fsSL https://cli.kiro.dev/install | bash
```

#### 核心命令

```bash
# 启动交互式聊天
kiro-cli chat

# 直接提问（非交互模式）
kiro-cli chat "如何列出 Linux 文件？"

# 恢复上次会话
kiro-cli chat --resume

# 选择会话恢复
kiro-cli chat --resume-picker

# 自然语言转命令
kiro-cli translate "列出所有 Python 文件"

# 管理自定义 Agent
kiro-cli agent list
kiro-cli agent create my-agent
kiro-cli agent edit my-agent

# 管理 MCP 服务器
kiro-cli mcp add --name server --command "node server.js"
kiro-cli mcp list

# 诊断问题
kiro-cli doctor
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--no-interactive` | 打印响应后退出（脚本模式） |
| `--resume` / `-r` | 恢复上次会话 |
| `--agent` | 指定使用的 Agent |
| `--trust-all-tools` | 允许模型使用任何工具无需确认 |
| `--trust-tools` | 仅信任指定工具（逗号分隔） |
| `--wrap` | 行换行模式：`always`/`never`/`auto` |

#### 特色功能

- **规格驱动开发**：先生成需求规格，再实现代码
- **自定义 Agent**：创建专门用途的 AI 助手
- **MCP 集成**：Model Context Protocol 服务器支持
- **会话管理**：自动保存所有对话，随时恢复
- **企业支持**：AWS Identity Center 集成

---

### 2. Claude Code

**官方网站**: https://www.npmjs.com/package/@anthropic-ai/claude-code

#### 安装方式

```bash
# 所有平台
npm install -g @anthropic-ai/claude-code
```

#### 核心命令

```bash
# 启动交互式会话
claude

# 直接查询
claude "解释这个函数的作用"

# 打印模式（脚本友好）
claude --print "生成 REST API"

# 指定模型
claude --model claude-opus-4 "复杂任务"

# 包含图片
claude --image ./screenshot.png "分析这个 UI"

# 查看历史
claude --history

# 恢复会话
claude --restore
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--model` / `-m` | 指定模型（opus-4/sonnet-4/haiku-4） |
| `--print` / `-p` | 打印模式，仅输出结果 |
| `--image` / `-i` | 包含图片文件 |
| `--auto-edit` | 自动批准文件编辑 |
| `--suggest` | 所有操作都需要确认（默认） |
| `--restore` | 恢复上次会话 |

#### 特色功能

- **Agentic 编码**：自主规划和调整执行步骤
- **MCP 服务器**：扩展工具和资源
- **Subagents**：独立上下文窗口的子代理
- **CLAUDE.md**：项目级配置文件
- **Hooks**：自定义工作流钩子

---

### 3. Cursor Agent

**官方网站**: https://cursor.sh

#### 安装方式

```bash
# Windows
winget install Cursor.Cursor

# macOS
brew install --cask cursor

# Linux
curl -fsSL https://cursor.sh/install.sh | bash
```

#### 核心命令

```bash
# 启动 Cursor IDE
cursor

# 打开特定文件/文件夹
cursor /path/to/project

# CLI 模式（如果安装了 Cursor CLI）
cursor-agent chat "帮我重构这个组件"

# 单次查询
cursor-agent "修复这个 bug"

# 流式输出
cursor-agent --stream "生成测试用例"
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--stream` | 流式输出响应 |
| `--json` | JSON 格式输出 |
| `--model` | 指定模型 |

#### 特色功能

- **预测编辑**：预测下一次逻辑修改
- **IDE 集成**：深度集成到编辑器
- **多行补全**：上下文感知的多行建议
- **项目索引**：理解整个代码库
- **Rules 系统**：项目级编码规则

---

### 4. Aider

**官方网站**: https://aider.chat

#### 安装方式

```bash
# 所有平台
pip install aider-chat

# macOS
brew install aider

# Linux/WSL
curl -LsSf https://aider.chat/install.sh | sh
```

#### 核心命令

```bash
# 启动并添加文件
aider file1.py file2.py

# 指定模型
aider --model o3-mini file.py
aider --model sonnet file.py

# 架构师模式
aider --architect file.py

# 自动批准模式
aider --auto-accept file.py

# 仅读取文件（不编辑）
aider --read-only docs/

# 使用本地模型
aider --model ollama/codellama file.py
```

#### 聊天内命令

| 命令 | 说明 |
|------|------|
| `/add <file>` | 添加文件到会话 |
| `/drop <file>` | 从会话移除文件 |
| `/undo` | 撤销最后的 AI 修改 |
| `/diff` | 显示未提交的更改 |
| `/commit` | 提交更改 |
| `/model <name>` | 切换模型 |
| `/architect` | 切换到架构师模式 |
| `/code` | 切换到编码模式 |
| `/ask` | 切换到问答模式 |
| `/help` | 显示帮助 |

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--model` | 指定 LLM 模型 |
| `--architect` | 先讨论再编码 |
| `--auto-accept` | 自动接受所有更改 |
| `--read-only` | 只读模式 |
| `--message` / `-m` | 直接发送消息 |
| `--yes` | 自动确认所有提示 |

#### 特色功能

- **Git 原生**：自动提交所有更改
- **多模型支持**：支持 50+ LLM 提供商
- **Repository Map**：自动理解代码库结构
- **编辑格式**：多种代码编辑策略
- **语音输入**：语音转代码

---

### 5. OpenCode

**官方网站**: https://opencode.ai

#### 安装方式

```bash
# Windows
curl -fsSL https://opencode.ai/install.ps1 | powershell

# Linux/macOS/WSL
curl -fsSL https://opencode.ai/install.sh | bash
```

#### 核心命令

```bash
# 启动 TUI（默认）
opencode

# 直接查询
opencode "创建 REST API"

# 指定提供商
opencode --provider anthropic "任务描述"
opencode --provider openai "任务描述"

# 使用本地模型
opencode --provider ollama --model codellama "任务描述"

# 配置管理
opencode config set provider anthropic
opencode config set model claude-opus-4
opencode config list
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--provider` | AI 提供商（anthropic/openai/gemini/ollama） |
| `--model` | 指定模型 |
| `--api-key` | API 密钥 |
| `--no-tui` | 禁用 TUI，使用简单模式 |

#### 特色功能

- **多提供商**：支持 75+ LLM 提供商
- **LSP 集成**：Language Server Protocol 支持
- **隐私优先**：不存储代码或上下文
- **开源**：完全开源，可自定义
- **Go 构建**：高性能、低资源占用

---

### 6. OpenAI Codex CLI

**官方网站**: https://www.npmjs.com/package/@openai/codex

#### 安装方式

```bash
# NPM（推荐）
npm install -g @openai/codex

# Homebrew
brew install codex
```

#### 核心命令

```bash
# 启动交互式会话
codex

# 直接查询
codex "解释这个函数"

# 安静模式（仅输出）
codex -q "修复这个 bug"

# 恢复上次会话
codex --restore

# 指定模型
codex -m "gpt-4o" "复杂任务"
codex -m "o1" "推理任务"

# 包含图片
codex -i ./screenshot.png "分析这个 UI"

# 查看历史
codex --history
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `-m` / `--model` | 指定模型（gpt-4o/o1/o3-mini） |
| `-q` / `--quiet` | 安静模式，仅输出结果 |
| `-i` / `--image` | 包含图片文件 |
| `-p` / `--provider` | 指定提供商 |
| `--restore` | 恢复上次会话 |
| `--auto-edit` | 自动批准文件编辑 |
| `--suggest` | 所有操作需确认（默认） |

#### 特色功能

- **推理模型**：支持 o1/o3-mini 推理模型
- **多模态**：支持图片、草图输入
- **会话恢复**：`codex resume --last`
- **命令队列**：批量执行命令
- **自定义提示库**：保存常用提示

---

### 7. Kimi CLI

**官方网站**: https://moonshotai.github.io/kimi-cli/

#### 安装方式

```bash
# Python（推荐）
pip install kimi-cli

# WSL（使用 uv）
uv tool install --python 3.13 kimi-cli
```

#### 核心命令

```bash
# 启动交互式会话
kimi

# 直接查询
kimi "如何使用 Docker？"

# 指定模型
kimi --model kimi-k1 "复杂任务"

# 非交互模式
kimi --no-interactive "生成代码"

# 启用技能
kimi --skills web-search,code-review "任务"
```

#### 聊天内命令

| 命令 | 说明 |
|------|------|
| `/clear` | 清除终端输出 |
| `/compact` | 压缩上下文（总结） |
| `/debug` | 查看调试日志 |
| `/release-notes` | 查看更新日志 |
| `/model` | 切换模型 |
| `/skills` | 管理技能 |

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--model` | 指定模型 |
| `--no-interactive` | 非交互模式 |
| `--skills` | 启用技能（逗号分隔） |
| `--api-key` | API 密钥 |

#### 特色功能

- **中文优化**：针对中文场景优化
- **技能系统**：可扩展的技能插件
- **MCP 支持**：Model Context Protocol
- **Web 搜索**：内置网页搜索能力
- **VS Code 集成**：编辑器扩展

---

### 8. Qwen Code

**官方网站**: https://qwenlm.github.io/qwen-code-docs/

#### 安装方式

```bash
# NPM
npm install -g @qwen-code/qwen-code@latest

# Linux/macOS/WSL
curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.sh | bash
```

#### 核心命令

```bash
# 启动交互式会话
qwen

# 直接查询
qwen "创建 Flask 应用"

# 指定模型
qwen --model qwen3-coder-32b "任务"

# 使用本地模型
qwen --provider ollama --model qwen3-coder "任务"

# Web 搜索集成
qwen --web-search "最新的 React 最佳实践"
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `--model` | 指定 Qwen 模型 |
| `--provider` | 提供商（qwen/ollama） |
| `--web-search` | 启用 Web 搜索 |
| `--language` | 界面语言（en/zh） |

#### 特色功能

- **Qwen3-Coder 优化**：专门优化的提示和协议
- **多语言支持**：中英文界面
- **Web 搜索**：集成搜索功能
- **Zed 集成**：与 Zed 编辑器集成
- **开源**：基于 Gemini CLI 改进

---

### 9. Gemini CLI

**官方网站**: https://www.npmjs.com/package/@google/gemini-cli

#### 安装方式

```bash
# 所有平台
npm install -g @google/gemini-cli
```

#### 核心命令

```bash
# 启动交互式会话
gemini

# 直接查询
gemini "解释这段代码"

# 包含文件
gemini -f readme.md "总结这个 README"

# 管道输入
cat package.json | gemini "解释这些依赖"

# 多文件分析
gemini --files="file1.py,file2.py" "比较这些文件"

# JSON 输出
gemini --json "提取数据"
```

#### 主要参数

| 参数 | 说明 |
|------|------|
| `-f` / `--file` | 包含文件内容 |
| `--files` | 多文件（逗号分隔） |
| `--json` | JSON 格式输出 |
| `--model` | 指定 Gemini 模型 |
| `--temperature` | 温度参数（0-1） |

#### 特色功能

- **多模态**：文本、图片、代码
- **免费额度大**：慷慨的免费使用限制
- **MCP 集成**：Model Context Protocol
- **快速原型**：适合快速查询和原型
- **管道友好**：Unix 管道集成


---

## 功能对比表

### 核心功能对比

| 功能 | Kiro CLI | Claude Code | Cursor | Aider | OpenCode | Codex CLI | Kimi CLI | Qwen Code | Gemini CLI |
|------|----------|-------------|--------|-------|----------|-----------|----------|-----------|------------|
| **交互式聊天** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **文件编辑** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **代码生成** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Git 集成** | ✅ | ✅ | ✅ | ✅✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **多文件编辑** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **会话管理** | ✅✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Shell 命令执行** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **图片输入** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| **语音输入** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Web 搜索** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

### 模型支持对比

| 工具 | 主要模型 | 多模型支持 | 本地模型 | 推理模型 |
|------|----------|------------|----------|----------|
| **Kiro CLI** | Claude Opus 4.6 | ✅ (Claude 系列) | ❌ | ❌ |
| **Claude Code** | Claude Opus 4 | ✅ (Claude 系列) | ❌ | ❌ |
| **Cursor** | GPT-4o, Claude | ✅ | ❌ | ❌ |
| **Aider** | Claude 3.5, GPT-4o | ✅✅ (50+) | ✅ | ✅ (o1/o3) |
| **OpenCode** | 多提供商 | ✅✅ (75+) | ✅ | ✅ |
| **Codex CLI** | GPT-4o, o1 | ✅ | ❌ | ✅ (o1/o3) |
| **Kimi CLI** | Kimi-k1 | ✅ (Kimi 系列) | ❌ | ❌ |
| **Qwen Code** | Qwen3-Coder | ✅ | ✅ | ❌ |
| **Gemini CLI** | Gemini 2.0 | ✅ (Gemini 系列) | ❌ | ❌ |

### 扩展性对比

| 功能 | Kiro CLI | Claude Code | Cursor | Aider | OpenCode | Codex CLI | Kimi CLI | Qwen Code | Gemini CLI |
|------|----------|-------------|--------|-------|----------|-----------|----------|-----------|------------|
| **MCP 服务器** | ✅✅ | ✅✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **自定义 Agent** | ✅✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **插件系统** | ❌ | ✅ (Hooks) | ✅ | ❌ | ❌ | ❌ | ✅ (Skills) | ❌ | ❌ |
| **API 访问** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **配置文件** | ✅ | ✅ (CLAUDE.md) | ✅ (.cursorrules) | ✅ (.aider.conf) | ✅ | ✅ | ✅ | ✅ | ✅ |

### 平台支持对比

| 平台 | Kiro CLI | Claude Code | Cursor | Aider | OpenCode | Codex CLI | Kimi CLI | Qwen Code | Gemini CLI |
|------|----------|-------------|--------|-------|----------|-----------|----------|-----------|------------|
| **Windows** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WSL** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 定价对比

| 工具 | 免费版 | 付费版 | 定价模式 | 备注 |
|------|--------|--------|----------|------|
| **Kiro CLI** | ✅ (预览) | ✅ | 订阅制 | AWS Builder ID 免费，Pro 需订阅 |
| **Claude Code** | ❌ | ✅ | API 计费 | 需要 Anthropic API 密钥 + 充值 |
| **Cursor** | ✅ (限制) | ✅ | 订阅制 | $20/月，包含 500 次快速请求 |
| **Aider** | ✅ | - | API 计费 | 开源免费，需自备 API 密钥 |
| **OpenCode** | ✅ | - | API 计费 | 开源免费，需自备 API 密钥 |
| **Codex CLI** | ❌ | ✅ | API 计费 | 需要 OpenAI API 密钥 |
| **Kimi CLI** | ✅ | ✅ | API 计费 | 有免费额度，超出需充值 |
| **Qwen Code** | ✅ | ✅ | API 计费 | 可用本地模型完全免费 |
| **Gemini CLI** | ✅✅ | ✅ | API 计费 | 免费额度非常大 |

### 性能对比

| 指标 | Kiro CLI | Claude Code | Cursor | Aider | OpenCode | Codex CLI | Kimi CLI | Qwen Code | Gemini CLI |
|------|----------|-------------|--------|-------|----------|-----------|----------|-----------|------------|
| **响应速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **代码质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **上下文理解** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **资源占用** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **稳定性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 学习曲线对比

| 工具 | 上手难度 | 文档质量 | 社区支持 | 适合人群 |
|------|----------|----------|----------|----------|
| **Kiro CLI** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 企业开发者、AWS 用户 |
| **Claude Code** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 专业开发者 |
| **Cursor** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 所有开发者 |
| **Aider** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Git 熟练用户 |
| **OpenCode** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 开源爱好者 |
| **Codex CLI** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | OpenAI 用户 |
| **Kimi CLI** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中文开发者 |
| **Qwen Code** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中文开发者、本地部署 |
| **Gemini CLI** | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 快速原型、初学者 |

---

## 选择建议

### 按使用场景选择

#### 🏢 企业开发
**推荐**: Kiro CLI, Claude Code
- **理由**: 企业级支持、安全性、合规性
- **次选**: Cursor（如果需要 IDE 集成）

#### 🚀 个人项目
**推荐**: Aider, OpenCode, Gemini CLI
- **理由**: 开源免费、灵活性高
- **次选**: Kimi CLI（中文用户）

#### 🎯 快速原型
**推荐**: Gemini CLI, Cursor
- **理由**: 快速响应、易用性
- **次选**: Claude Code

#### 🔬 复杂重构
**推荐**: Claude Code, Kiro CLI, Aider
- **理由**: 强大的代码理解能力
- **次选**: Codex CLI（如果需要推理模型）

#### 🌐 中文场景
**推荐**: Kimi CLI, Qwen Code
- **理由**: 中文优化、本地化支持
- **次选**: Claude Code（多语言支持好）

#### 💰 预算有限
**推荐**: Aider, OpenCode, Qwen Code（本地模型）
- **理由**: 开源免费、可用本地模型
- **次选**: Gemini CLI（免费额度大）

### 按技术栈选择

#### Python 开发
1. **Aider** - Git 原生，Python 生态
2. **Kimi CLI** - Python 安装，中文友好
3. **Claude Code** - 强大的 Python 理解

#### JavaScript/TypeScript
1. **Cursor** - 前端开发最佳
2. **Claude Code** - Node.js 生态
3. **Codex CLI** - OpenAI 优化

#### Go/Rust/系统编程
1. **OpenCode** - Go 构建，性能优秀
2. **Aider** - 多语言支持
3. **Claude Code** - 系统级理解

#### 全栈开发
1. **Kiro CLI** - 规格驱动，全栈支持
2. **Claude Code** - 多文件协调
3. **Cursor** - IDE 集成

### 按团队规模选择

#### 个人开发者
- **首选**: Aider, Gemini CLI
- **备选**: OpenCode, Kimi CLI

#### 小团队（2-10人）
- **首选**: Claude Code, Cursor
- **备选**: Aider, Kiro CLI

#### 中大型团队（10+人）
- **首选**: Kiro CLI, Cursor
- **备选**: Claude Code

### 特殊需求

#### 需要离线使用
- **Aider** + Ollama
- **OpenCode** + 本地模型
- **Qwen Code** + 本地 Qwen3-Coder

#### 需要推理能力
- **Codex CLI** (o1/o3-mini)
- **Aider** (支持 o1)
- **OpenCode** (多模型)

#### 需要多模态
- **Gemini CLI** - 最佳多模态
- **Codex CLI** - 图片支持
- **Claude Code** - 图片分析

#### 需要 Web 搜索
- **Kimi CLI** - 内置搜索
- **Qwen Code** - 搜索集成

---

## 功能矩阵图

```
                    易用性
                      ↑
                      |
        Gemini CLI ●  |  ● Cursor
                      |
        Kimi CLI   ●  |  ● Claude Code
                      |
                   ●  |  ● Kiro CLI
              Qwen    |
                      |
        OpenCode   ●  |
                      |
        Aider      ●  |  ● Codex CLI
                      |
                      |
    ←─────────────────┼─────────────────→
    简单功能          |          复杂功能
                      |
                      ↓
```

## 成本对比图

```
月度成本（美元）
  ↑
  |
$50|                    ● Cursor Pro
  |
$40|
  |
$30|              ● Claude Code (重度使用)
  |
$20|         ● Kiro CLI Pro
  |    ● Codex CLI (中度使用)
$10|    ● Kimi CLI (付费)
  |
 $5|    ● Gemini CLI (付费)
  |
 $0|● Aider ● OpenCode ● Qwen Code (本地)
  └─────────────────────────────────────→
    开源免费    API计费    订阅制
```

---

## 总结

### 最佳综合选择
1. **Claude Code** - 功能最全面，代码质量最高
2. **Kiro CLI** - 企业级支持，规格驱动开发
3. **Aider** - 开源最佳，Git 原生

### 最佳性价比
1. **Aider** - 开源免费，功能强大
2. **Gemini CLI** - 免费额度大
3. **OpenCode** - 开源，多提供商

### 最佳用户体验
1. **Cursor** - IDE 集成最佳
2. **Gemini CLI** - 最易上手
3. **Claude Code** - 交互体验好

### 最佳中文支持
1. **Kimi CLI** - 专为中文优化
2. **Qwen Code** - 中文模型
3. **Claude Code** - 多语言支持

---

## 更新日志

- **2026-03-05**: 初始版本，包含 9 款工具的详细对比
- 基于最新的搜索结果和官方文档整理

## 参考资料

- [Kiro CLI 官方文档](https://kiro.dev/docs/cli/)
- [Claude Code 完整指南](https://www.viberank.app/blog/claude-code-complete-guide)
- [Aider 官方文档](https://aider.chat/docs/)
- [OpenCode 文档](https://opencode.ai/docs)
- [Codex CLI 指南](https://majesticlabs.dev/blog/202509/codex-cli-developer-guide)
- [Kimi CLI 文档](https://moonshotai.github.io/kimi-cli/)
- [Qwen Code 教程](https://www.datacamp.com/tutorial/qwen-code)
- [Gemini CLI 速查表](https://www.geminicli.net/cheatsheet)

---

**注意**: 本文档基于 2026 年 3 月的信息整理，部分工具可能已有更新。使用前请查阅官方文档获取最新信息。
