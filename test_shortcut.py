#!/usr/bin/env python3
"""Test desktop shortcut creation on different platforms."""

import platform
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_cli.cli import create_desktop_shortcut, remove_desktop_shortcut

def test_create():
    """Test creating desktop shortcut."""
    print(f"Testing on {platform.system()}...")
    print("Creating desktop shortcut...")
    
    try:
        create_desktop_shortcut()
        print("✓ Shortcut created successfully!")
        
        # Check if shortcut exists
        system = platform.system()
        if system == "Windows":
            shortcut = Path.home() / "Desktop" / "AI-CLI.lnk"
            if shortcut.exists():
                print(f"✓ Verified: {shortcut}")
            else:
                print(f"✗ Not found: {shortcut}")
        
        elif system == "Linux":
            desktop_dirs = [
                Path.home() / "Desktop" / "ai-cli.desktop",
                Path.home() / "desktop" / "ai-cli.desktop",
                Path.home() / ".local" / "share" / "applications" / "ai-cli.desktop"
            ]
            found = False
            for shortcut in desktop_dirs:
                if shortcut.exists():
                    print(f"✓ Verified: {shortcut}")
                    found = True
                    break
            if not found:
                print("✗ Shortcut not found in any location")
        
        elif system == "Darwin":
            app_path = Path.home() / "Desktop" / "AI-CLI.app"
            if app_path.exists():
                print(f"✓ Verified: {app_path}")
            else:
                print(f"✗ Not found: {app_path}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_remove():
    """Test removing desktop shortcut."""
    print("\nRemoving desktop shortcut...")
    
    try:
        remove_desktop_shortcut()
        print("✓ Shortcut removed successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        test_remove()
    else:
        test_create()
