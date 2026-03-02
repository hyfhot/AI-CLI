#!/usr/bin/env python3
"""Test WSL launch command."""

import sys
sys.path.insert(0, '.')

from ai_cli.platform.windows import WindowsPlatformAdapter
from ai_cli.models import Tool, ProjectNode, ToolEnvironment

# Create test objects
adapter = WindowsPlatformAdapter()
tool = Tool(
    name='kiro-cli',
    display_name='Kiro CLI',
    environment=ToolEnvironment.WSL,
    available=True,
    version=None
)
project = ProjectNode(
    name='AI-CLI',
    path='C:\\Projects\\AIStudio\\AI-CLI',
    type='project'
)

# Test command generation
print("=== Testing WSL Launch Command ===\n")

# Simulate launch_terminal logic
from ai_cli.utils import PathConverter

wsl_path = PathConverter.to_wsl_path(project.path)
print(f"Project path: {project.path}")
print(f"WSL path: {wsl_path}")

wsl_command = f"cd {wsl_path} && {tool.name}"
print(f"\nWSL command: {wsl_command}")

# Test new window
title = f"{tool.name} - {project.name}"
cmd_window = ["wt.exe", "new-window", "--title", title, "wsl.exe", "bash", "-ic", wsl_command]
print(f"\nNew window command:")
print(" ".join(f'"{arg}"' if ' ' in arg else arg for arg in cmd_window))

# Test new tab
cmd_tab = ["wt.exe", "-w", "0", "new-tab", "--title", title, "wsl.exe", "bash", "-ic", wsl_command]
print(f"\nNew tab command:")
print(" ".join(f'"{arg}"' if ' ' in arg else arg for arg in cmd_tab))

# Test the command manually
print("\n=== Manual Test ===")
print("Run this command to test:")
print(f'wsl.exe bash -ic "{wsl_command}"')
