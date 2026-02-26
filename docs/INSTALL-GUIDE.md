🌐 [English](INSTALL-GUIDE.md) | [中文](INSTALL-GUIDE.zh.md) | [日本語](INSTALL-GUIDE.ja.md)

# AI-CLI Installation Tool Guide

## Feature Overview

Press the `I` key in the tool selection screen to quickly install AI CLI tools that are not yet installed.

## Usage Steps

### 1. Start AI-CLI
```powershell
.\ai-cli.ps1
```

### 2. Select a Project
Use the ↑↓ keys to select a project, then press Enter to confirm.

### 3. Press I to Enter the Installation Screen
In the tool selection screen, press the `I` key to open the installation tool list.

### 4. Select Tools to Install
- The list displays all tools that are not installed but have installation commands configured
- `[Win]` or `[WSL]` after the tool name indicates the installation environment
- Use ↑↓ keys to select, press Enter to confirm installation
- Press Esc to return to the tool selection screen

### 5. Wait for Installation to Complete
- The screen will display the installation command and execution process
- Press any key to return after installation completes

## Keyboard Shortcuts

### Tool Selection Screen
- `↑↓` - Navigate selection
- `Enter` - Launch tool in a new window
- `Ctrl+Enter` - Launch tool in a new tab (requires Windows Terminal)
- `I` - Install new tool
- `Esc` - Return to project selection
- `Q` - Exit program

### Installation Tool Screen
- `↑↓` - Navigate selection
- `Enter` - Install selected tool
- `Esc` - Return to tool selection
- `Q` - Exit program

## Installation Logic

### Windows Environment Tools
Execute installation commands directly in PowerShell, for example:
```powershell
npm install -g @anthropic-ai/claude-code
```

### WSL Environment Tools
Execute bash commands through WSL, for example:
```bash
wsl.exe -e bash -ic "curl -fsSL https://cli.kiro.dev/install | bash"
```

## Supported Tools

Based on `config.json` configuration, the following tools are currently supported for installation:

| Tool | Windows | WSL/Linux |
|------|---------|-----------|
| Kiro CLI | ❌ | ✅ |
| Claude Code | ✅ | ✅ |
| OpenAI Codex | ✅ | ✅ |
| Kimi CLI | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ |
| Cursor Agent | ❌ | ✅ |
| OpenCode | ✅ | ✅ |
| Aider | ✅ | ✅ |

## Important Notes

1. **Permission Requirements**: Some installation commands may require administrator privileges
2. **Network Connection**: A stable network connection is required during installation
3. **Dependency Check**: Ensure necessary dependencies are installed (Node.js, Python, pip, etc.)
4. **WSL Configuration**: WSL tools require WSL environment to be configured first
5. **Installation Verification**: After installation, tools will be automatically detected on next launch

## Custom Installation Commands

Edit the `config.json` file to modify or add tool installation commands:

```json
{
  "name": "tool-name",
  "displayName": "Tool Display Name",
  "winInstall": "npm install -g tool-name",
  "wslInstall": "curl -fsSL https://example.com/install.sh | bash",
  "checkCommand": "tool-name --version",
  "url": "https://official-website.com"
}
```

- `winInstall`: Windows environment installation command (null means not supported)
- `wslInstall`: WSL/Linux environment installation command (null means not supported)
- `checkCommand`: Command used to detect whether the tool is installed

## Troubleshooting

### Installation Failure
1. Check network connection
2. Confirm dependencies are installed (Node.js, Python, etc.)
3. Review error messages and manually execute the installation command
4. Refer to the tool's official documentation

### Tool Not Detected After Installation
1. Restart AI-CLI
2. Check PATH environment variable
3. Manually run `tool-name --version` to verify installation
4. Check if `checkCommand` in `config.json` is correct

### WSL Tool Installation Failure
1. Confirm WSL is properly installed and configured
2. Manually execute the installation command in WSL to test
3. Check WSL network connection
4. Update WSL: `wsl --update`

---

*Last updated: 2026-02-26*
