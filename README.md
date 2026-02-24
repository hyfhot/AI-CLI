# AI CLI Launcher (AI 编程工作台启动器)

## 多语言支持

本工具支持 **English**, **中文**, **日本語**, **Deutsch** 四种语言。

- **自动检测**：启动时自动根据系统语言环境选择对应语言
- **手动切换**：在界面右上角的下拉框中可随时切换语言

---

## 1. 简介

**AI CLI Launcher** 是一款基于 PowerShell 编写的轻量级桌面可视化启动工具。它专为现代 AI 辅助编程场景设计，旨在统一管理和快速启动各类 AI CLI 工具（如 `kiro-cli`, `Claude Code`, `Kimi CLI`, `Cursor`, `OpenCode` 等）。

该工具打破了 Windows 原生环境与 Windows Subsystem for Linux (WSL) 之间的环境壁垒，允许开发者在一个统一的图形界面中选择目标项目，并一键唤起对应的 AI 编程工具，自动完成路径转换与终端环境初始化。

## 2. 核心特性

* **🤖 智能双轨探测**：启动时自动侦测 Windows 宿主机与 WSL 环境中已安装的 AI CLI 工具，并分类打上 `[Win]` 或 `[WSL]` 标签。
* **📂 统一项目管理**：通过全局环境变量 `AI_PROJECTS` 集中管理项目路径，支持跨盘符、跨环境。
* **🔄 跨环境路径转换**：内置路径转化引擎，自动将 Windows 绝对路径（如 `C:\Projects\...`）转化为符合 WSL 规范的挂载路径（如 `/mnt/c/Projects/...`）。
* **🎨 可视化无感交互**：原生 WinForms 极简 UI，支持鼠标双击快启；底层屏蔽 PowerShell 黑框，实现无缝沉浸式启动。
* **🏷️ 动态页签命名**：启动时通过 ANSI 转义序列和 Windows 原生指令，动态修改终端页签标题（如 `KIRO-CLI BT2400`），极大提升多任务管理的清晰度。
* **⌨️ 自定义工具输入**：下拉列表不仅支持选择探测到的工具，更支持用户手动输入任意临时安装的 CLI 指令。

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

或者使用更简短的方式：

```powershell
iwr https://bit.ly/ai-cli-install | iex
```

安装脚本会自动：
1. 从 GitHub 下载最新版本
2. 将程序文件复制到 `%LOCALAPPDATA%\AI-CLI` 目录
3. 创建桌面快捷方式（带图标）
4. 创建开始菜单快捷方式
5. 添加到系统 PATH 环境变量

安装完成后，您可以通过以下方式启动：
- 双击桌面上的 "AI-CLI" 快捷方式
- 从开始菜单中选择 "AI-CLI"
- 在命令行中运行 `ai-cli`（需重新打开终端）

**卸载命令：**
```powershell
ai-cli --uninstall
```

或者重新运行安装脚本：
```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/main/install.ps1 | iex -Uninstall
```

### 3.3 手动部署步骤

**第一步：保存脚本文件**
将核心脚本代码保存为 `.ps1` 文件。例如，存放在 `C:\Scripts\Launcher.ps1`。

**第二步：配置项目环境变量**
在 Windows 系统中新增一个名为 `AI_PROJECTS` 的用户环境变量。

* **格式规范**：`项目名称=项目绝对路径;项目名称2=项目绝对路径2;`
* **配置示例**：
```text
BT2400=c:\Work\RS\source\Qualcomm\BT2400\;Headset-984=c:\Projects\Qualcomm\Headset\Headset-984\;

```


*(注：路径末尾是否带斜杠均可，支持 Windows 格式。)*

**第三步：创建桌面快捷方式**

1. 在桌面右键 -> **新建** -> **快捷方式**。
2. 在“对象的位置”中输入以下无黑框启动命令（请替换为您的实际脚本路径）：
```cmd
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Scripts\Launcher.ps1"

```


3. 命名为“AI 编程工作台”，并可为其分配专属图标。

---

## 4. 使用说明

### 4.1 启动与界面说明

双击桌面快捷方式后，将弹出“AI 编程工作台”主界面：

1. **AI 编程工具 (下拉框)**：
* 列表会自动展示系统已安装的工具。
* 带有 `[Win]` 前缀的工具将在 Windows CMD 中原生运行。
* 带有 `[WSL]` 前缀的工具将在 WSL Bash 环境中运行。
* **进阶用法**：如果列表未包含您刚安装的工具，您可以直接在下拉框中**键盘输入**工具名。以 `[Win]` 开头强制走 Windows 环境，不带前缀默认走 WSL 环境。


