"""
Uninstall script for AI-CLI Launcher.
Run this before pip uninstall to clean up shortcuts and config.
"""
import platform
import subprocess
import sys
from pathlib import Path


def cleanup():
    """Clean up shortcuts and show config location."""
    print("Cleaning up AI-CLI Launcher...")
    
    # Remove Windows desktop shortcut
    if platform.system() == "Windows":
        desktop = Path.home() / "Desktop"
        for shortcut_name in ["AI-CLI 3.0.lnk", "AI-CLI.lnk"]:
            shortcut = desktop / shortcut_name
            if shortcut.exists():
                shortcut.unlink()
                print(f"✓ Removed desktop shortcut: {shortcut_name}")
    
    # Show config location
    if platform.system() == "Windows":
        config_dir = Path.home() / "AppData" / "Roaming" / "AI-CLI"
    elif platform.system() == "Darwin":
        config_dir = Path.home() / "Library" / "Application Support" / "ai-cli"
    else:
        config_dir = Path.home() / ".config" / "ai-cli"
    
    if config_dir.exists():
        print(f"\n📁 Configuration preserved at: {config_dir}")
        print(f"   To remove: rm -rf {config_dir}")
    
    print("\n✓ Cleanup complete!")


def uninstall():
    """Run cleanup and pip uninstall."""
    cleanup()
    
    print("\nUninstalling package...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "ai-cli-launcher", "-y"], check=True)
        print("\n✓ AI-CLI Launcher has been uninstalled successfully!")
    except subprocess.CalledProcessError:
        print("\n✗ Failed to uninstall. Please run manually:")
        print("  pip uninstall ai-cli-launcher")
        sys.exit(1)


if __name__ == "__main__":
    uninstall()
