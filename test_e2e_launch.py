#!/usr/bin/env python3
"""End-to-end test for WSL tool launch."""

import sys
import subprocess
sys.path.insert(0, '.')

from ai_cli.platform.windows import WindowsPlatformAdapter
from ai_cli.models import Tool, ProjectNode, ToolEnvironment

print("=== End-to-End WSL Launch Test ===\n")

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

print(f"Tool: {tool.name}")
print(f"Project: {project.name}")
print(f"Path: {project.path}\n")

# Test launch
print("Testing launch_terminal()...")
try:
    adapter.launch_terminal(tool, project, new_tab=False)
    print("✓ Launch command executed successfully")
    print("\nCheck if a new window opened with kiro-cli running.")
    print("If not, check the error messages above.")
except Exception as e:
    print(f"✗ Launch failed: {e}")
    import traceback
    traceback.print_exc()
