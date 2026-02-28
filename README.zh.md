# AI CLI Launcher (AI 编程工作台启动器)

> 🌐 [English](README.md) | **中文** | [日本語](README.ja.md)

## 1. 简介

**AI CLI Launcher** 是一款基于 PowerShell 编写的轻量级终端启动工具。它专为现代 AI 辅助编程场景设计，旨在统一管理和快速启动各类 AI CLI 工具（如 `kiro-cli`, `Claude Code`, `Kimi CLI`, `Cursor Agent`, `OpenCode` 等）。

该工具打破了 Windows 原生环境与 Windows Subsystem for Linux (WSL) 之间的环境壁垒，允许开发者在一个统一的终端界面中选择目标项目，并一键唤起对应的 AI 编程工具，自动完成路径转换与终端环境初始化。

> 📚 **查看支持的工具**: 详细的工具列表、安装说明和对比请参考 [docs/TOOLS.zh.md](docs/TOOLS.zh.md)

### 🎯 为什么选择 AI-CLI？

**对于使用多个 AI 编程助手的开发者**，AI-CLI 解决了这些痛点：

✅ **告别记忆命令** - 一个 `ai-cli` 命令替代 8+ 个工具专用命令  
✅ **Windows ↔ WSL 无缝切换** - 自动路径转换，无需手动翻译  
✅ **Git Worktree 智能支持** - 自动检测分支，即时切换工作树实现并行开发  
✅ **环境变量自动注入** - 项目专属环境变量自动加载，告别手动 `export`  
✅ **多标签工作流** - `Ctrl+Enter` 并行启动多个 AI 工具，动态标签名称便于管理  

**实际效果**：从打开终端 → 导航路径 → 设置环境变量 → 启动工具（2-3 分钟）缩短到 **3 次按键**（↓ Enter Enter）。

## 2. 核心特性

* **🤖 智能双轨探测**：启动时后台异步检测 Windows 和 WSL 环境中的 AI CLI 工具，界面立即响应，检测完成后自动更新。
* **📂 统一项目管理**：通过 `config.json` 集中管理项目路径，支持跨盘符、跨环境。
* **🔄 跨环境路径转换**：内置路径转化引擎，自动将 Windows 绝对路径（如 `C:\Projects\...`）转化为符合 WSL 规范的挂载路径（如 `/mnt/c/Projects/...`）。
* **⚡ 纯终端交互**：快速键盘驱动的 CLI 界面，无 GUI 加载延迟，即时响应。
* **🔁 循环启动模式**：程序不退出，支持连续选择工具和项目，提升工作效率。
* **📑 多页签支持**：Ctrl+Enter 在 Windows Terminal 新页签中启动工具，方便多任务管理。
* **🛠️ 工具安装功能**：按 I 键快速安装未安装的 AI CLI 工具，安装后自动添加到 PATH 环境变量。
* **🔄 手动刷新功能**：按 R 键手动刷新工具列表，方便验证工具安装状态。
* **🏷️ 动态页签命名**：启动时通过 ANSI 转义序列和 Windows 原生指令，动态修改终端页签标题（如 `KIRO-CLI BT2400`），极大提升多任务管理的清晰度。

---

## 3. 安装与配置指南

### 3.1 环境要求

* 操作系统：Windows 10 / Windows 11
* 运行环境：PowerShell 5.1 或更高版本
* 依赖组件：已安装并配置好 WSL（如需使用 Linux 下的工具）

### 3.2 快速安装（推荐）

项目提供了自动安装脚本，只需运行以下命令即可完成安装：

```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

安装脚本会自动：
1. 从 GitHub 下载最新版本（包含图标文件）
2. 将程序文件复制到 `%LOCALAPPDATA%\AI-CLI` 目录
3. 创建桌面快捷方式（带自定义图标）
4. 添加到系统 PATH 环境变量

安装完成后，您可以通过以下方式启动：
- 双击桌面上的 "AI-CLI" 快捷方式
- 在命令行中运行 `ai-cli`（需重新打开终端）

**常用命令：**
```powershell
ai-cli           # 启动交互式界面
ai-cli --help    # 查看帮助信息
ai-cli --init    # 初始化配置
ai-cli --config  # 编辑配置
```

**卸载命令：**
```powershell
ai-cli -Uninstall
```

如果尚未添加到 PATH，可使用以下方式卸载：
```powershell
& "$env:LOCALAPPDATA\AI-CLI\ai-cli.ps1" -Uninstall
```

**参数说明**：支持 `-` 和 `--` 两种参数前缀，例如 `-Init` 和 `--init` 等效（不区分大小写）。

### 3.3 手动部署步骤

**第一步：克隆或下载项目**
```powershell
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI
```

**第二步：初始化配置**
```powershell
.\ai-cli.ps1 -Init
```

这将在用户配置目录（`%APPDATA%\AI-CLI\config.json`）创建配置文件。如果程序目录存在默认配置，会自动复制；否则创建新配置。

您可以手动编辑配置文件添加项目：

```json
{
  "projects": [
    {
      "name": "项目名称",
      "path": "C:\\Projects\\MyProject",
      "description": "项目描述（可选）"
    }
  ]
}
```

**第三步：运行程序**
```powershell
.\ai-cli.ps1
```

**查看帮助**
```powershell
.\ai-cli.ps1 --help
```

---

## 4. 使用说明

### 4.1 启动与界面说明

运行 `ai-cli` 后，将进入纯终端交互界面：

#### 项目选择界面（树状结构）
```
=== 选择项目 ===
> 📁 前端项目 (3 item(s))
  📁 后端项目 (2 item(s))
  📄 独立项目 (C:\Projects\standalone)

