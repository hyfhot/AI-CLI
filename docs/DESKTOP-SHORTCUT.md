# Desktop Shortcut Guide

AI-CLI automatically creates desktop shortcuts when you run `ai-cli --init`.

## Platform-Specific Behavior

### Windows

- **Location**: `%USERPROFILE%\Desktop\AI-CLI.lnk`
- **Type**: Windows shortcut (.lnk)
- **Icon**: Uses bundled ai-cli.ico
- **Launch**: Double-click to open AI-CLI in a new terminal window

### Linux

- **Locations** (tries in order):
  1. `~/Desktop/ai-cli.desktop`
  2. `~/desktop/ai-cli.desktop`
  3. `~/.local/share/applications/ai-cli.desktop`
- **Type**: Desktop Entry file (.desktop)
- **Icon**: Uses bundled ai-cli.ico or system terminal icon
- **Launch**: Double-click to open AI-CLI in terminal

### macOS

- **Location**: `~/Desktop/AI-CLI.app`
- **Type**: Application bundle (.app)
- **Launch**: Double-click to open AI-CLI in Terminal.app

## Manual Creation

If the automatic creation fails, you can manually create shortcuts:

### Windows (PowerShell)

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\AI-CLI.lnk")
$Shortcut.TargetPath = "ai-cli"
$Shortcut.Description = "AI-CLI Launcher"
$Shortcut.Save()
```

### Linux

```bash
cat > ~/Desktop/ai-cli.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=AI-CLI
Comment=AI-CLI Launcher for AI Coding Assistants
Exec=ai-cli
Icon=utilities-terminal
Terminal=true
Categories=Development;Utility;
DESKTOP

chmod +x ~/Desktop/ai-cli.desktop
```

### macOS

```bash
# Create app bundle
mkdir -p ~/Desktop/AI-CLI.app/Contents/MacOS

cat > ~/Desktop/AI-CLI.app/Contents/MacOS/ai-cli << 'SCRIPT'
#!/bin/bash
osascript -e 'tell application "Terminal" to do script "ai-cli"'
SCRIPT

chmod +x ~/Desktop/AI-CLI.app/Contents/MacOS/ai-cli

# Create Info.plist
cat > ~/Desktop/AI-CLI.app/Contents/Info.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ai-cli</string>
    <key>CFBundleIdentifier</key>
    <string>org.ai-cli.launcher</string>
    <key>CFBundleName</key>
    <string>AI-CLI</string>
</dict>
</plist>
PLIST
```

## Removal

Desktop shortcuts are automatically removed when you run `ai-cli --uninstall`.

To manually remove:

- **Windows**: Delete `%USERPROFILE%\Desktop\AI-CLI.lnk`
- **Linux**: Delete `~/Desktop/ai-cli.desktop` or `~/.local/share/applications/ai-cli.desktop`
- **macOS**: Delete `~/Desktop/AI-CLI.app`

## Troubleshooting

### Shortcut not created

1. Check if Desktop directory exists
2. Check file permissions
3. Try running `ai-cli --init` again
4. Create shortcut manually (see above)

### Shortcut doesn't work

1. Verify `ai-cli` is in PATH: `which ai-cli` (Linux/macOS) or `where ai-cli` (Windows)
2. Try running `ai-cli` from terminal first
3. Check Python installation
4. Reinstall: `pip install --upgrade --force-reinstall ai-cli-launcher`

### Icon not showing (Linux)

The icon may not display if:
- Icon file is not found
- Desktop environment doesn't support .ico files

Solution: Edit the .desktop file and change `Icon=` to use a system icon like `utilities-terminal`.
