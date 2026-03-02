"""CLI command line interface."""
import click
import os
import platform
import subprocess
from pathlib import Path

__version__ = "0.1.0"


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
            click.echo(f"Configuration already exists: {config_file}")
        else:
            config = manager.create_default()
            manager.save(config)
            click.echo(f"Configuration created: {config_file}")
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
            shortcut = desktop / "AI-CLI.lnk"
            if shortcut.exists():
                shortcut.unlink()
                click.echo("  Removed desktop shortcut")
        
        click.echo("\nUninstallation complete!")
        click.echo("To remove the program, run: pip uninstall ai-cli")
        click.echo("Your configuration has been preserved for future use.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == '__main__':
    main()
