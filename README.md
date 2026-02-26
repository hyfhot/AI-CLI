# AI CLI Launcher

> 🌐 **English** | [中文](README.zh.md) | [日本語](README.ja.md)

## 1. Introduction

**AI CLI Launcher** is a lightweight terminal launcher tool based on PowerShell. Designed for modern AI-assisted programming scenarios, it aims to unify management and quickly launch various AI CLI tools (such as `kiro-cli`, `Claude Code`, `Kimi CLI`, `Cursor Agent`, `OpenCode`, etc.).

This tool breaks down the barriers between native Windows environment and Windows Subsystem for Linux (WSL), allowing developers to select target projects in a unified terminal interface and launch corresponding AI programming tools with one click, automatically completing path conversion and terminal environment initialization.

> 📚 **View Supported Tools**: For detailed tool list, installation instructions, and comparison, please refer to [docs/TOOLS.md](docs/TOOLS.md)

## 2. Core Features

* **🤖 Intelligent Dual-Environment Detection**: Automatically detects AI CLI tools installed in Windows host and WSL environments at startup, and categorizes them with `[Win]` or `[WSL]` labels.
* **📂 Unified Project Management**: Centrally manages project paths through `config.json`, supporting cross-drive and cross-environment projects.
* **🔄 Cross-Environment Path Conversion**: Built-in path conversion engine automatically converts Windows absolute paths (e.g., `C:\Projects\...`) to WSL-compliant mount paths (e.g., `/mnt/c/Projects/...`).
* **⚡ Pure Terminal Interaction**: Fast keyboard-driven CLI interface, no GUI loading delay, instant response.
* **🔁 Loop Launch Mode**: The program does not exit, supports continuous selection of tools and projects, improving work efficiency.
* **📑 Multi-Tab Support**: Ctrl+Enter launches tools in new Windows Terminal tabs, convenient for multi-task management.
* **🛠️ Tool Installation Feature**: Press I key to quickly install uninstalled AI CLI tools.
* **🏷️ Dynamic Tab Naming**: Dynamically modifies terminal tab titles at startup through ANSI escape sequences and Windows native commands (e.g., `KIRO-CLI BT2400`), greatly improving multi-task management clarity.

---

## 3. Installation and Configuration Guide

### 3.1 Environment Requirements

* Operating System: Windows 10 / Windows 11
* Runtime Environment: PowerShell 5.1 or higher
* Dependencies: WSL installed and configured (if you need to use Linux tools)

### 3.2 Quick Installation (Recommended)

The project provides an automatic installation script. Just run the following command to complete the installation:

```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

The installation script will automatically:
1. Download the latest version from GitHub (including icon files)
2. Copy program files to `%LOCALAPPDATA%\AI-CLI` directory
3. Create desktop shortcuts (with custom icons)
4. Add to system PATH environment variable

After installation, you can start by:
- Double-clicking the "AI-CLI" shortcut on the desktop
- Running `ai-cli` in the command line (need to reopen the terminal)

**Common Commands:**
```powershell
ai-cli           # Launch interactive interface
ai-cli --help    # View help information
ai-cli --init    # Initialize configuration
ai-cli --config  # Edit configuration
```

**Uninstall Command:**
```powershell
ai-cli -Uninstall
```

If not yet added to PATH, you can uninstall using:
```powershell
& "$env:LOCALAPPDATA\AI-CLI\ai-cli.ps1" -Uninstall
```

**Parameter Description**: Supports both `-` and `--` parameter prefixes, e.g., `-Init` and `--init` are equivalent (case-insensitive).

### 3.3 Manual Deployment Steps

**Step 1: Clone or Download the Project**
```powershell
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI
```

**Step 2: Initialize Configuration**
```powershell
.\ai-cli.ps1 -Init
```

This will create a configuration file in the user configuration directory (`%APPDATA%\AI-CLI\config.json`). If a default configuration exists in the program directory, it will be copied automatically; otherwise, a new configuration will be created.

You can manually edit the configuration file to add projects:

```json
{
  "projects": [
    {
      "name": "Project Name",
      "path": "C:\\Projects\\MyProject",
      "description": "Project description (optional)"
    }
  ]
}
```

**Step 3: Run the Program**
```powershell
.\ai-cli.ps1
```

**View Help**
```powershell
.\ai-cli.ps1 --help
```

---

## 4. Usage Instructions

### 4.1 Launch and Interface Description

After running `ai-cli`, you will enter the pure terminal interaction interface:

#### Project Selection Interface (Tree Structure)
```
=== Select Project ===
> 📁 Frontend Projects (3 item(s))
  📁 Backend Projects (2 item(s))
  📄 Standalone Project (C:\Projects\standalone)