[↑↓] 选择  [Enter] 进入/确认  [N] 新增  [D] 删除  [Q] 退出
```

进入文件夹后：
```
  Home > 前端项目

=== 选择项目 ===
> 📄 Vue 项目 (C:\Projects\vue-app)
  📁 React 项目 (2 item(s))
  📄 Angular 项目 (C:\Projects\angular-app)

[↑↓] 选择  [Enter] 进入/确认  [N] 新增  [D] 删除  [Esc] 返回  [Q] 退出
```

#### 工具选择界面
```
=== 选择 AI 工具 (项目：项目 1) ===
> [WSL] kiro-cli
  [Win] claude
  [WSL] opencode
  [Win] aider

[↑↓] 选择  [Enter] 启动  [Ctrl+Enter] 新页签  [I] 安装  [R] 刷新  [Esc] 返回  [Q] 退出
```

#### 新增界面（类型选择）
```
=== 选择类型 ===
> 📄 Project
  📁 Folder

[↑↓] 选择  [Enter] 确认  [Esc] 取消
```

#### 删除确认界面
```
=== 删除确认 ===
项目名称：MyProject_

项目名称：MyProject
项目路径：C:\Projects\MyProject
环境变量 (可选，按 Enter 跳过):
  格式：KEY=VALUE，每行一个，空行结束
  Env Var: API_KEY=sk-xxx
    已添加：API_KEY=sk-xxx
将要删除：📁 前端项目 (包含 5 个子项)

⚠️  警告：此操作不可恢复！
请输入名称以确认删除：前端项目_

[输入名称] 确认  [Esc] 取消
```

### 4.2 快捷键

#### 项目选择界面
- `↑↓` - 导航选择
- `Enter` - 进入文件夹或选择项目
- `N` - 新增项目或文件夹
- `D` - 删除项目或文件夹
- `Esc` - 返回上级文件夹
- `Q` - 退出程序

#### 工具选择界面
- `↑↓` - 导航选择
- `Enter` - 在新窗口启动工具
- `Ctrl+Enter` - 在新页签启动工具（需要 Windows Terminal）
- `I` - 安装新工具
- `Esc` - 返回项目选择
- `Q` - 退出程序

#### 新增界面
- 输入项目名称（必填，不能重复）
- 输入项目路径（必填，自动检测路径是否存在）
- 输入环境变量（可选，格式：KEY=VALUE）
- 确认添加或取消

### 4.3 树状结构管理

项目支持树状结构组织：
- **文件夹**：用于分类管理项目，可以包含项目和子文件夹
- **项目**：实际的工作目录，包含路径和环境变量
- **面包屑导航**：显示当前位置，方便多层级导航
- **递归删除**：删除文件夹时会提示包含的子项数量

### 4.4 运行效果

* 脚本会自动拉起对应的终端（Cmd 或 WSL）。
* 终端会自动 `cd` 进入所选项目的对应路径。
* 项目配置的环境变量会自动注入到运行环境中。
  * **智能路径转换**：WSL 环境下，Windows 路径格式的环境变量值（如 `C:\Projects\...`）会自动转换为 WSL 路径格式（`/mnt/c/Projects/...`）。
* 终端顶部页签名称会自动变更为 `[工具名] [项目名]`，方便多开辨识。

---

## 5. 技术架构与实现原理

### 5.1 树状结构实现

项目配置采用递归树状结构：
```json
{
  "projects": [
    {
      "type": "folder",
      "name": "前端项目",
      "children": [
        {
          "type": "project",
          "name": "Vue 项目",
          "path": "C:\\Projects\\vue-app"
        }
      ]
    }
  ]
}
```

- 自动迁移旧版本平面配置到树状结构
- 支持递归遍历、添加、删除操作
- 面包屑导航跟踪当前路径

### 5.2 路径解析引擎 (`ConvertTo-WslPath`)

利用正则表达式 `^([a-zA-Z]):(.*)` 捕获 Windows 盘符，将其转化为 `/mnt/盘符小写` 格式，并将反斜杠 `\` 统一替换为正斜杠 `/`，确保 WSL 能够正确挂载和访问 Windows 文件系统。

### 5.3 工具检测机制

* **Windows 环境**：使用 PowerShell 内置 cmdlet `Get-Command -ErrorAction SilentlyContinue` 进行低开销静默探测。
* **WSL 环境**：通过 `wsl.exe -e bash -ic "command -v tool"` 执行检测，使用 `-ic` 参数确保加载 `.bashrc` 环境变量。

### 5.4 终端拉起与进程分发

根据工具环境标志（`[Win]` / `[WSL]`），执行不同策略：

* **针对 WSL**：
组合使用 `-e bash -ic` 确保加载完整的 Linux 环境变量（解决诸如 `command not found` 的问题），并利用 `echo -ne '\033]0;TITLE\007'` 发送 ANSI 序列设置终端标题。
* **针对 Windows**：
利用 `cmd.exe /k` 保持控制台窗口打开，通过 `title` 指令修改标题，利用 `cd /d` 实现安全的跨盘符目录切换。

---

## 6. 工具安装功能

### 6.1 使用方法

在工具选择界面按 `I` 键，进入工具安装界面：

```
=== 安装 AI 工具 ===
> [WSL] kiro-cli
  [Win] gemini
  [WSL] cursor-agent

