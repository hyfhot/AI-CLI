# AI-CLI (Python 版本)

> 🌐 [English](README.md) | **中文** | [日本語](README.ja.md)

[![Python 版本](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![许可证](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![状态](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** 是一个跨平台的终端启动器，用于管理多个 AI 编程助手。无缝切换 Kiro CLI、Claude Code、Cursor Agent 等工具。

## ✨ 核心特性

### 🌍 跨平台支持
- **Windows**: 原生支持 + WSL 集成
- **Linux**: 完整支持所有主流发行版
- **macOS**: 支持 Terminal.app 和 iTerm2

### 🔄 WSL 深度集成
- 自动检测 WSL 环境
- Windows ↔ WSL 路径自动转换
- 支持在 Windows 中启动 WSL 工具
- 支持在 WSL 中启动 Windows 工具

### 📁 项目管理
- **树形结构**: 使用文件夹组织项目
- **Git Worktree**: 自动检测和选择 Git worktrees
- **环境变量**: 为每个项目配置独立的环境变量
- **路径规范化**: 自动处理不同平台的路径格式

### ⚡ 工具检测与管理
- **异步检测**: 使用 async/await 并行检测工具
- **智能缓存**: 后台检测并缓存结果
- **一键安装**: 按 `I` 键安装未安装的工具
- **手动刷新**: 按 `R` 键刷新工具列表
- **环境识别**: 自动识别 Windows、WSL、Linux、macOS 环境

### 🎨 用户界面
- **Rich UI**: 基于 Rich 库的美观终端界面
- **键盘导航**: 完整的键盘快捷键支持
- **实时反馈**: 显示工具检测和安装进度
- **主题支持**: 可自定义的颜色主题

### 🌐 国际化
- **多语言支持**: 英语、中文、日语、德语
- **自动检测**: 根据系统语言自动选择
- **可配置**: 在配置文件中手动指定语言

## 🚀 快速开始

### 安装

#### 使用安装脚本（推荐）

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

#### 手动安装

```bash
# 克隆仓库
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 如果使用 Git worktree
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 安装依赖
pip install -e ".[dev]"
```

### 初始化配置

```bash
ai-cli --init
```

这将创建默认配置文件，包含常用 AI 工具的配置。

### 运行

```bash
ai-cli
```

## 📖 使用说明

### 命令行选项

```bash
ai-cli              # 启动交互界面
ai-cli --init       # 初始化配置文件
ai-cli --config     # 编辑配置文件
ai-cli --uninstall  # 卸载 AI-CLI
ai-cli --version    # 显示版本信息
ai-cli --help       # 显示帮助信息
```

### 键盘快捷键

#### 项目选择界面

| 按键 | 功能 |
|------|------|
| `↑` / `↓` | 上下导航 |
| `Enter` | 选择项目 / 进入文件夹 |
| `Esc` | 返回上级文件夹 |
| `N` | 新建项目或文件夹 |
| `D` | 删除选中的项目或文件夹 |
| `Q` | 退出程序 |

#### 工具选择界面

| 按键 | 功能 |
|------|------|
| `↑` / `↓` | 上下导航 |
| `Enter` | 启动工具（新窗口） |
| `Ctrl+Enter` | 启动工具（新标签页） |
| `I` | 安装未安装的工具 |
| `R` | 刷新工具列表 |
| `Esc` | 返回项目选择界面 |
| `Q` | 退出程序 |

### 工作流程

1. **启动程序**: 运行 `ai-cli`
2. **选择项目**: 使用方向键选择项目，按 `Enter` 确认
3. **选择工具**: 选择要使用的 AI 工具
4. **开始工作**: 工具将在新窗口或标签页中启动

## 🔧 配置详解

### 配置文件位置

- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### 配置文件结构

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

### 项目配置

#### 项目类型

**文件夹 (folder)**:
```json
{
  "type": "folder",
  "name": "项目组名称",
  "children": [...]
}
```

**项目 (project)**:
```json
{
  "type": "project",
  "name": "项目名称",
  "path": "/absolute/path/to/project",
  "env": {
    "KEY": "value"
  }
}
```

#### 环境变量

为每个项目配置独立的环境变量：

```json
{
  "type": "project",
  "name": "API 项目",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "API_BASE_URL": "https://api.example.com",
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

### 工具配置

#### 必需字段

- `name`: 工具的命令名称（用于检测）
- `displayName`: 显示名称
- `checkCommand`: 用于检测工具是否安装的命令

#### 安装命令（按平台）

- `windowsInstall`: Windows 原生安装命令
- `wslInstall`: WSL 环境安装命令
- `linuxInstall`: Linux 安装命令
- `macosInstall`: macOS 安装命令

#### 可选字段

- `url`: 工具的官方网站（显示在工具列表中）

#### 示例配置

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

### 设置选项

#### language（语言）

- `auto`: 自动检测系统语言（默认）
- `en`: 英语
- `zh`: 中文
- `ja`: 日语
- `de`: 德语

#### terminalEmulator（终端模拟器）

- `default`: 使用系统默认终端（默认）
- `wt`: Windows Terminal（仅 Windows）
- `iterm`: iTerm2（仅 macOS）
- `gnome-terminal`: GNOME Terminal（仅 Linux）
- `konsole`: Konsole（仅 Linux）

#### theme（主题）

- `default`: 默认深色主题
- 未来版本将支持更多主题

## 🏗️ 项目架构

### 目录结构

```
ai_cli/
├── __init__.py        # 包初始化
├── cli.py             # CLI 入口点
├── app.py             # 主应用逻辑
├── models.py          # 数据模型
├── config.py          # 配置管理
├── utils.py           # 路径转换工具
├── core/              # 核心功能模块
│   ├── __init__.py
│   ├── tools.py       # 工具检测
│   ├── projects.py    # 项目管理
│   ├── git.py         # Git 集成
│   └── installer.py   # 工具安装
├── ui/                # 用户界面模块
│   ├── __init__.py
│   ├── theme.py       # 主题配置
│   ├── menu.py        # 菜单渲染
│   └── input.py       # 键盘输入处理
├── platform/          # 平台适配模块
│   ├── __init__.py
│   ├── base.py        # 抽象基类
│   ├── windows.py     # Windows 适配器
│   ├── linux.py       # Linux 适配器
│   ├── macos.py       # macOS 适配器
│   └── factory.py     # 平台工厂
└── i18n/              # 国际化模块
    ├── __init__.py
    └── manager.py     # 语言管理器
```

### 核心模块说明

#### models.py - 数据模型

定义了所有数据结构：
- `Config`: 主配置对象
- `Settings`: 设置选项
- `ProjectNode`: 项目节点（支持树形结构）
- `Tool`: 工具对象
- `ToolConfig`: 工具配置
- `ToolEnvironment`: 工具运行环境枚举

#### config.py - 配置管理

- 跨平台配置文件路径处理
- 配置文件加载和保存
- 从旧版本配置迁移
- 创建默认配置

#### app.py - 主应用

- 应用主循环
- 项目选择逻辑
- 工具选择逻辑
- 工具启动逻辑
- 项目和文件夹的增删改

#### core/tools.py - 工具检测

- 异步并行检测工具
- 平台特定的检测逻辑
- Windows 原生工具检测
- WSL 工具检测
- 工具缓存管理

#### core/git.py - Git 集成

- 检测 Git worktrees
- 显示分支状态
- 交互式 worktree 选择

#### core/installer.py - 工具安装

- 根据平台选择安装命令
- 执行安装过程
- 安装后路径更新
- 查找已安装的工具

#### ui/menu.py - 菜单渲染

- 渲染项目树
- 渲染工具列表
- 显示面包屑导航
- 清屏和刷新

#### ui/input.py - 键盘输入

- 跨平台键盘输入处理
- Windows 和 Unix 系统的不同实现
- 文本输入支持
- 特殊键处理

#### platform/ - 平台适配

- 抽象平台接口
- Windows 特定实现（支持 Windows Terminal）
- Linux 特定实现（支持多种终端）
- macOS 特定实现（支持 iTerm2）
- 平台工厂模式

#### i18n/manager.py - 国际化

- 语言检测
- 翻译字典管理
- 文本获取接口

## 🔍 高级功能

### Git Worktree 支持

当项目路径是 Git worktree 时，AI-CLI 会：

1. 自动检测所有 worktrees
2. 显示每个 worktree 的分支和状态
3. 允许选择要使用的 worktree
4. 显示分支的领先/落后提交数

### WSL 路径转换

AI-CLI 自动处理 Windows 和 WSL 之间的路径转换：

- Windows 路径: `C:\Users\username\project`
- WSL 路径: `/mnt/c/Users/username/project`

转换是双向的，支持：
- Windows 中启动 WSL 工具
- WSL 中启动 Windows 工具

### 异步工具检测

工具检测使用异步并行处理：

1. **启动时**: 快速显示界面，后台检测工具
2. **缓存**: 检测结果被缓存，避免重复检测
3. **刷新**: 按 `R` 键清除缓存并重新检测

### 环境变量注入

为每个项目配置的环境变量会在启动工具时注入：

```json
{
  "type": "project",
  "name": "API 项目",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "DEBUG": "true"
  }
}
```

启动工具时，这些环境变量会被添加到工具的运行环境中。

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models.py

# 运行特定测试
pytest tests/test_models.py::TestConfig::test_from_dict

# 显示详细输出
pytest -v

# 显示打印输出
pytest -s
```

### 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=ai_cli

# 生成 HTML 覆盖率报告
pytest --cov=ai_cli --cov-report=html

# 查看报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### 测试文件说明

- `test_models.py`: 数据模型测试
- `test_config.py`: 配置管理测试
- `test_utils.py`: 路径转换测试
- `test_platform.py`: 平台适配器测试
- `test_git.py`: Git 集成测试
- `test_tools.py`: 工具检测测试
- `test_projects.py`: 项目管理测试
- `test_ui.py`: UI 组件测试
- `test_app.py`: 应用集成测试
- `test_cli.py`: CLI 入口测试

## 📝 开发指南

### 环境要求

- **Python**: 3.8 或更高版本
- **依赖库**:
  - `rich`: 终端 UI 渲染
  - `prompt-toolkit`: 键盘输入处理
  - `click`: CLI 框架
  - `platformdirs`: 跨平台路径

### 开发环境设置

```bash
# 1. 克隆仓库
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 2. 创建 Python 版本的 worktree（如果需要）
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 3. 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. 安装开发依赖
pip install -e ".[dev]"

# 5. 运行测试确认环境
pytest
```

### 代码风格

项目遵循 PEP 8 代码风格指南：

```bash
# 安装代码检查工具
pip install flake8 black mypy

# 运行代码检查
flake8 ai_cli tests

# 自动格式化代码
black ai_cli tests

# 类型检查
mypy ai_cli
```

### 添加新工具

在 `config.json` 中添加新工具配置：

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

### 添加新语言

在 `ai_cli/i18n/manager.py` 中添加翻译：

```python
translations = {
    'new_lang': {
        'app_title': 'AI-CLI',
        'select_project': 'Select Project',
        # ... 其他翻译
    }
}
```

### 调试技巧

```bash
# 启用调试模式
ai-cli --debug

# 使用 Python 调试器
python -m pdb -m ai_cli.cli

# 查看详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🐛 故障排除

### Windows 相关问题

**问题**: 无法检测到 Windows Terminal
```bash
# 解决方案：确保 Windows Terminal 已安装
winget install Microsoft.WindowsTerminal
```

**问题**: WSL 工具检测失败
```bash
# 解决方案：确保 WSL 已启用
wsl --install
```

### Linux 相关问题

**问题**: 终端模拟器检测失败
```bash
# 解决方案：安装支持的终端
sudo apt install gnome-terminal  # Ubuntu/Debian
sudo dnf install gnome-terminal  # Fedora
```

### macOS 相关问题

**问题**: iTerm2 未被检测到
```bash
# 解决方案：确保 iTerm2 已安装
brew install --cask iterm2
```

### 通用问题

**问题**: 配置文件损坏
```bash
# 解决方案：重新初始化配置
ai-cli --init
```

**问题**: 工具检测缓存过期
```bash
# 解决方案：在工具选择界面按 R 键刷新
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告 Bug**: 在 [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues) 提交问题
2. **功能建议**: 提出新功能的想法
3. **代码贡献**: 提交 Pull Request
4. **文档改进**: 改进文档和示例
5. **翻译**: 添加新语言支持

### Pull Request 流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 添加新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具链更新
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- **原项目**: [AI-CLI (PowerShell 版本)](https://github.com/hyfhot/AI-CLI)
- **文档**: [docs/](docs/)
- **问题反馈**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

## 🙏 致谢

感谢以下开源项目：

- [Rich](https://github.com/Textualize/rich) - 强大的终端 UI 库
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - 交互式命令行工具
- [Click](https://github.com/pallets/click) - Python CLI 框架
- [platformdirs](https://github.com/platformdirs/platformdirs) - 跨平台目录路径

## 📊 项目状态

- **版本**: Beta
- **Python 版本**: 3.8+
- **平台**: Windows, Linux, macOS
- **维护状态**: 活跃开发中

## 🗺️ 路线图

- [ ] 支持更多 AI 工具
- [ ] 插件系统
- [ ] 配置文件验证
- [ ] 更多主题选项
- [ ] 工具使用统计
- [ ] 云端配置同步
- [ ] 项目模板支持

---

**用 ❤️ 制作 by AI-CLI 团队**