[↑↓] Select  [Enter] Enter/Confirm  [N] New  [D] Delete  [Q] Quit
```

After entering a folder:
```
  Home > Frontend Projects

=== Select Project ===
> 📄 Vue Project (C:\Projects\vue-app)
  📁 React Projects (2 item(s))
  📄 Angular Project (C:\Projects\angular-app)

[↑↓] Select  [Enter] Enter/Confirm  [N] New  [D] Delete  [Esc] Back  [Q] Quit
```

#### Tool Selection Interface
```
=== Select AI Tool (Project: Project 1) ===
> [WSL] kiro-cli
  [Win] claude
  [WSL] opencode
  [Win] aider

[↑↓] Select  [Enter] Launch  [Ctrl+Enter] New Tab  [I] Install  [Esc] Back  [Q] Quit
```

#### New Item Interface (Type Selection)
```
=== Select Type ===
> 📄 Project
  📁 Folder

[↑↓] Select  [Enter] Confirm  [Esc] Cancel
```

#### Delete Confirmation Interface
```
=== Delete Confirmation ===
Project Name: MyProject_

Project Name: MyProject
Project Path: C:\Projects\MyProject
Environment Variables (optional, press Enter to skip):
  Format: KEY=VALUE, one per line, empty line to end
  Env Var: API_KEY=sk-xxx
    Added: API_KEY=sk-xxx
To delete: 📁 Frontend Projects (contains 5 items)

⚠️  Warning: This action cannot be undone!
Please enter the name to confirm deletion: Frontend Projects_

[Enter name] Confirm  [Esc] Cancel
```

### 4.2 Keyboard Shortcuts

#### Project Selection Interface
- `↑↓` - Navigate selection
- `Enter` - Enter folder or select project
- `N` - New project or folder
- `D` - Delete project or folder
- `Esc` - Return to parent folder
- `Q` - Quit program

#### Tool Selection Interface
- `↑↓` - Navigate selection
- `Enter` - Launch tool in new window
- `Ctrl+Enter` - Launch tool in new tab (requires Windows Terminal)
- `I` - Install new tool
- `Esc` - Return to project selection
- `Q` - Quit program

#### New Item Interface
- Enter project name (required, cannot be duplicate)
- Enter project path (required, automatically detects if path exists)
- Enter environment variables (optional, format: KEY=VALUE)
- Confirm add or cancel

### 4.3 Tree Structure Management

Projects support tree structure organization:
- **Folders**: Used to categorize and manage projects, can contain projects and subfolders
- **Projects**: Actual working directories, containing paths and environment variables
- **Breadcrumb Navigation**: Shows current location, convenient for multi-level navigation
- **Recursive Delete**: Prompts the number of contained items when deleting a folder

### 4.4 Runtime Effects

* The script automatically launches the corresponding terminal (Cmd or WSL).
* The terminal automatically `cd` into the corresponding path of the selected project.
* Environment variables configured in the project are automatically injected into the runtime environment.
  * **Intelligent Path Conversion**: In WSL environment, Windows path format environment variable values (e.g., `C:\Projects\...`) are automatically converted to WSL path format (`/mnt/c/Projects/...`).
* The terminal tab title at the top is automatically changed to `[Tool Name] [Project Name]`, convenient for multi-instance identification.

---

## 5. Technical Architecture and Implementation Principles

### 5.1 Tree Structure Implementation

Project configuration uses a recursive tree structure:
```json
{
  "projects": [
    {
      "type": "folder",
      "name": "Frontend Projects",
      "children": [
        {
          "type": "project",
          "name": "Vue Project",
          "path": "C:\\Projects\\vue-app"
        }
      ]
    }
  ]
}
```

- Automatically migrates old version flat configurations to tree structure
- Supports recursive traversal, add, and delete operations
- Breadcrumb navigation tracks current path

### 5.2 Path Resolution Engine (`ConvertTo-WslPath`)

Uses regular expression `^([a-zA-Z]):(.*)` to capture Windows drive letters, converts them to `/mnt/lowercase-drive-letter` format, and replaces backslashes `\` with forward slashes `/` to ensure WSL can correctly mount and access Windows file systems.

### 5.3 Tool Detection Mechanism

* **Windows Environment**: Uses PowerShell built-in cmdlet `Get-Command -ErrorAction SilentlyContinue` for low-overhead silent detection.
* **WSL Environment**: Executes detection through `wsl.exe -e bash -ic "command -v tool"`, using `-ic` parameter to ensure `.bashrc` environment variables are loaded.

### 5.4 Terminal Launch and Process Distribution

Based on tool environment flags (`[Win]` / `[WSL]`), different strategies are executed:

* **For WSL**:
Combines `-e bash -ic` to ensure complete Linux environment variables are loaded (solving issues like `command not found`), and uses `echo -ne '\033]0;TITLE\007'` to send ANSI sequences to set terminal titles.
* **For Windows**:
Uses `cmd.exe /k` to keep the console window open, modifies titles through `title` command, and uses `cd /d` to achieve safe cross-drive directory switching.

---

## 6. Tool Installation Feature

### 6.1 Usage

In the tool selection interface, press the `I` key to enter the tool installation interface:

```
=== Install AI Tools ===
> [WSL] kiro-cli
  [Win] gemini
  [WSL] cursor-agent