[↑↓] 选择  [Enter] 安装  [Esc] 返回  [Q] 退出
```

选择要安装的工具，按 Enter 确认，程序会自动执行安装命令。

### 6.2 支持的工具

根据 `config.json` 配置，当前支持安装 8 个主流 AI CLI 工具。详细信息请参考 [docs/TOOLS.zh.md](docs/TOOLS.zh.md) 和 [docs/INSTALL-GUIDE.zh.md](docs/INSTALL-GUIDE.zh.md)。

---

## 7. 配置文件说明

配置文件位置：`%APPDATA%\AI-CLI\config.json`（通常为 `C:\Users\<用户名>\AppData\Roaming\AI-CLI\config.json`）

**配置优先级**：
1. 优先读取用户配置目录的 `config.json`
2. 如果不存在，则读取程序目录的默认 `config.json`
3. 所有修改都保存到用户配置目录

**注意**：配置文件与程序分离存储，卸载程序时配置不会丢失。

### 7.1 config.json 结构

```json
{
  "projects": [
    {
      "name": "项目名称",
      "path": "项目路径",
      "description": "项目描述（可选）",
      "env": {
        "API_KEY": "your-api-key",
        "DEBUG": "true"
      }
    }
  ],
  "tools": [
    {
      "name": "工具命令",
      "displayName": "显示名称",
      "winInstall": "Windows 安装命令或 null",
      "wslInstall": "WSL 安装命令或 null",
      "checkCommand": "检测命令",
      "url": "官方网站"
    }
  ],
  "settings": {
    "language": "auto",
    "defaultEnv": "wsl",
    "terminalEmulator": "default"
  }
}
```

### 7.2 添加项目

编辑 `config.json`，在 `projects` 数组中添加：

```json
{
  "name": "MyProject",
  "path": "C:\\Projects\\MyProject",
  "description": "我的项目"
}
```

### 7.3 添加自定义工具

编辑 `config.json`，在 `tools` 数组中添加：

```json
{
  "name": "mytool",
  "displayName": "My Tool",
  "winInstall": "npm install -g mytool",
  "wslInstall": "npm install -g mytool",
  "checkCommand": "mytool --version",
  "url": "https://mytool.com"
}
```

---

## 8. 常见问题 (FAQ)

**Q1：如何添加新项目？**
编辑 `config.json` 文件，在 `projects` 数组中添加项目信息，或运行 `ai-cli -Init` 重新初始化配置。

**Q2：运行时提示找不到工具？**
1. 确认工具已正确安装
2. 检查 PATH 环境变量
3. 对于 WSL 工具，确认 WSL 环境已正确配置
4. 运行 `ai-cli` 重新检测工具

**Q3：WSL 启动后提示 `No such file or directory`？**
检查项目路径是否正确，确保该盘符（如 C 盘、D 盘）已经被 WSL 正常挂载。

**Q4：如何使用多页签功能？**
确保已安装 Windows Terminal，然后在工具选择界面按 `Ctrl+Enter` 启动工具。

**Q5：如何卸载？**
运行 `ai-cli -Uninstall` 或 `& "$env:LOCALAPPDATA\AI-CLI\ai-cli.ps1" -Uninstall`。

---

## 9. 相关文档

- **[docs/TOOLS.zh.md](docs/TOOLS.zh.md)** - 8 个主流 AI CLI 工具的详细参考手册
- **[docs/INSTALL-GUIDE.zh.md](docs/INSTALL-GUIDE.zh.md)** - 工具安装功能使用指南
- **[docs/BUGFIX.zh.md](docs/BUGFIX.zh.md)** - Bug 修复记录和技术细节
- **[docs/CHANGELOG.zh.md](docs/CHANGELOG.zh.md)** - 版本更新日志

---

*最后更新：2026-02-26*
