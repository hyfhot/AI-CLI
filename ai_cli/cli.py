"""CLI command line interface."""
import click
import os
import platform
import subprocess
import sys
from pathlib import Path
from . import __version__

# Debug output helper
def debug_print(msg):
    """Print debug message to both stdout and stderr."""
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)
    print(f"[DEBUG] {msg}", flush=True)


@click.command()
@click.option('--init', '-i', is_flag=True, help='Initialize configuration file')
@click.option('--config', '-c', is_flag=True, help='Open configuration file for editing')
@click.option('--uninstall', '-u', is_flag=True, help='Uninstall AI-CLI')
@click.option('--version', '-v', is_flag=True, help='Show version information')
@click.option('--lang', '-l', type=click.Choice(['auto', 'en', 'zh', 'ja', 'de'], case_sensitive=False), help='Set language (auto, en, zh, ja, de)')
def main(init, config, uninstall, version, lang):
    """AI-CLI: Terminal launcher for AI coding assistants."""
    
    # Enable debug mode if --debug flag is present
    debug_mode = '--debug' in sys.argv
    if debug_mode:
        print("[DEBUG] Debug mode enabled", flush=True)
        print(f"[DEBUG] Python version: {sys.version}", flush=True)
        print(f"[DEBUG] Platform: {sys.platform}", flush=True)
    
    if version:
        click.echo(f"AI-CLI version {__version__}")
        return
    
    if init:
        init_config()
        return
    
    if config:
        edit_config()
        return
    
    if uninstall:
        uninstall_app()
        return
    
    # Default: start interactive interface
    try:
        if debug_mode:
            print("[DEBUG] Starting Application", flush=True)
        from .app import Application
        app = Application(language=lang)
        app.run()
    except KeyboardInterrupt:
        click.echo("\nGoodbye!")
    except Exception as e:
        import traceback
        click.echo(f"Error: {e}", err=True)
        click.echo("\nFull traceback:", err=True)
        click.echo(traceback.format_exc(), err=True)