[↑↓] Select  [Enter] Install  [Esc] Back  [Q] Quit
```

Select the tool you want to install, press Enter to confirm, and the program will automatically execute the installation command.

### 6.2 Supported Tools

According to `config.json` configuration, currently supports installing 8 mainstream AI CLI tools. For detailed information, please refer to [docs/TOOLS.md](docs/TOOLS.md) and [docs/INSTALL-GUIDE.md](docs/INSTALL-GUIDE.md).

---

## 7. Configuration File Description

Configuration file location: `%APPDATA%\AI-CLI\config.json` (typically `C:\Users\<Username>\AppData\Roaming\AI-CLI\config.json`)

**Configuration Priority**:
1. Prioritize reading `config.json` from the user configuration directory
2. If it does not exist, read the default `config.json` from the program directory
3. All modifications are saved to the user configuration directory

**Note**: Configuration files are stored separately from the program, and configurations are not lost when uninstalling the program.

### 7.1 config.json Structure

```json
{
  "projects": [
    {
      "name": "Project Name",
      "path": "Project Path",
      "description": "Project description (optional)",
      "env": {
        "API_KEY": "your-api-key",
        "DEBUG": "true"
      }
    }
  ],
  "tools": [
    {
      "name": "Tool Command",
      "displayName": "Display Name",
      "winInstall": "Windows installation command or null",
      "wslInstall": "WSL installation command or null",
      "checkCommand": "Detection command",
      "url": "Official website"
    }
  ],
  "settings": {
    "language": "auto",
    "defaultEnv": "wsl",
    "terminalEmulator": "default"
  }
}
```

### 7.2 Adding Projects

Edit `config.json`, add to the `projects` array:

```json
{
  "name": "MyProject",
  "path": "C:\\Projects\\MyProject",
  "description": "My Project"
}
```

### 7.3 Adding Custom Tools

Edit `config.json`, add to the `tools` array:

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

## 8. Frequently Asked Questions (FAQ)

**Q1: How to add a new project?**
Edit the `config.json` file, add project information to the `projects` array, or run `ai-cli -Init` to reinitialize the configuration.

**Q2: Tool not found when running?**
1. Confirm the tool is correctly installed
2. Check the PATH environment variable
3. For WSL tools, confirm the WSL environment is correctly configured
4. Run `ai-cli` to re-detect tools

**Q3: `No such file or directory` after WSL launch?**
Check if the project path is correct, and ensure the drive (e.g., C drive, D drive) has been normally mounted by WSL.

**Q4: How to use the multi-tab feature?**
Make sure Windows Terminal is installed, then press `Ctrl+Enter` in the tool selection interface to launch the tool.

**Q5: How to uninstall?**
Run `ai-cli -Uninstall` or `& "$env:LOCALAPPDATA\AI-CLI\ai-cli.ps1" -Uninstall`.

---

## 9. Related Documentation

- **[docs/TOOLS.md](docs/TOOLS.md)** - Detailed reference manual for 8 mainstream AI CLI tools
- **[docs/INSTALL-GUIDE.md](docs/INSTALL-GUIDE.md)** - Guide for using the tool installation feature
- **[docs/BUGFIX.md](docs/BUGFIX.md)** - Bug fix records and technical details
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Version update log

---

*Last updated: 2026-02-26*
