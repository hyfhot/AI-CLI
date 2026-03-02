#!/usr/bin/env python3
"""Test subprocess with CREATE_NEW_CONSOLE."""

import subprocess
import sys

print("=== Testing CREATE_NEW_CONSOLE ===\n")

# Test 1: WSL in new console
print("Test 1: WSL in new console window")
cmd = ["wsl.exe", "-e", "bash", "-ic", "cd '/mnt/c/Projects/AIStudio/AI-CLI'; kiro-cli --version; exec bash"]
print(f"Command: {' '.join(cmd)}")

try:
    if sys.platform == 'win32':
        proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(f"✓ Process started with PID: {proc.pid}")
        print("Check if a new console window opened with kiro-cli")
    else:
        print("✗ Not on Windows, skipping test")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "="*50)
input("Press Enter to continue to Test 2...")

# Test 2: Windows Terminal new tab
print("\nTest 2: Windows Terminal new tab")
cmd = ["wt.exe", "-w", "0", "new-tab", "--title", "Test", "wsl", "-e", "bash", "-ic", "cd '/mnt/c/Projects/AIStudio/AI-CLI'; kiro-cli --version; exec bash"]
print(f"Command: wt.exe -w 0 new-tab --title Test wsl ...")

try:
    proc = subprocess.Popen(cmd)
    print(f"✓ Process started with PID: {proc.pid}")
    print("Check if a new tab opened in Windows Terminal")
except FileNotFoundError:
    print("✗ wt.exe not found - Windows Terminal not installed")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "="*50)
print("Tests complete!")