def init_config():
    """Initialize default configuration."""
    try:
        from .config import ConfigManager
        
        manager = ConfigManager()
        config_dir = manager.get_config_dir()
        config_file = config_dir / "config.json"
        
        if config_file.exists():
            # Config exists - merge tools incrementally
            click.echo(f"Configuration exists: {config_file}")
            click.echo("Updating tool definitions...")
            
            existing_config = manager.load()
            default_config = manager.create_default_tools()
            
            # Keep existing projects
            # Merge tools: add new tools from default, keep user custom tools
            existing_tool_names = {t.name for t in existing_config.tools}
            default_tool_names = {t.name for t in default_config}
            
            # Add new default tools that don't exist
            for tool in default_config:
                if tool.name not in existing_tool_names:
                    existing_config.tools.append(tool)
                    click.echo(f"  Added: {tool.display_name}")
            
            # Update existing default tools (keep user custom tools unchanged)
            for i, tool in enumerate(existing_config.tools):
                if tool.name in default_tool_names:
                    # Find matching default tool
                    for default_tool in default_config:
                        if default_tool.name == tool.name:
                            # Update tool definition
                            existing_config.tools[i] = default_tool
                            click.echo(f"  Updated: {tool.display_name}")
                            break
            
            manager.save(existing_config)
            click.echo(f"Configuration updated: {config_file}")
        else:
            # No config - create new
            config = manager.create_default()
            manager.save(config)
            click.echo(f"Configuration created: {config_file}")
        
        # Create desktop shortcut
        create_desktop_shortcut()
        
        click.echo("")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def edit_config():
    """Open configuration file with system editor."""
    try:
        from .config import ConfigManager
        
        manager = ConfigManager()
        config_dir = manager.get_config_dir()
        config_file = config_dir / "config.json"
        
        if not config_file.exists():
            click.echo("Configuration not found. Run 'ai-cli --init' first.")
            return
        
        system = platform.system()
        
        if system == "Windows":
            subprocess.run(["notepad", str(config_file)])
        elif system == "Darwin":
            subprocess.run(["open", str(config_file)])
        else:
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, str(config_file)])
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def uninstall_app():
    """Uninstall AI-CLI."""
    try:
        from .config import ConfigManager
        
        click.echo("Uninstalling AI-CLI...")
        
        manager = ConfigManager()
        config_dir = manager.get_config_dir()
        
        # Show config location but don't delete
        if config_dir.exists():
            click.echo(f"  Configuration preserved at: {config_dir}")
            click.echo("  (Run manually to remove: rm -rf {})".format(config_dir))
        
        # Remove desktop shortcut
        remove_desktop_shortcut()
        
        click.echo("\nUninstallation complete!")
        click.echo("To remove the program, run: pip uninstall ai-cli-launcher")
        click.echo("Your configuration has been preserved for future use.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def create_desktop_shortcut():
    """Create desktop shortcut for AI-CLI."""
    system = platform.system()
    
    try:
        if system == "Windows":
            _create_windows_shortcut()
        elif system == "Linux":
            _create_linux_shortcut()
        elif system == "Darwin":
            _create_macos_shortcut()
    except Exception as e:
        click.echo(f"  Warning: Could not create desktop shortcut: {e}")


def _create_windows_shortcut():
    """Create Windows desktop shortcut."""
    import sys
    
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "AI-CLI.lnk"
    
    # Get Python executable and script path
    python_exe = sys.executable
    script_path = Path(sys.executable).parent / "Scripts" / "ai-cli.exe"
    
    # If ai-cli.exe doesn't exist, use python -m ai_cli.cli
    if not script_path.exists():
        script_path = python_exe
        args = "-m ai_cli.cli"
    else:
        args = ""
    
    # Get icon path
    icon_path = Path(__file__).parent.parent / "ai-cli.ico"
    if not icon_path.exists():
        icon_path = python_exe  # Fallback to Python icon
    
    # Create shortcut using PowerShell
    ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{script_path}"
$Shortcut.Arguments = "{args}"
$Shortcut.IconLocation = "{icon_path}"
$Shortcut.Description = "AI-CLI Launcher"
$Shortcut.Save()
"""
    
    result = subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        click.echo(f"  Created desktop shortcut: {shortcut_path}")
    else:
        raise Exception(f"PowerShell error: {result.stderr}")


def _create_linux_shortcut():
    """Create Linux desktop shortcut (.desktop file)."""
    import sys
    
    # Try both Desktop and desktop
    desktop_dirs = [
        Path.home() / "Desktop",
        Path.home() / "desktop",
        Path.home() / ".local" / "share" / "applications"
    ]
    
    desktop = None
    for d in desktop_dirs:
        if d.exists():
            desktop = d
            break
    
    if not desktop:
        click.echo("  Desktop directory not found, skipping shortcut creation")
        return
    
    shortcut_path = desktop / "ai-cli.desktop"
    
    # Get Python executable and script path
    python_exe = sys.executable
    script_path = Path(sys.executable).parent / "ai-cli"
    
    if not script_path.exists():
        # Try to find in PATH
        result = subprocess.run(["which", "ai-cli"], capture_output=True, text=True)
        if result.returncode == 0:
            script_path = result.stdout.strip()
        else:
            script_path = f"{python_exe} -m ai_cli.cli"
    
    # Get icon path
    icon_path = Path(__file__).parent.parent / "ai-cli.ico"
    if not icon_path.exists():
        icon_path = "utilities-terminal"  # Fallback to system icon
    
    # Create .desktop file
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=AI-CLI
Comment=AI-CLI Launcher for AI Coding Assistants
Exec={script_path}
Icon={icon_path}
Terminal=true
Categories=Development;Utility;
"""
    
    shortcut_path.write_text(desktop_content)
    shortcut_path.chmod(0o755)
    
    click.echo(f"  Created desktop shortcut: {shortcut_path}")


def _create_macos_shortcut():
    """Create macOS desktop shortcut (app bundle or alias)."""
    import sys
    
    desktop = Path.home() / "Desktop"
    app_path = desktop / "AI-CLI.app"
    
    # Get Python executable and script path
    python_exe = sys.executable
    script_path = Path(sys.executable).parent / "ai-cli"
    
    if not script_path.exists():
        # Try to find in PATH
        result = subprocess.run(["which", "ai-cli"], capture_output=True, text=True)
        if result.returncode == 0:
            script_path = result.stdout.strip()
        else:
            script_path = f"{python_exe} -m ai_cli.cli"
    
    # Create app bundle structure
    contents_dir = app_path / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Create launcher script
    launcher_script = macos_dir / "ai-cli"
    launcher_content = f"""#!/bin/bash
osascript -e 'tell application "Terminal" to do script "{script_path}"'
"""
    launcher_script.write_text(launcher_content)
    launcher_script.chmod(0o755)
    
    # Create Info.plist
    info_plist = contents_dir / "Info.plist"
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ai-cli</string>
    <key>CFBundleIdentifier</key>
    <string>org.ai-cli.launcher</string>
    <key>CFBundleName</key>
    <string>AI-CLI</string>
    <key>CFBundleVersion</key>
    <string>3.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>3.0.0</string>
</dict>
</plist>
"""
    info_plist.write_text(plist_content)
    
    click.echo(f"  Created desktop app: {app_path}")


def remove_desktop_shortcut():
    """Remove desktop shortcut."""
    system = platform.system()
    
    try:
        if system == "Windows":
            desktop = Path.home() / "Desktop"
            for shortcut_name in ["AI-CLI 3.0.lnk", "AI-CLI.lnk"]:
                shortcut = desktop / shortcut_name
                if shortcut.exists():
                    shortcut.unlink()
                    click.echo(f"  Removed desktop shortcut: {shortcut_name}")
        
        elif system == "Linux":
            desktop_dirs = [
                Path.home() / "Desktop",
                Path.home() / "desktop",
                Path.home() / ".local" / "share" / "applications"
            ]
            
            for desktop in desktop_dirs:
                shortcut = desktop / "ai-cli.desktop"
                if shortcut.exists():
                    shortcut.unlink()
                    click.echo(f"  Removed desktop shortcut: {shortcut}")
        
        elif system == "Darwin":
            desktop = Path.home() / "Desktop"
            app_path = desktop / "AI-CLI.app"
            if app_path.exists():
                import shutil
                shutil.rmtree(app_path)
                click.echo(f"  Removed desktop app: {app_path}")
    
    except Exception as e:
        click.echo(f"  Warning: Could not remove desktop shortcut: {e}")


if __name__ == '__main__':
    main()
