# AI-CLI (Python 版本)

> 🌐 [English](README.md) | **中文**

[![Python 版本](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![许可证](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![状态](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** 是一个跨平台的终端启动器，用于管理多个 AI 编程助手。无缝切换 Kiro CLI、Claude Code、Cursor Agent 等工具。

## ✨ 特性

- 🌍 **跨平台支持**: Windows、Linux、macOS
- 🔄 **WSL 支持**: Windows ↔ WSL 环境无缝切换
- 📁 **树形结构**: 文件夹方式组织项目
- ⚡ **异步检测**: 使用 async/await 快速检测工具
- 🎨 **精美界面**: 美观的终端界面和键盘快捷键
- 🔧 **自动路径转换**: Windows ↔ WSL 路径自动转换
- 🌳 **Git Worktree**: 检测和管理 Git worktrees
- 🎯 **环境变量**: 项目级环境变量注入

## 🚀 快速开始

### 安装

```bash
pip install -e ".[dev]"
```

### 初始化配置

```bash
ai-cli --init
```

### 运行

```bash
ai-cli
```

## 📖 使用说明

### 命令

```bash
ai-cli              # 启动交互界面
ai-cli --init       # 初始化配置
ai-cli --config     # 编辑配置文件
ai-cli --version    # 显示版本
ai-cli --help       # 显示帮助
```

### 键盘快捷键

**项目选择界面**:
- `↑↓` - 上下导航
- `Enter` - 选择项目 / 进入文件夹
- `Esc` - 返回上级
- `N` - 新建项目
- `D` - 删除项目
- `Q` - 退出程序

**工具选择界面**:
- `↑↓` - 上下导航
- `Enter` - 启动工具（新窗口）
- `Ctrl+Enter` - 启动工具（新标签页）
- `I` - 安装工具
- `R` - 刷新工具列表
- `Esc` - 返回上级
- `Q` - 退出程序

## 🔧 配置

配置文件位置：
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

配置示例：

```json
{
  "projects": [
    {
      "type": "folder",
      "name": "我的项目",
      "children": [
        {
          "type": "project",
          "name": "Web 应用",
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

## 🏗️ 架构

```
ai_cli/
├── models.py          # 数据模型
├── config.py          # 配置管理
├── utils.py           # 路径转换工具
├── app.py             # 主应用
├── cli.py             # CLI 入口
├── core/
│   ├── tools.py       # 工具检测
│   ├── projects.py    # 项目管理
│   └── git.py         # Git 集成
├── ui/
│   ├── theme.py       # 主题配置
│   ├── menu.py        # 菜单渲染
│   └── input.py       # 键盘输入
└── platform/
    ├── base.py        # 抽象适配器
    ├── windows.py     # Windows 适配器
    ├── linux.py       # Linux 适配器
    ├── macos.py       # macOS 适配器
    └── factory.py     # 平台工厂
```

## 🧪 测试

```bash
# 运行测试
pytest

# 运行覆盖率测试
pytest --cov=ai_cli

# 运行特定测试
pytest tests/test_models.py
```

## 📝 开发

### 要求

- Python 3.8+
- 依赖: rich, prompt-toolkit, click, platformdirs

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 创建 Python 版本 worktree
git worktree add ../ai-cli-multi-platform python-migration

# 安装依赖
cd ../ai-cli-multi-platform
pip install -e ".[dev]"

# 运行测试
pytest
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 链接

- **原项目**: [AI-CLI (PowerShell)](https://github.com/hyfhot/AI-CLI)
- **文档**: [docs/](docs/)
- **问题反馈**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)

## 🙏 致谢

- [Rich](https://github.com/Textualize/rich) - 终端 UI
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - 键盘输入
- [Click](https://github.com/pallets/click) - CLI 框架

---

**用 ❤️ 制作 by AI-CLI 团队**
