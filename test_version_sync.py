#!/usr/bin/env python3
"""Test version synchronization across all files."""

import re
import sys
from pathlib import Path

def get_version_from_file(file_path, pattern):
    """Extract version from file using regex pattern."""
    content = Path(file_path).read_text()
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

def main():
    """Check version consistency."""
    print("Checking version synchronization...\n")
    
    # Get versions from different files
    versions = {}
    
    # pyproject.toml
    versions['pyproject.toml'] = get_version_from_file(
        'pyproject.toml',
        r'version\s*=\s*"([^"]+)"'
    )
    
    # ai_cli/__init__.py
    versions['ai_cli/__init__.py'] = get_version_from_file(
        'ai_cli/__init__.py',
        r'__version__\s*=\s*"([^"]+)"'
    )
    
    # Display versions
    all_same = True
    reference_version = None
    
    for file, version in versions.items():
        if version:
            print(f"  {file:30s} : {version}")
            if reference_version is None:
                reference_version = version
            elif version != reference_version:
                all_same = False
        else:
            print(f"  {file:30s} : NOT FOUND")
            all_same = False
    
    print()
    
    # Test import
    try:
        from ai_cli import __version__ as init_version
        from ai_cli.cli import __version__ as cli_version
        
        print(f"  Runtime import (__init__):     {init_version}")
        print(f"  Runtime import (cli):          {cli_version}")
        
        if init_version != cli_version:
            print("\n✗ ERROR: Runtime versions don't match!")
            all_same = False
        elif init_version != reference_version:
            print("\n✗ ERROR: Runtime version doesn't match file versions!")
            all_same = False
    except Exception as e:
        print(f"\n✗ ERROR: Failed to import: {e}")
        all_same = False
    
    print()
    
    if all_same:
        print("✓ All versions are synchronized!")
        print(f"  Version: {reference_version}")
        return 0
    else:
        print("✗ Version mismatch detected!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
