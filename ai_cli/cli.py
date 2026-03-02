"""CLI command line interface."""
import click
import os
import platform
import subprocess
from pathlib import Path

__version__ = "3.1.0"


@click.command()
@click.option('--init', '-i', is_flag=True, help='Initialize configuration file')
@click.option('--config', '-c', is_flag=True, help='Open configuration file for editing')
@click.option('--uninstall', '-u', is_flag=True, help='Uninstall AI-CLI')
@click.option('--version', '-v', is_flag=True, help='Show version information')
def main(init, config, uninstall, version):
    """AI-CLI: Terminal launcher for AI coding assistants."""
    
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
        from .app import Application
        app = Application()
        app.run()
    except KeyboardInterrupt:
        click.echo("\nGoodbye!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


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
        
        # On Windows, remove desktop shortcut if exists
        if platform.system() == "Windows":
            desktop = Path.home() / "Desktop"
            # Try both old and new shortcut names
            for shortcut_name in ["AI-CLI 3.0.lnk", "AI-CLI.lnk"]:
                shortcut = desktop / shortcut_name
                if shortcut.exists():
                    shortcut.unlink()
                    click.echo(f"  Removed desktop shortcut: {shortcut_name}")
        
        click.echo("\nUninstallation complete!")
        click.echo("To remove the program, run: pip uninstall ai-cli")
        click.echo("Your configuration has been preserved for future use.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == '__main__':
    main()
