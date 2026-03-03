# AI-CLI Installation Guide

> 🌐 **English** | [中文](INSTALL-GUIDE.zh.md) | [日本語](INSTALL-GUIDE.ja.md) | [Deutsch](INSTALL-GUIDE.de.md)

## Quick Installation

### Using Installation Script (Recommended)

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# If using Git worktree
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# Install dependencies
pip install -e ".[dev]"
```

## Tool Installation Feature

Press the `I` key in the tool selection screen to quickly install AI CLI tools that are not yet installed.

### Usage Steps

1. **Start AI-CLI**
   ```bash
   ai-cli
   ```

2. **Select a Project**
   - Use ↑↓ keys to select a project
   - Press Enter to confirm

3. **Press I to Enter Installation Screen**
   - In the tool selection screen, press the `I` key
   - Opens the installation tool list

4. **Select Tools to Install**
   - List displays all tools that are not installed but have installation commands configured
   - `[Windows]`, `[WSL]`, `[Linux]`, or `[macOS]` indicates the installation environment
   - Use ↑↓ keys to select
   - Press Enter to confirm installation
   - Press Esc to return to tool selection screen

5. **Wait for Installation to Complete**
   - Screen displays the installation command and execution process
   - Press any key to return after installation completes

## Configuration

### Initialize Configuration

```bash
ai-cli --init
```

This creates a default configuration file at:
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### Edit Configuration

```bash
ai-cli --config
```

Or manually edit the configuration file with your preferred text editor.

## Troubleshooting

### Python Version Issues

**Issue**: Command not found or import errors

**Solution**: Ensure Python 3.8+ is installed
```bash
python --version  # Should be 3.8 or higher
```

### Permission Issues

**Issue**: Permission denied during installation

**Solution**: 
- Linux/macOS: Use `sudo` if needed
- Windows: Run as Administrator

### Path Issues

**Issue**: `ai-cli` command not found after installation

**Solution**: 
- Ensure pip installation directory is in PATH
- Try using `python -m ai_cli.cli` instead

### WSL Issues

**Issue**: WSL tools not detected

**Solution**: 
- Ensure WSL is installed: `wsl --install`
- Check WSL is accessible: `wsl --list`

## Uninstallation

```bash
ai-cli --uninstall
```

This will:
- Remove the configuration directory
- Uninstall the Python package
- Clean up any temporary files

---

For more information, see the [main README](../README.md).
