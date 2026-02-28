🌐 [English](CHANGELOG.md) | [中文](CHANGELOG.zh.md) | [日本語](CHANGELOG.ja.md)

# AI-CLI Changelog

## v2.3.0 (2026-02-28)

### ✨ New Features

#### 1. Git Worktree Support ⭐
- **Automatic Detection**: Detects Git repositories and worktrees after project selection
- **Smart Selection Interface**: Shows all worktrees when multiple detected
  - Branch name highlighting (cyan/green, most prominent)
  - Status indicators: ahead/behind commits (↑↓) and current worktree
  - Path display in gray (least prominent)
  - Keyboard navigation: ↑↓ to select, Enter to confirm, Esc to go back
- **Parallel Development**: Work on multiple branches simultaneously without switching
- **Branch Status**: Shows ahead/behind commit counts relative to remote
  - `↑3` - 3 commits ahead
  - `↓1` - 1 commit behind
  - `↑2 ↓1` - Diverged (2 ahead, 1 behind)

#### 2. Empty Project List Smart Guidance
- Automatically prompts when no projects configured
- Auto-enters project creation after 2 seconds
- Removed old direct exit logic, improved first-time experience

#### 3. Project Path Input Optimization
- Shows current directory as default value hint
- Format: `(Press Enter to use current directory: C:\...)`
- Users clearly understand default behavior

#### 4. Input Flow Cancel Support
- Enhanced `Read-InputWithPlaceholder` function with ESC key support
- Name and path inputs can be cancelled with ESC
- Backspace key support for character deletion
- Users can return at any input stage without forced completion

#### 5. Interface Display Fixes
- Fixed duplicate icons in type selection interface
- Removed redundant icons from type definitions

### 🔧 Technical Implementation

#### New Functions
1. **Get-GitWorktrees**: Git repository and worktree detection
   - Checks .git directory existence
   - Verifies git command availability
   - Executes `git worktree list` and parses output
   - Extracts path, branch, HEAD information
   - Detects branch status (ahead/behind) using `git rev-list`
   - Supports detached HEAD state

2. **Select-GitWorktree**: Interactive worktree selection
   - Builds selection item list
   - Identifies and highlights current worktree
   - Implements keyboard navigation logic
   - Returns user-selected path or null (ESC)

#### Function Enhancements
- **Read-InputWithPlaceholder**: Added `AllowCancel` parameter
  - Custom key handling logic
  - Returns special value `__CANCEL__` for cancel operation
  - Supports character input, backspace, enter, ESC

#### Flow Optimizations
- **Start-InteractiveLauncher**: 
  - Distinguishes between root empty and subfolder empty
  - Integrates worktree detection after project selection
  - Updates project path to selected worktree
  - Handles ESC return to cancel project selection
- **Add-NewProject**: Detects cancel signal at each input point

### 📊 Change Statistics
- Modified file: ai-cli.ps1
- Lines changed: +247/-24
- New functions: 2 (Git Worktree related)
- Enhanced functions: 1 (input cancel support)
- New features: 5
- Fixed issues: 2
- New documentation: docs/GIT-WORKTREE.md

### 📚 Documentation
- Added docs/GIT-WORKTREE.md - Git Worktree feature guide
- Updated README.md - Added Git Worktree to core features
- Updated CHANGELOG.md - Version change log

---

## v2.2.9 (2026-02-28)

### ✨ New Features
- **Automatic PATH Management**: Automatically adds tools to environment variables after installation
  - Automatically searches for tool executable locations (supports 9 common installation directories)
  - Intelligently detects if directory is already in PATH to avoid duplicates
  - Automatically updates user environment variables and refreshes current session
  - No need for manual configuration or terminal restart to use new tools
  - PATH length check (2047 character limit) prevents system issues

### 🔧 Technical Improvements
- Added `Find-ToolExecutable` function: searches for tool executables
- Added `Add-ToUserPath` function: safely adds directories to PATH
- Added `Update-PathAfterInstall` function: automatically updates PATH after installation
- Supports .exe, .cmd, .bat executable file formats
- WSL environment automatically skipped (handled by package manager)

---

## v2.2.8 (2026-02-28)

### ✨ New Features
- **Manual Tool List Refresh**: Added `[R] Refresh` shortcut in tool selection interface
  - Manually trigger foreground tool detection
  - Immediately update tool list and configuration file
  - Convenient for verifying tool installation status

### 🔧 Technical Improvements
- **Auto-refresh After Installation**: Automatically reloads configuration after tool installation
  - Newly installed tools immediately available in list
  - No need to manually return or restart program

---

## v2.2.7 (2026-02-28)

### ✨ New Features
- **Background Async Tool Detection**: Background tool detection at startup, non-blocking UI
  - Startup delay reduced to 0ms, UI displays immediately
  - Configuration automatically updates after background detection completes
  - Automatically stops background task during foreground detection to avoid conflicts