2. **选择目标项目 (列表框)**：
* 粗体显示项目名称，灰色弱化显示实际物理路径。
* 选中目标项目后，点击**启动工作台**，或直接**双击列表项**即可极速启动。



### 4.2 运行效果

* 脚本会自动拉起对应的终端（Cmd 或 WSL）。
* 终端会自动 `cd` 进入所选项目的对应路径。
* 终端顶部页签名称会自动变更为 `[工具名] [项目名]`，方便多开辨识。

---

## 5. 技术架构与实现原理

### 5.1 路径解析引擎 (`ConvertTo-WslPath`)

利用正则表达式 `^([a-zA-Z]):(.*)` 捕获 Windows 盘符，将其转化为 `/mnt/盘符小写` 格式，并将反斜杠 `\` 统一替换为正斜杠 `/`，确保 WSL 能够正确挂载和访问 Windows 文件系统。

### 5.2 异步检测机制

* **Windows 环境**：使用 PowerShell 内置 cmdlet `Get-Command -ErrorAction SilentlyContinue` 进行低开销静默探测。
* **WSL 环境**：通过拼接 Bash for 循环，执行 `wsl.exe -e bash -lc "for cmd in ...; do command -v; done"`，实现一次进程调用完成批量指令探测，最大化缩短 UI 启动延迟。

### 5.3 终端拉起与进程分发

根据下拉框捕获的环境标志（`[Win]` / `[WSL]`），执行不同策略：

* **针对 WSL**：
组合使用 `-e bash -ic` 确保加载完整的 Linux 环境变量（解决诸如 `command not found` 的问题），并利用 `echo -ne '\033]0;TITLE\007'` 发送 ANSI 序列劫持终端标题。
* **针对 Windows**：
利用 `cmd.exe /k` 保持控制台窗口打开，通过 `title` 指令修改标题，利用 `cd /d` 实现安全的跨盘符目录切换。

---

## 6. 维护与扩展 (FAQ)

**Q1：如何让工具自动探测更多新的 AI 指令？**
打开 `Launcher.ps1`，找到代码第 20 行的 `$toolsToCheck` 数组：

```powershell
$toolsToCheck = @("kiro-cli", "claude", "kimi", "opencode", "gemini", "cursor", "code")

```

直接将新的工具命令名称追加到数组中即可，脚本下次启动时会自动进行双轨探测。

**Q2：运行快捷方式时毫无反应？**

1. 检查 PowerShell 脚本的绝对路径是否拼写正确。
2. 检查是否正确配置了 `AI_PROJECTS` 环境变量。如果未配置或格式错误，脚本为了防止异常可能会静默退出（或弹出缺失配置的提示框）。

**Q3：WSL 启动后提示 `No such file or directory`？**
检查环境变量中配置的 Windows 路径是否正确，确保该盘符（如 C盘、D盘）已经被 WSL 正常挂载。

---

## 7. 下载安装功能

### 7.1 功能概述

点击工具下拉框右侧的 **"下载"** 按钮，可弹出工具安装管理对话框：

* 显示预设的 AI 编程工具列表及其安装状态
* 支持选择运行环境（Windows / WSL）
* 支持安装未安装的工具
* 支持添加自定义工具

### 7.2 预设工具

`tools-config.json` 中预设了以下常用 AI 编程工具：

| 工具名称 | Windows 安装命令 | WSL 安装命令 |
|---------|-----------------|-------------|
| Kiro CLI | (不支持，仅 WSL) | `npm install -g kiro-cli` |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | `npm install -g @anthropic-ai/claude-code` |
| Cursor | `winget install Cursor.Cursor` | (不支持) |
| Kimi CLI | `npm install -g kimi-cli` | `npm install -g kimi-cli` |

### 7.3 添加自定义工具

在下载对话框中点击 **"添加自定义"** 按钮，可添加自定义工具：

* **Tool Name**：工具显示名称
* **Install Command**：安装命令
* **Check Command**：检测命令（可选，默认使用 `工具名 --version`）

### 7.4 修改预设工具配置

编辑 `tools-config.json` 文件可修改预设工具列表：

```json
{
  "tools": [
    {
      "name": "tool-name",
      "displayName": "Display Name",
      "winInstall": "npm install -g tool-name",
      "wslInstall": "npm install -g tool-name",
      "checkCommand": "tool-name --version",
      "url": "https://example.com"
    }
  ]
}
```