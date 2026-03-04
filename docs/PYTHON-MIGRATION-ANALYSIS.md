# AI-CLI Python 迁移系统分析文档

> **文档版本**: v1.0  
> **创建日期**: 2026-03-01  
> **目标**: 将 PowerShell 实现的 AI-CLI 迁移至 Python 跨平台方案

---

## 📋 目录

1. [项目概述](#1-项目概述)
2. [现有系统分析](#2-现有系统分析)
3. [技术栈选型](#3-技术栈选型)
4. [系统架构设计](#4-系统架构设计)
5. [模块设计](#5-模块设计)
6. [数据模型](#6-数据模型)
7. [核心功能映射](#7-核心功能映射)
8. [跨平台兼容性](#8-跨平台兼容性)
9. [实施计划](#9-实施计划)
10. [风险评估](#10-风险评估)

---

## 1. 项目概述

### 1.1 当前状态

**AI-CLI** 是一个基于 PowerShell 的终端启动器，用于统一管理和快速启动多种 AI 编程工具（如 kiro-cli、Claude Code、Cursor Agent 等）。

**核心特性**：
- 🤖 双环境检测（Windows + WSL）
- 📂 树形项目管理
- 🔄 自动路径转换（Windows ↔ WSL）
- ⚡ 纯终端交互界面
- 📑 多标签支持（Windows Terminal）
- 🌳 Git Worktree 集成

**技术债务**：
- 仅支持 Windows 平台
- 依赖 PowerShell 5.1+
- WSL 特定逻辑耦合度高
- 跨平台扩展困难

### 1.2 迁移目标

**主要目标**：
1. ✅ 支持 Windows / Linux / macOS 三大平台
2. ✅ 统一的用户体验和交互逻辑
3. ✅ 保留所有现有功能（**包括 Windows WSL 双环境支持**）
4. ✅ 提升启动速度和响应性能
5. ✅ 简化安装和分发流程

**非目标**：
- ❌ 不改变配置文件格式（保持 JSON）
- ❌ 不改变用户交互流程
- ❌ 不增加新功能（迁移阶段）

**关键约束**：
- ⚠️ **必须保留 Windows 平台的 WSL 双环境支持**
- ⚠️ Windows 用户需要能同时检测和启动 Windows 原生工具和 WSL 工具
- ⚠️ 自动路径转换功能必须保留（C:\ ↔ /mnt/c）

---

## 2. 现有系统分析

### 2.1 代码结构分析

**文件组成**：
```
AI-CLI/
├── ai-cli.ps1          # 主程序 (2000+ 行)
├── install.ps1         # 安装脚本
├── config.json         # 默认配置
├── lang/               # 多语言支持
│   ├── en-US.ps1
│   ├── zh-CN.ps1
│   ├── ja-JP.ps1
│   └── de-DE.ps1
└── docs/               # 文档
```

**核心函数统计**：
| 函数名 | 功能 | 代码行数 | 复杂度 |
|--------|------|----------|--------|
| `Start-InteractiveLauncher` | 主交互循环 | ~150 | 高 |
| `Show-Menu` | 菜单渲染 | ~70 | 中 |
| `Get-UserSelection` | 键盘输入处理 | ~60 | 高 |
| `Start-DevSession` | 启动终端会话 | ~90 | 高 |
| `Get-AvailableTools` | 工具检测 | ~50 | 中 |
| `ConvertTo-WslPath` | 路径转换 | ~10 | 低 |
| `Get-GitWorktrees` | Git Worktree 检测 | ~80 | 中 |

### 2.2 功能模块分解

#### 模块 1: 配置管理
- 配置文件读取/写入
- 树形结构迁移（旧版扁平 → 新版树形）
- 用户配置目录管理
- 工具缓存更新

#### 模块 2: 工具检测
- Windows 环境检测（`Get-Command`）
- WSL 环境检测（`wsl.exe -e bash -ic`）
- 后台异步检测（PowerShell Job）
- 工具安装状态缓存

#### 模块 3: 交互式 UI
- 树形菜单导航
- 面包屑导航
- 键盘事件处理（↑↓ Enter Esc Ctrl+Enter）
- 输入框（带占位符和取消支持）
- 删除确认对话框

#### 模块 4: 项目管理
- 树形结构 CRUD
- 递归遍历和展平
- 项目路径验证
- 环境变量管理

#### 模块 5: 终端启动
- Windows: `cmd.exe` / Windows Terminal
- WSL: `wsl.exe -e bash`
- 路径转换（Windows → WSL）
- 环境变量注入
- 标签页标题设置

#### 模块 6: Git 集成
- Worktree 检测
- 分支状态（ahead/behind）
- 快速切换 Worktree

### 2.3 依赖关系图

```
┌─────────────────────────────────────┐
│   Start-InteractiveLauncher (主循环) │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐  ┌────▼─────────┐
│ Show-Menu   │  │ Get-UserSel  │
└──────┬──────┘  └────┬─────────┘
       │               │
       └───────┬───────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼────┐ ┌──▼──────┐
│ 项目   │ │ 工具   │ │ 启动    │
│ 管理   │ │ 检测   │ │ 会话    │
└────────┘ └────────┘ └─────────┘
```

---

## 3. 技术栈选型

### 3.1 核心依赖

| 库名 | 版本 | 用途 | 理由 |
|------|------|------|------|
| **rich** | 13.7+ | 终端 UI 渲染 | 强大的样式和布局能力 |
| **prompt_toolkit** | 3.0+ | 交互式输入 | 专业的键盘事件处理 |
| **click** | 8.1+ | CLI 参数解析 | 业界标准，易用性高 |
| **pyyaml** | 6.0+ | 配置文件（可选） | 支持 JSON/YAML |
| **gitpython** | 3.1+ | Git 操作 | 纯 Python Git 库 |

### 3.2 标准库使用

```python
import os              # 路径和环境变量
import sys             # 平台检测
import json            # 配置文件
import subprocess      # 进程启动
import shutil          # 工具检测 (which)
import pathlib         # 现代路径处理
import asyncio         # 异步工具检测
from dataclasses import dataclass  # 数据模型
from typing import Optional, List, Dict
```

### 3.3 可选增强

- **platformdirs**: 跨平台配置目录
- **psutil**: 进程管理（检测终端类型）
- **typer**: 替代 click（更现代的 API）

---

## 4. 系统架构设计

### 4.1 分层架构

```
┌─────────────────────────────────────────┐
│         CLI Entry Point (main.py)       │  ← click 命令行接口
├─────────────────────────────────────────┤
│      Application Layer (app.py)         │  ← 主交互循环
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ UI Layer │  │ Business │  │ Config ││  ← 业务逻辑层
│  │ (ui.py)  │  │ (core.py)│  │(cfg.py)││
│  └──────────┘  └──────────┘  └────────┘│
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Tools    │  │ Projects │  │  Git   ││  ← 领域模型层
│  │(tools.py)│  │(proj.py) │  │(git.py)││
│  └──────────┘  └──────────┘  └────────┘│
├─────────────────────────────────────────┤
│      Platform Abstraction (platform.py) │  ← 平台适配层
├─────────────────────────────────────────┤
│      Utilities (utils.py, models.py)    │  ← 工具和数据模型
└─────────────────────────────────────────┘
```

### 4.2 目录结构

```
ai-cli/
├── ai_cli/                    # 主包
│   ├── __init__.py
│   ├── __main__.py           # 入口点 (python -m ai_cli)
│   ├── cli.py                # Click 命令定义
│   ├── app.py                # 主应用逻辑
│   ├── config.py             # 配置管理
│   ├── models.py             # 数据模型
│   ├── ui/                   # UI 组件
│   │   ├── __init__.py
│   │   ├── menu.py           # 菜单渲染
│   │   ├── input.py          # 输入处理
│   │   └── theme.py          # 主题配置
│   ├── core/                 # 核心业务
│   │   ├── __init__.py
│   │   ├── tools.py          # 工具检测
│   │   ├── projects.py       # 项目管理
│   │   ├── session.py        # 会话启动
│   │   └── git.py            # Git 集成
│   ├── platform/             # 平台适配
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象基类
│   │   ├── windows.py        # Windows 实现
│   │   ├── linux.py          # Linux 实现
│   │   └── macos.py          # macOS 实现
│   └── utils.py              # 工具函数
├── tests/                    # 测试
│   ├── test_config.py
│   ├── test_tools.py
│   └── test_ui.py
├── pyproject.toml            # 项目配置
├── README.md
└── LICENSE
```

### 4.3 数据流图

```
用户输入
   │
   ▼
┌──────────────┐
│ CLI Parser   │ (click)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ App.run()    │ ← 主循环
└──────┬───────┘
       │
   ┌───┴────┐
   │        │
   ▼        ▼
┌─────┐  ┌─────┐
│ UI  │  │Core │
└──┬──┘  └──┬──┘
   │        │
   │    ┌───┴────┐
   │    │        │
   │    ▼        ▼
   │  ┌────┐  ┌────┐
   │  │Tool│  │Proj│
   │  └────┘  └────┘
   │
   ▼
┌──────────────┐
│ Platform     │ ← 启动终端
└──────────────┘
```

---

## 5. 模块设计

### 5.1 配置管理模块 (config.py)

**职责**：
- 加载/保存配置文件
- 配置迁移（扁平 → 树形）
- 跨平台配置路径

**核心类**：
```python
@dataclass
class Config:
    projects: List[ProjectNode]
    tools: List[ToolConfig]
    settings: Settings
    
    @classmethod
    def load(cls) -> 'Config':
        """从配置文件加载"""
        
    def save(self) -> None:
        """保存到配置文件"""
        
    def migrate_legacy(self) -> None:
        """迁移旧版配置"""
```

**配置路径逻辑**：
```python
def get_config_dir() -> Path:
    if sys.platform == 'win32':
        return Path(os.environ['APPDATA']) / 'AI-CLI'
    else:
        return Path.home() / '.config' / 'ai-cli'
```

### 5.2 工具检测模块 (tools.py)

**职责**：
- 检测已安装工具
- 异步并发检测
- 缓存检测结果

**核心函数**：
```python
async def detect_tools(tools_config: List[ToolConfig]) -> List[Tool]:
    """异步检测所有工具"""
    tasks = [detect_single_tool(t) for t in tools_config]
    return await asyncio.gather(*tasks)

def is_tool_available(command: str) -> bool:
    """检查工具是否可用"""
    return shutil.which(command) is not None
```

**PowerShell 对比**：
| PowerShell | Python |
|------------|--------|
| `Get-Command -ErrorAction SilentlyContinue` | `shutil.which(cmd)` |
| `wsl.exe -e bash -ic "command -v tool"` | 移除（Linux 原生运行） |
| PowerShell Job | `asyncio.gather()` |

### 5.3 UI 模块 (ui/menu.py)

**职责**：
- 渲染树形菜单
- 处理键盘事件
- 面包屑导航

**核心类**：
```python
class Menu:
    def __init__(self, items: List, title: str):
        self.items = items
        self.selected = 0
        
    def render(self) -> None:
        """使用 rich 渲染菜单"""
        
    def handle_key(self, key: str) -> Optional[Action]:
        """处理键盘输入"""
```

**rich 渲染示例**：
```python
from rich.console import Console
from rich.table import Table

def render_menu(items, selected):
    console = Console()
    table = Table(show_header=False, box=None)
    
    for i, item in enumerate(items):
        icon = "📁" if item.is_folder else "📄"
        style = "green" if i == selected else "white"
        prefix = ">" if i == selected else " "
        table.add_row(f"{prefix} {icon} {item.name}", style=style)
    
    console.print(table)
```

### 5.4 项目管理模块 (projects.py)

**职责**：
- 树形结构 CRUD
- 递归遍历
- 路径验证

**核心类**：
```python
@dataclass
class ProjectNode:
    type: str  # "project" | "folder"
    name: str
    path: Optional[str] = None
    children: List['ProjectNode'] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    
    def add_child(self, node: 'ProjectNode') -> None:
        """添加子节点"""
        
    def remove_child(self, name: str) -> bool:
        """删除子节点"""
        
    def flatten(self) -> List['ProjectNode']:
        """展平为列表（用于显示）"""
```

### 5.5 会话启动模块 (session.py)

**职责**：
- 启动终端会话
- 环境变量注入
- 标题设置

**核心函数**：
```python
def start_session(
    tool: str,
    project_path: str,
    env_vars: Dict[str, str],
    platform: PlatformAdapter,
    use_tab: bool = False
) -> None:
    """启动开发会话"""
    
    # 构建命令
    cmd = platform.build_command(tool, project_path, env_vars)
    
    # 启动进程
    if use_tab:
        platform.launch_in_tab(cmd, title=f"{tool} - {project_path}")
    else:
        platform.launch_in_window(cmd)
```

---

## 6. 数据模型

### 6.1 核心数据类

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class NodeType(Enum):
    PROJECT = "project"
    FOLDER = "folder"

@dataclass
class ProjectNode:
    """项目树节点"""
    type: NodeType
    name: str
    path: Optional[str] = None
    children: List['ProjectNode'] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None

@dataclass
class ToolConfig:
    """工具配置"""
    name: str
    display_name: str
    win_install: Optional[str]
    linux_install: Optional[str]
    macos_install: Optional[str]
    check_command: str
    url: str

@dataclass
class Tool:
    """检测到的工具"""
    name: str
    display_name: str
    available: bool
    version: Optional[str] = None

@dataclass
class Settings:
    """全局设置"""
    language: str = "auto"
    terminal_emulator: str = "default"
    theme: str = "default"

@dataclass
class Config:
    """完整配置"""
    projects: List[ProjectNode]
    tools: List[ToolConfig]
    settings: Settings
```

### 6.2 配置文件格式

**保持与 PowerShell 版本兼容**：
```json
{
  "projects": [
    {
      "type": "folder",
      "name": "Frontend Projects",
      "children": [
        {
          "type": "project",
          "name": "Vue App",
          "path": "/home/user/projects/vue-app",
          "env": {
            "API_KEY": "xxx"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "winInstall": null,
      "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "macosInstall": "brew install kiro-cli",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    }
  ],
  "settings": {
    "language": "auto",
    "terminalEmulator": "default"
  }
}
```

---

*（文档第一部分完成，包含 1-6 章节）*

## 7. 核心功能映射

### 7.1 配置管理

| PowerShell 实现 | Python 实现 | 说明 |
|----------------|-------------|------|
| `Get-Content $path \| ConvertFrom-Json` | `json.load(open(path))` | JSON 解析 |
| `$config \| ConvertTo-Json \| Set-Content` | `json.dump(config, open(path, 'w'))` | JSON 保存 |
| `Join-Path $env:APPDATA "AI-CLI"` | `platformdirs.user_config_dir("ai-cli")` | 配置目录 |
| `Test-Path $path` | `Path(path).exists()` | 路径检测 |

**Python 实现示例**：
```python
from pathlib import Path
import json
from platformdirs import user_config_dir

class ConfigManager:
    def __init__(self):
        self.config_dir = Path(user_config_dir("ai-cli"))
        self.config_file = self.config_dir / "config.json"
        
    def load(self) -> Config:
        if not self.config_file.exists():
            return self.create_default()
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Config.from_dict(data)
    
    def save(self, config: Config) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
```

### 7.2 工具检测

| PowerShell 实现 | Python 实现 | 说明 |
|----------------|-------------|------|
| `Get-Command $tool -EA SilentlyContinue` | `shutil.which(tool)` | Windows 原生检测 |
| `wsl.exe -e bash -ic "command -v $tool"` | `subprocess + wsl.exe` | **保留 WSL 检测** |
| `Start-Job -ScriptBlock {...}` | `asyncio.create_task()` | 异步检测 |
| `Receive-Job $job` | `await task` | 获取结果 |

**重要说明**: Windows 平台保留 WSL 双环境支持，详见 [WSL 支持文档](PYTHON-MIGRATION-WSL-SUPPORT.md)

**Python 实现示例**：
```python
import shutil
import asyncio
import subprocess
import sys

class ToolDetector:
    """跨平台工具检测器"""
    
    def __init__(self):
        self.is_windows = sys.platform == 'win32'
        self.wsl_available = self._check_wsl() if self.is_windows else False
    
    def _check_wsl(self) -> bool:
        """检测 WSL 是否可用"""
        try:
            result = subprocess.run(['wsl.exe', '--status'], capture_output=True, timeout=2)
            return result.returncode == 0
        except:
            return False

async def detect_tool(tool_config: ToolConfig) -> List[Tool]:
    """检测单个工具（可能返回多个环境）"""
    tools = []
    
    # Windows 原生检测
    if sys.platform == 'win32' and tool_config.win_install:
        if shutil.which(tool_config.name):
            tools.append(Tool(
                name=tool_config.name,
                display_name=tool_config.display_name,
                environment="windows",
                available=True
            ))
    
    # WSL 检测（仅 Windows）
    if sys.platform == 'win32' and tool_config.wsl_install:
        try:
            result = await asyncio.create_subprocess_exec(
                'wsl.exe', '-e', 'bash', '-ic', f'command -v {tool_config.name}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            if stdout.strip():
                tools.append(Tool(
                    name=tool_config.name,
                    display_name=tool_config.display_name,
                    environment="wsl",
                    available=True
                ))
        except:
            pass
    
    # Linux/macOS 原生检测
    if sys.platform != 'win32':
        if shutil.which(tool_config.name):
            tools.append(Tool(
                name=tool_config.name,
                display_name=tool_config.display_name,
                environment="native",
                available=True
            ))
    
    return tools

async def detect_all_tools(tools_config: List[ToolConfig]) -> List[Tool]:
    """并发检测所有工具"""
    tasks = [detect_tool(tc) for tc in tools_config]
    results = await asyncio.gather(*tasks)
    # 展平结果（每个工具可能有多个环境）
    return [tool for sublist in results for tool in sublist]
```

### 7.3 UI 渲染

| PowerShell 实现 | Python 实现 | 说明 |
|----------------|-------------|------|
| `Write-Host "text" -ForegroundColor Green` | `console.print("[green]text[/green]")` | 彩色输出 |
| `[Console]::CursorVisible = $false` | `console.show_cursor(False)` | 隐藏光标 |
| `Clear-Host` | `console.clear()` | 清屏 |
| `$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")` | `prompt_toolkit.key_binding` | 键盘输入 |

**Python 实现示例**：
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

class MenuRenderer:
    def __init__(self):
        self.console = Console()
        
    def render(self, items: List, selected: int, title: str, breadcrumb: List[str]):
        self.console.clear()
        
        # 面包屑
        if breadcrumb:
            path = " > ".join(["Home"] + breadcrumb)
            self.console.print(f"  {path}", style="dim")
        
        # 标题
        self.console.print(f"\n  {title}", style="cyan bold")
        self.console.print("  " + "=" * 60, style="dim")
        
        # 菜单项
        table = Table(show_header=False, box=None, padding=(0, 2))
        
        for i, item in enumerate(items):
            icon = "📁" if item.type == "folder" else "📄"
            prefix = ">" if i == selected else " "
            style = "green" if i == selected else "white"
            
            name = f"{prefix} {icon} {item.name}"
            if item.path:
                name += f" [dim]({item.path})[/dim]"
            
            table.add_row(name, style=style)
        
        self.console.print(table)
        
        # 提示
        self.console.print("\n  [dim][↑↓] Navigate  [Enter] Select  [Q] Quit[/dim]")
```

### 7.4 键盘输入处理

**PowerShell 实现**：
```powershell
$key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
switch ($key.VirtualKeyCode) {
    38 { $selected = [Math]::Max(0, $selected - 1) }  # Up
    40 { $selected = [Math]::Min($items.Count - 1, $selected + 1) }  # Down
    13 { return $items[$selected] }  # Enter
    27 { return $null }  # Esc
}
```

**Python 实现**：
```python
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout

class MenuController:
    def __init__(self, items: List):
        self.items = items
        self.selected = 0
        self.result = None
        
    def create_keybindings(self) -> KeyBindings:
        kb = KeyBindings()
        
        @kb.add('up')
        def _(event):
            self.selected = max(0, self.selected - 1)
            self.render()
        
        @kb.add('down')
        def _(event):
            self.selected = min(len(self.items) - 1, self.selected + 1)
            self.render()
        
        @kb.add('enter')
        def _(event):
            self.result = self.items[self.selected]
            event.app.exit()
        
        @kb.add('escape')
        def _(event):
            self.result = None
            event.app.exit()
        
        @kb.add('q')
        def _(event):
            event.app.exit()
        
        return kb
    
    def run(self):
        app = Application(
            key_bindings=self.create_keybindings(),
            full_screen=False
        )
        app.run()
        return self.result
```

### 7.5 终端启动

| PowerShell 实现 | Python 实现 | 说明 |
|----------------|-------------|------|
| `Start-Process cmd.exe -ArgumentList "/k ..."` | `subprocess.Popen(['cmd', '/k', ...])` | Windows 原生 |
| `Start-Process wsl.exe -ArgumentList "-e bash ..."` | `subprocess.Popen(['wsl.exe', '-e', 'bash', ...])` | **保留 WSL** |
| `Start-Process wt -ArgumentList "new-tab ..."` | `subprocess.Popen(['wt', 'new-tab', ...])` | 新标签 |

**Python 实现示例**：
```python
import subprocess
import sys
from abc import ABC, abstractmethod

class PlatformAdapter(ABC):
    @abstractmethod
    def launch_terminal(self, tool_env: str, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        pass

class WindowsAdapter(PlatformAdapter):
    """Windows 适配器 - 支持 Windows + WSL 双环境"""
    
    def launch_terminal(self, tool_env: str, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        if tool_env == "wsl":
            self._launch_wsl(command, cwd, env, title, use_tab)
        else:
            self._launch_windows(command, cwd, env, title, use_tab)
    
    def _launch_windows(self, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        """启动 Windows 原生会话"""
        env_setup = ' & '.join([f'set {k}={v}' for k, v in env.items()])
        full_cmd = f'title {title} & cd /d "{cwd}" & {env_setup} & {command}'
        
        if use_tab and shutil.which('wt'):
            subprocess.Popen(['wt', '-w', '0', 'new-tab', '--title', title, 'cmd', '/k', full_cmd])
        else:
            subprocess.Popen(['cmd', '/k', full_cmd])
    
    def _launch_wsl(self, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        """启动 WSL 会话"""
        # 路径转换
        wsl_path = self._to_wsl_path(cwd)
        
        # 环境变量转换（Windows 路径 → WSL 路径）
        wsl_env = {}
        for k, v in env.items():
            if ':' in v and v[1] == ':':  # 检测 Windows 路径
                wsl_env[k] = self._to_wsl_path(v)
            else:
                wsl_env[k] = v
        
        env_setup = ' && '.join([f'export {k}="{v}"' for k, v in wsl_env.items()])
        full_cmd = f"cd '{wsl_path}' && {env_setup} && {command}; exec bash"
        
        if use_tab and shutil.which('wt'):
            subprocess.Popen(['wt', '-w', '0', 'new-tab', '--title', title, 
                            'wsl', '-e', 'bash', '-ic', full_cmd])
        else:
            subprocess.Popen(['wsl.exe', '-e', 'bash', '-ic', full_cmd])
    
    @staticmethod
    def _to_wsl_path(win_path: str) -> str:
        """Windows 路径 → WSL 路径"""
        import re
        match = re.match(r'^([a-zA-Z]):\\(.*)$', win_path)
        if match:
            drive = match.group(1).lower()
            rest = match.group(2).replace('\\', '/')
            return f"/mnt/{drive}/{rest}"
        return win_path.replace('\\', '/')

class LinuxAdapter(PlatformAdapter):
    """Linux 适配器 - 仅原生环境"""
    
    def launch_terminal(self, tool_env: str, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        env_setup = ' && '.join([f'export {k}="{v}"' for k, v in env.items()])
        full_cmd = f'cd "{cwd}" && {env_setup} && {command}; exec bash'
        
        terminal = shutil.which('gnome-terminal') or shutil.which('konsole') or shutil.which('xterm')
        
        if terminal == 'gnome-terminal':
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', full_cmd])
        elif terminal == 'konsole':
            subprocess.Popen(['konsole', '-e', 'bash', '-c', full_cmd])
        else:
            subprocess.Popen(['xterm', '-e', 'bash', '-c', full_cmd])

class MacOSAdapter(PlatformAdapter):
    """macOS 适配器 - 仅原生环境"""
    
    def launch_terminal(self, tool_env: str, command: str, cwd: str, env: Dict, title: str, use_tab: bool):
        env_setup = ' && '.join([f'export {k}="{v}"' for k, v in env.items()])
        full_cmd = f'cd "{cwd}" && {env_setup} && {command}'
        
        script = f'tell application "Terminal" to do script "{full_cmd}"'
        subprocess.Popen(['osascript', '-e', script])

def get_platform_adapter() -> PlatformAdapter:
    if sys.platform == 'win32':
        return WindowsAdapter()
    elif sys.platform == 'darwin':
        return MacOSAdapter()
    else:
        return LinuxAdapter()
```

### 7.6 路径转换

**PowerShell 实现**：
```powershell
function ConvertTo-WslPath {
    param([string]$WinPath)
    $linuxPath = $WinPath -replace '\\', '/'
    if ($linuxPath -match '^([a-zA-Z]):(.*)') {
        $drive = $Matches[1].ToLower()
        return "/mnt/$drive" + $Matches[2]
    }
    return $linuxPath
}
```

**Python 实现（保留并增强）**：
```python
from pathlib import Path, PureWindowsPath, PurePosixPath
import sys
import re

class PathConverter:
    """跨平台路径转换器"""
    
    @staticmethod
    def to_wsl_path(windows_path: str) -> str:
        """Windows 路径 → WSL 路径 (C:\Projects\... → /mnt/c/Projects/...)"""
        match = re.match(r'^([a-zA-Z]):\\(.*)$', windows_path)
        if match:
            drive = match.group(1).lower()
            rest = match.group(2).replace('\\', '/')
            return f"/mnt/{drive}/{rest}".rstrip('/')
        return windows_path.replace('\\', '/')
    
    @staticmethod
    def to_windows_path(wsl_path: str) -> str:
        """WSL 路径 → Windows 路径 (/mnt/c/Projects/... → C:\Projects\...)"""
        match = re.match(r'^/mnt/([a-z])/(.*)$', wsl_path)
        if match:
            drive = match.group(1).upper()
            rest = match.group(2).replace('/', '\\')
            return f"{drive}:\\{rest}"
        return wsl_path
    
    @staticmethod
    def normalize_for_environment(path: str, environment: str) -> str:
        """根据目标环境规范化路径"""
        if environment == "wsl":
            # 如果是 Windows 路径，转换为 WSL 路径
            if ':' in path and path[1] == ':':
                return PathConverter.to_wsl_path(path)
        elif environment == "windows":
            # 如果是 WSL 路径，转换为 Windows 路径
            if path.startswith('/mnt/'):
                return PathConverter.to_windows_path(path)
        
        return path

# 使用示例
converter = PathConverter()

# Windows → WSL
wsl_path = converter.to_wsl_path("C:\\Projects\\MyApp")
# 结果: "/mnt/c/Projects/MyApp"

# WSL → Windows
win_path = converter.to_windows_path("/mnt/d/Code/test")
# 结果: "D:\\Code\\test"

# 自动转换
path = converter.normalize_for_environment("C:\\Projects\\MyApp", "wsl")
# 结果: "/mnt/c/Projects/MyApp"
```

**关键改进**：
- 保留完整的 Windows ↔ WSL 路径转换功能
- 支持环境变量中的路径自动转换
- 双向转换能力（原 PowerShell 版本仅单向）

### 7.7 Git Worktree 检测

**PowerShell 实现**：
```powershell
function Get-GitWorktrees {
    param([string]$projectPath)
    
    $output = git -C $projectPath worktree list --porcelain
    # 解析输出...
}
```

**Python 实现**：
```python
from git import Repo
from dataclasses import dataclass

@dataclass
class Worktree:
    path: str
    branch: str
    is_current: bool
    ahead: int = 0
    behind: int = 0

def get_worktrees(project_path: str) -> List[Worktree]:
    """获取 Git Worktree 列表"""
    try:
        repo = Repo(project_path)
        worktrees = []
        
        # 主 worktree
        main_branch = repo.active_branch.name
        worktrees.append(Worktree(
            path=str(repo.working_dir),
            branch=main_branch,
            is_current=True
        ))
        
        # 其他 worktrees
        for wt in repo.git.worktree('list', '--porcelain').split('\n\n'):
            lines = wt.strip().split('\n')
            if len(lines) < 2:
                continue
            
            path = lines[0].replace('worktree ', '')
            branch = lines[2].replace('branch refs/heads/', '') if len(lines) > 2 else 'detached'
            
            worktrees.append(Worktree(
                path=path,
                branch=branch,
                is_current=False
            ))
        
        return worktrees
    except:
        return []
```

---

## 8. 跨平台兼容性

### 8.1 平台差异对比

| 特性 | Windows | Linux | macOS | 解决方案 |
|------|---------|-------|-------|----------|
| 配置目录 | `%APPDATA%` | `~/.config` | `~/Library/Application Support` | `platformdirs` |
| 路径分隔符 | `\` | `/` | `/` | `pathlib.Path` |
| **WSL 支持** | **双环境 (Win+WSL)** | **不适用** | **不适用** | **WindowsAdapter 特殊处理** |
| 终端模拟器 | cmd / Windows Terminal | gnome-terminal / konsole | Terminal.app | 平台适配器 |
| 环境变量设置 | `set VAR=value` | `export VAR=value` | `export VAR=value` | 平台适配器 |
| 工具检测 | `where` + `wsl.exe` | `which` | `which` | `shutil.which()` + WSL 检测 |
| 新标签启动 | `wt new-tab` | 终端特定 | AppleScript | 平台适配器 |
| **路径转换** | **C:\ ↔ /mnt/c** | **不需要** | **不需要** | **PathConverter** |

**重要说明**：
- Windows 平台是唯一需要处理双环境的平台
- Linux/macOS 用户体验不受影响（无 WSL 概念）
- 路径转换仅在 Windows + WSL 场景下触发

### 8.2 配置目录处理

```python
import sys
from pathlib import Path

def get_config_dir() -> Path:
    """获取跨平台配置目录"""
    if sys.platform == 'win32':
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    elif sys.platform == 'darwin':
        base = Path.home() / 'Library' / 'Application Support'
    else:
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    
    return base / 'ai-cli'
```

### 8.3 终端检测

```python
def detect_terminal() -> str:
    """检测当前终端类型"""
    if sys.platform == 'win32':
        if os.environ.get('WT_SESSION'):
            return 'windows-terminal'
        return 'cmd'
    elif sys.platform == 'darwin':
        return 'terminal-app'
    else:
        # Linux: 检测常见终端
        for term in ['gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm']:
            if shutil.which(term):
                return term
        return 'xterm'
```

### 8.4 环境变量注入

```python
def build_env_command(env_vars: Dict[str, str]) -> str:
    """构建环境变量设置命令"""
    if sys.platform == 'win32':
        return ' & '.join([f'set {k}={v}' for k, v in env_vars.items()])
    else:
        return ' && '.join([f'export {k}="{v}"' for k, v in env_vars.items()])
```

### 8.5 路径验证

```python
def validate_project_path(path: str) -> bool:
    """验证项目路径是否存在"""
    try:
        p = Path(path)
        return p.exists() and p.is_dir()
    except:
        return False
```

---

## 9. 实施计划

### 9.1 开发阶段

#### 阶段 1: 基础架构 (2 天)
- [ ] 项目初始化（pyproject.toml, 目录结构）
- [ ] 数据模型定义（models.py）
- [ ] 配置管理（config.py）
- [ ] 单元测试框架搭建

**交付物**：
- 可加载/保存配置文件
- 通过所有配置相关测试

#### 阶段 2: 核心业务逻辑 (2 天)
- [ ] 工具检测模块（tools.py）
- [ ] 项目管理模块（projects.py）
- [ ] Git 集成（git.py）
- [ ] 平台适配器基类（platform/base.py）

**交付物**：
- 可检测已安装工具
- 可管理项目树结构
- 可检测 Git Worktree

#### 阶段 3: UI 实现 (2 天)
- [ ] 菜单渲染（ui/menu.py）
- [ ] 键盘输入处理（ui/input.py）
- [ ] 主题配置（ui/theme.py）
- [ ] 交互流程测试

**交付物**：
- 完整的交互式菜单
- 支持所有键盘快捷键

#### 阶段 4: 平台适配 (1.5 天)
- [ ] Windows 适配器（platform/windows.py）
- [ ] Linux 适配器（platform/linux.py）
- [ ] macOS 适配器（platform/macos.py）
- [ ] 终端启动测试

**交付物**：
- 三平台均可启动终端会话
- 环境变量正确注入

#### 阶段 5: CLI 接口 (0.5 天)
- [ ] Click 命令定义（cli.py）
- [ ] 主应用逻辑（app.py）
- [ ] 入口点配置（__main__.py）

**交付物**：
- 完整的 CLI 工具
- 支持所有命令行参数

#### 阶段 6: 测试与优化 (1 天)
- [ ] 集成测试
- [ ] 跨平台测试（Windows / Linux / macOS）
- [ ] 性能优化
- [ ] 文档完善

**交付物**：
- 通过所有测试
- 性能达标（启动 < 500ms）

### 9.2 时间线

```
Week 1:
  Mon-Tue: 阶段 1 (基础架构)
  Wed-Thu: 阶段 2 (核心逻辑)
  Fri:     阶段 3 开始 (UI)

Week 2:
  Mon:     阶段 3 完成 (UI)
  Tue:     阶段 4 (平台适配)
  Wed:     阶段 5 (CLI) + 阶段 6 开始
  Thu-Fri: 阶段 6 (测试优化) + 发布准备
```

**总工期**: 7-8 个工作日

### 9.3 里程碑

| 里程碑 | 日期 | 标准 |
|--------|------|------|
| M1: 配置可用 | Day 2 | 可加载/保存配置 |
| M2: 工具检测 | Day 4 | 可检测所有工具 |
| M3: UI 完成 | Day 6 | 可交互式选择 |
| M4: 跨平台 | Day 7 | 三平台可运行 |
| M5: 发布 | Day 8 | 通过所有测试 |

---

## 10. 风险评估

### 10.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 终端兼容性问题 | 中 | 高 | 提前在多个终端测试 |
| 键盘输入处理复杂 | 中 | 中 | 使用成熟库（prompt_toolkit） |
| Git 库性能问题 | 低 | 中 | 使用 subprocess 替代 GitPython |
| 跨平台路径问题 | 低 | 高 | 使用 pathlib 统一处理 |

### 10.2 兼容性风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 配置文件不兼容 | 低 | 高 | 保持 JSON 格式不变 |
| 用户习惯改变 | 低 | 中 | 保持交互流程一致 |
| 旧版本迁移 | 中 | 中 | 提供迁移脚本 |

### 10.3 性能风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 启动速度慢 | 低 | 中 | 异步工具检测 + 缓存 |
| UI 渲染卡顿 | 低 | 低 | 使用 rich 优化渲染 |
| 大量项目时性能下降 | 中 | 低 | 虚拟滚动 + 分页 |

### 10.4 依赖风险

| 依赖 | 风险 | 缓解措施 |
|------|------|----------|
| rich | 版本更新可能破坏 API | 锁定版本范围 |
| prompt_toolkit | 学习曲线陡峭 | 提前原型验证 |
| GitPython | 性能问题 | 可降级为 subprocess |

---

## 11. 附录

### 11.1 依赖清单

```toml
[project]
name = "ai-cli"
version = "3.0.0"
description = "Cross-platform AI CLI launcher"
requires-python = ">=3.8"

dependencies = [
    "rich>=13.7.0",
    "prompt-toolkit>=3.0.0",
    "click>=8.1.0",
    "platformdirs>=4.0.0",
    "gitpython>=3.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
ai-cli = "ai_cli.cli:main"
```

### 11.2 开发环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black ai_cli/

# 类型检查
mypy ai_cli/
```

### 11.3 打包与分发

```bash
# 构建
python -m build

# 发布到 PyPI
python -m twine upload dist/*

# 用户安装
pip install ai-cli
# 或
pipx install ai-cli
```

---

**文档结束**

*最后更新: 2026-03-01*  
*作者: AI-CLI 开发团队*  
*版本: 1.0*
