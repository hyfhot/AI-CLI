# 🚀 AI-CLI Python 版本 - 快速启动指南

> **项目状态**: ✅ 核心功能开发完成  
> **版本**: 0.1.0  
> **完成时间**: 2026-03-01

---

## 📦 安装

### 1. 安装依赖

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]"
```

这将安装：
- `rich` - 终端 UI 渲染
- `prompt-toolkit` - 键盘输入处理
- `click` - CLI 参数解析
- `platformdirs` - 跨平台路径
- `pytest` 等开发工具

---

## 🎯 快速开始

### 2. 初始化配置

```bash
ai-cli --init
```

这将在以下位置创建配置文件：
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### 3. 编辑配置

```bash
ai-cli --config
```

添加你的项目和工具配置：

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

### 4. 运行程序

```bash
ai-cli
```

---

## ⌨️ 键盘快捷键

### 项目选择界面
- `↑↓` - 上下导航
- `Enter` - 进入文件夹 / 选择项目
- `Esc` - 返回上级
- `N` - 新建项目
- `D` - 删除项目
- `Q` - 退出程序

### 工具选择界面
- `↑↓` - 上下导航
- `Enter` - 启动工具（新窗口）
- `Ctrl+Enter` - 启动工具（新标签页）
- `I` - 安装工具
- `R` - 刷新工具列表
- `Esc` - 返回项目选择
- `Q` - 退出程序

---

## 🔧 命令行参数

```bash
ai-cli --help          # 显示帮助信息
ai-cli --version       # 显示版本信息
ai-cli --init          # 初始化配置文件
ai-cli --config        # 编辑配置文件
ai-cli                 # 启动交互界面（默认）
```

---

## 🎨 功能特性

### ✅ 已实现
- ✅ 跨平台支持 (Windows/Linux/macOS)
- ✅ Windows WSL 双环境支持
- ✅ 树形项目结构
- ✅ 异步工具检测
- ✅ 自动路径转换
- ✅ 环境变量注入
- ✅ 终端标题设置
- ✅ 多标签支持 (Windows Terminal)
- ✅ Git Worktree 检测

### 🔄 开发中
- 🔄 工具安装功能
- 🔄 更多测试覆盖
- 🔄 完整文档

---

## 📊 项目结构

```
ai-cli-multi-platform/
├── ai_cli/              # 核心代码
│   ├── models.py        # 数据模型
│   ├── config.py        # 配置管理
│   ├── utils.py         # 工具函数
│   ├── app.py           # 主应用
│   ├── cli.py           # CLI 入口
│   ├── core/            # 核心模块
│   ├── ui/              # UI 模块
│   └── platform/        # 平台适配器
├── tests/               # 测试文件
└── pyproject.toml       # 项目配置
```

---

## 🐛 故障排除

### 问题：找不到 ai-cli 命令

**解决方案**:
```bash
pip install -e ".[dev]"  # 重新安装
```

### 问题：ModuleNotFoundError: No module named 'rich'

**解决方案**:
```bash
pip install rich prompt-toolkit click
```

### 问题：配置文件不存在

**解决方案**:
```bash
ai-cli --init  # 初始化配置
```

---

## 📚 更多信息

- **原项目**: `/mnt/c/Projects/AIStudio/AI-CLI` (PowerShell 版本)
- **新项目**: `/mnt/c/Projects/AIStudio/ai-cli-multi-platform` (Python 版本)
- **设计文档**: `AI-CLI/docs/PYTHON-MIGRATION-ANALYSIS.md`
- **任务清单**: `TASK-CHECKLIST.md`
- **完成报告**: `PROJECT-COMPLETION-REPORT.md`

---

## 🎉 开始使用

```bash
# 1. 安装
pip install -e ".[dev]"

# 2. 初始化
ai-cli --init

# 3. 配置
ai-cli --config

# 4. 运行
ai-cli
```

**享受你的 AI 编程助手！** 🚀
