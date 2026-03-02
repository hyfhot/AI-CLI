#!/usr/bin/env python3
"""Test input handling in Windows environment."""

import sys
from ai_cli.ui.input import InputHandler, InputEvent
from ai_cli.ui.menu import MenuRenderer

def test_input_handler():
    """Test input handler key bindings."""
    print("Testing InputHandler...")
    handler = InputHandler()
    
    # Check bindings are set up
    assert handler.bindings is not None
    print("✓ Key bindings initialized")
    
    # Check all events are defined
    events = [InputEvent.UP, InputEvent.DOWN, InputEvent.ENTER, 
              InputEvent.ESCAPE, InputEvent.QUIT]
    for event in events:
        assert event is not None
    print("✓ All input events defined")
    
    print("\n✅ InputHandler test passed!")

def test_menu_renderer():
    """Test menu rendering."""
    print("\nTesting MenuRenderer...")
    menu = MenuRenderer()
    
    # Test project rendering
    items = [
        {"name": "Project 1", "type": "project"},
        {"name": "Folder 1", "type": "folder"}
    ]
    
    print("\n--- Project Menu Test ---")
    menu.render_tree(items, selected=0)
    
    # Test tool rendering
    tools = [
        {"name": "kiro-cli", "env": "WSL"},
        {"name": "claude", "env": "Win"}
    ]
    
    print("\n--- Tool Menu Test ---")
    menu.render_tools(tools, selected=0)
    
    print("\n✅ MenuRenderer test passed!")

def test_interactive():
    """Interactive test - requires user input."""
    print("\n" + "="*50)
    print("INTERACTIVE TEST")
    print("="*50)
    print("\nThis will test keyboard input.")
    print("Try pressing: ↑ ↓ Enter Esc Q")
    print("Press Q to quit the test.\n")
    
    handler = InputHandler()
    menu = MenuRenderer()
    
    items = [
        {"name": "Test Project 1", "type": "project"},
        {"name": "Test Project 2", "type": "project"},
        {"name": "Test Folder", "type": "folder"}
    ]
    
    selected = 0
    
    while True:
        menu.clear()
        menu.render_tree(items, selected)
        
        print("\nWaiting for input...")
        event = handler.get_input()
        
        if event == InputEvent.UP:
            selected = max(0, selected - 1)
            print(f"↑ UP pressed, selected: {selected}")
        elif event == InputEvent.DOWN:
            selected = min(len(items) - 1, selected + 1)
            print(f"↓ DOWN pressed, selected: {selected}")
        elif event == InputEvent.ENTER:
            print(f"✓ ENTER pressed, selected: {items[selected]['name']}")
        elif event == InputEvent.ESCAPE:
            print("← ESC pressed")
        elif event == InputEvent.QUIT:
            print("✓ QUIT pressed, exiting...")
            break
        else:
            print(f"? Unknown event: {event}")

if __name__ == "__main__":
    try:
        test_input_handler()
        test_menu_renderer()
        
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            test_interactive()
        else:
            print("\n" + "="*50)
            print("Run with --interactive to test keyboard input")
            print("="*50)
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