### 🐛 Bug Fixes
- **Fixed Install Hint Display Issue**: `[I] Install` hint no longer depends on Windows Terminal
  - All users can see installation hint
  - Added `showInstall` parameter to decouple hint logic
- **Fixed Aider Installation Command**:
  - Windows: Fixed command separator (`&&` → `;`)
  - WSL: Changed to official installation script (`curl | sh`)

### 🔧 Technical Improvements
- Added `Start-BackgroundDetection` function: background async detection
- Main loop automatically checks background task status
- Automatically cleans up background tasks on exit
- Atomic file write mechanism (temp file + backup + move)

---

## v2.2.6 (2026-02-26)

### 🐛 Bug Fixes
- **Fixed WSL Tool Detection Failure**: Use `-ic` parameter to load complete environment
  - Resolved `command not found` issue
  - Ensures `.bashrc` environment variables load correctly
- **Fixed Configuration Sync Issue**: Tool detection results persisted to configuration file
  - Avoids re-detection on every startup
  - Improves startup speed

### 🔧 Technical Improvements
- Optimized WSL detection command: `wsl.exe -e bash -ic "command -v tool"`
- Tool status cached to `config.json`
- Removed redundant detection logic

---

## v2.2.0 (2026-02-26)

### ✨ New Features
- **Tree Structure Management**: Projects support folder categorization and multi-level organization
  - Support creating two types: folders and projects
  - Folders can contain projects and subfolders
  - Breadcrumb navigation shows current location
  - Recursively delete folders and all their children
- **Delete Function**: Support for deleting projects and folders
  - Requires manual name input to confirm deletion
  - Shows the number of children when deleting a folder
  - Safety mechanism to prevent accidental deletion
- **Configuration File Separation**: Configuration file migrated from program directory to user configuration directory
  - User configuration: `%APPDATA%\AI-CLI\config.json`
  - Default configuration: `config.json` in program directory
  - Read priority: User configuration first, default configuration if not exists
  - All modifications saved to user configuration
  - Configuration is not lost during uninstallation
- **Enhanced Parameter Compatibility**: Support for both `-` and `--` parameter prefixes
  - Example: Both `-Init` and `--init` can be used
  - Parameters are case-insensitive
- **Help Function**: New `--help` parameter displays all supported commands and descriptions

### 🔄 Improvements
- Automatically copy default configuration to user directory during installation
- Completely clear program folder during uninstallation
- Automatically migrate old flat configuration to tree structure
- Optimized UI display, using icons to distinguish folders and projects

### 📚 Documentation Updates
- Updated configuration file location and priority description
- Added configuration persistence description
- Added parameter prefix compatibility description
- Added help command usage description
- Added tree structure usage description
- Updated keyboard shortcut description

---

## v2.1.1 (2026-02-26)

### 🐛 Bug Fixes
- Fixed environment variable type conversion error: correctly convert PSCustomObject to Hashtable
- Improved uninstallation function: added desktop shortcut deletion and PATH environment variable cleanup
- Corrected uninstall command syntax in documentation (`--uninstall` → `-Uninstall`)

### 🔄 UI Improvements
- Optimized new project interface:
  - Project name no longer shows placeholder, must be manually entered
  - Project path no longer shows placeholder, automatically uses current directory when empty
  - Removed empty bracket display when placeholder is empty

### 📚 Documentation Updates
- Corrected uninstall command syntax description
- Added note: PowerShell parameters are case-insensitive (supports `-uninstall`, `-Uninstall`, `-UNINSTALL`, etc.)

---

## v2.1.0 (2026-02-26)

### ✨ New Features
- **Add Project Function**: Press `N` key in project selection interface to directly add new project
  - Support project name input (required, automatically detects duplicates)
  - Support project path input (required, automatically detects path existence, can create)
  - Support environment variable configuration (optional, KEY=VALUE format)
  - Complete input validation and user experience optimization
- **Environment Variable Injection**: Automatically inject project-configured environment variables when starting AI CLI tools
  - **Smart Path Conversion**: In WSL environment, automatically convert environment variable values in Windows path format to WSL path format

### 🔄 UI Improvements
- Removed install tool function (`I` key) from project selection interface, simplified interaction
- Optimized menu prompt text, displaying different keyboard shortcut hints based on interface type
- When project path is empty when adding new project, automatically use current directory

### 📚 Documentation Updates
- Updated README.md, added new project interface description and environment variable configuration examples
- Updated keyboard shortcut description, reflecting latest interaction logic
- Added smart path conversion function description

---

## v2.0.1 (2026-02-26)

### 🐛 Bug Fixes
- Fixed `install.ps1` desktop shortcut creation error
  - Changed `.bat` file content from PowerShell format to correct batch format
  - Shortcut directly points to `ai-cli.ps1` instead of intermediate `.bat` file
  - Added custom icon support (`ai-cli.ico`)
- Updated README.md installation description

---

## v2.0.0 (2026-02-26)

### 🎉 Major Update

