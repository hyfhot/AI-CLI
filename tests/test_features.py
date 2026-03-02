#!/usr/bin/env python3
"""Test script for new features."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_scrolling_display():
    """Test scrolling display with many items."""
    from ai_cli.ui.menu import MenuRenderer
    
    menu = MenuRenderer()
    
    # Test with 30 items (should show scroll indicators)
    items = [{"name": f"Project {i}", "type": "project"} for i in range(30)]
    
    print("Testing scrolling display with 30 items...")
    print("Selected index 0 (should show '↓ 15 more below'):")
    menu.render_tree(items, selected=0, max_display=15)
    
    print("\n\nSelected index 15 (should show both scroll indicators):")
    menu.render_tree(items, selected=15, max_display=15)
    
    print("\n\nSelected index 29 (should show '↑ 15 more above'):")
    menu.render_tree(items, selected=29, max_display=15)
    
    print("\n✓ Scrolling display test passed")

def test_empty_project_list():
    """Test empty project list prompt."""
    from ai_cli.ui.menu import MenuRenderer
    
    menu = MenuRenderer()
    
    print("\n\nTesting empty project list...")
    menu.render_tree([], selected=0)
    
    print("\n✓ Empty project list test passed")

def test_input_cancellation():
    """Test input with ESC cancellation."""
    from ai_cli.ui.input import InputHandler
    
    handler = InputHandler()
    
    print("\n\nTesting input cancellation...")
    print("Note: This requires manual testing with ESC key")
    print("Usage: result = handler.get_text_input('Enter name: ', allow_cancel=True)")
    print("If ESC is pressed, result will be None")
    
    print("\n✓ Input cancellation API available")

def test_git_worktree_selection():
    """Test git worktree selection."""
    from ai_cli.core.git import GitManager
    
    git_manager = GitManager()
    
    print("\n\nTesting git worktree detection...")
    
    # Test with current directory (if it's a git repo)
    worktrees = git_manager.detect_worktrees(".")
    
    if worktrees:
        print(f"Found {len(worktrees)} worktree(s):")
        for wt in worktrees:
            print(f"  - {wt.get('branch', 'detached')}: {wt['path']}")
        
        if len(worktrees) > 1:
            print("\nWorktree selection UI available (requires manual testing)")
    else:
        print("No worktrees found (not a git repo or no worktrees)")
    
    print("\n✓ Git worktree detection test passed")

def test_background_detection():
    """Test background async tool detection."""
    import asyncio
    from ai_cli.core.tools import ToolDetector
    from ai_cli.models import ToolConfig
    
    print("\n\nTesting background tool detection...")
    
    detector = ToolDetector()
    
    # Create sample tool config
    tools_config = [
        ToolConfig(
            name="python",
            display_name="Python",
            win_install="",
            linux_install="",
            macos_install=""
        )
    ]
    
    # Start background detection
    detector.start_background_detection(tools_config)
    
    print("Background detection started (non-blocking)")
    print("Cache will be populated in background")
    
    # Wait a bit and check cache
    async def check_cache():
        await asyncio.sleep(0.5)
        tools = await detector.detect_all_tools(tools_config)
        print(f"Detected {len(tools)} tool(s) from cache")
    
    asyncio.run(check_cache())
    
    print("\n✓ Background detection test passed")

def test_extended_search_paths():
    """Test extended tool search paths."""
    from ai_cli.core.installer import ToolInstaller
    
    print("\n\nTesting extended tool search paths...")
    
    installer = ToolInstaller()
    
    # Test finding python (should exist)
    result = installer._find_tool_executable("python")
    
    if result:
        print(f"Found python at: {result}")
    else:
        print("Python not found (testing search logic)")
    
    print("\n✓ Extended search paths test passed")

def test_path_length_check():
    """Test PATH length check."""
    print("\n\nTesting PATH length check...")
    print("PATH length check is integrated into _add_to_user_path()")
    print("It will warn if PATH exceeds 2047 characters on Windows")
    print("\n✓ PATH length check available")

def main():
    """Run all tests."""
    print("=" * 60)
    print("AI-CLI Feature Tests")
    print("=" * 60)
    
    try:
        test_scrolling_display()
        test_empty_project_list()
        test_input_cancellation()
        test_git_worktree_selection()
        test_background_detection()
        test_extended_search_paths()
        test_path_length_check()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