#### New Features
- ✅ **Pure Terminal Interface**: Replaced WinForms, providing fast keyboard-driven CLI interface
- ✅ **Loop Launch Mode**: Program doesn't exit, supports continuous tool and project selection
- ✅ **Multi-Tab Support**: Ctrl+Enter launches tool in new Windows Terminal tab
- ✅ **Tool Installation Function**: Press I key to quickly install uninstalled AI CLI tools
- ✅ **Unified Configuration Management**: config.json manages all settings (projects, tools, preferences)
- ✅ **8 Mainstream Tools Pre-configured**: Out-of-the-box tool configuration

#### Core Fixes
- 🐛 **WSL Tool Detection**: Use `bash -ic` instead of `bash -lc` to correctly load .bashrc environment variables
- 🐛 **WSL Launch Crash**: Adopted single string parameter method, solving ArgumentList array problem
- 🐛 **Show-Menu Return Value**: Removed redundant return statement, avoiding array return

#### Performance Improvements
- ⚡ **Faster Launch Speed**: No GUI loading delay, instant response
- 🎨 **Better Keyboard Navigation**: ↑↓ select, Enter confirm, Esc return, I install
- 📚 **Complete Documentation System**: README, TOOLS, INSTALL-GUIDE, BUGFIX

### Supported AI CLI Tools

| Tool | Developer | Windows | WSL/Linux |
|------|-----------|---------|-----------|
| Kiro CLI | AWS | ❌ | ✅ |
| Claude Code | Anthropic | ✅ | ✅ |
| OpenAI Codex | OpenAI | ✅ | ✅ |
| Kimi CLI | Moonshot AI | ✅ | ✅ |
| Gemini CLI | Google | ✅ | ✅ |
| Cursor Agent | Cursor | ❌ | ✅ |
| OpenCode | Open Source | ✅ | ✅ |
| Aider | Open Source | ✅ | ✅ |

### Keyboard Shortcuts

#### Tool Selection Interface
- `↑↓` - Navigate selection
- `Enter` - Launch tool in new window
- `Ctrl+Enter` - Launch tool in new tab (requires Windows Terminal)
- `I` - Install new tool
- `Esc` - Return to project selection
- `Q` - Exit program

#### Project Selection Interface
- `↑↓` - Navigate selection
- `Enter` - Select project
- `Q` - Exit program

### Technical Architecture

```
Main Loop
├── Project Selection Loop
│   └── Tool Selection Loop
│       ├── Detect Windows Terminal
│       ├── Show Prompt (conditional)
│       ├── Launch Session (normal/multi-tab)
│       ├── Install Tool (press I key)
│       └── Return to Parent (press Esc)
```

### Installation Methods

#### Quick Installation
```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

#### Manual Installation
```powershell
# Download project
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Initialize configuration
.\ai-cli.ps1 -Init

# Run
.\ai-cli.ps1
```

### Configuration File

#### config.json Structure
```json
{
  "projects": [
    {
      "name": "Project Name",
      "path": "Project Path",
      "description": "Project Description"
    }
  ],
  "tools": [
    {
      "name": "Tool Command",
      "displayName": "Display Name",
      "winInstall": "Windows Installation Command",
      "wslInstall": "WSL Installation Command",
      "checkCommand": "Detection Command",
      "url": "Official Website"
    }
  ],
  "settings": {
    "language": "auto",
    "defaultEnv": "wsl",
    "terminalEmulator": "default"
  }
}
```

### Documentation

- **README.md** - Complete usage description and feature introduction
- **TOOLS.md** - Detailed reference manual for 8 AI CLI tools
- **INSTALL-GUIDE.md** - Tool installation function usage guide
- **BUGFIX.md** - Bug fix records and technical details
- **CHANGELOG.md** - This document, version changelog

---

## v1.x (Historical Versions)

### Features
- ✅ WinForms GUI
- ✅ Environment variable configuration (AI_PROJECTS)
- ✅ Basic tool detection and launch
- ✅ Windows/WSL dual environment support
- ✅ Dynamic tab naming

### Limitations
- ❌ Slow launch speed (GUI loading)
- ❌ Program exits after each launch
- ❌ No multi-tab support
- ❌ No tool installation function
- ❌ Scattered configuration (environment variables + JSON)

### Migration to v2.0

v1.x users don't need manual migration, v2.0 will automatically:
1. Read `AI_PROJECTS` environment variable
2. Generate `config.json`
3. Preserve all project configuration

---

## Future Plans

### v2.1 (Planned)
- [ ] Project Management: Add/Edit/Delete projects
- [ ] Tool Management: Add/Edit/Delete tools
- [ ] Configuration Import/Export
- [ ] Tool Usage Statistics

### v2.2 (Planned)
- [ ] Remote Project Support (SSH)
- [ ] Docker Container Support
- [ ] Custom Launch Scripts
- [ ] Workspace Templates

---

*Last Updated: 2026-02-26*
