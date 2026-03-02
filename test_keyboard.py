#!/usr/bin/env python3
"""Test keyboard input handling."""

import sys
sys.path.insert(0, '/mnt/c/Projects/AIStudio/ai-cli-multi-platform')

from ai_cli.ui.input import InputHandler, InputEvent

def test_input():
    """Interactive test for keyboard input."""
    print("="*50)
    print("KEYBOARD INPUT TEST")
    print("="*50)
    print("\nTest each key and verify the output:")
    print("  ↑ ↓ ← → - Arrow keys")
    print("  Enter - Confirm")
    print("  N - New")
    print("  D - Delete")
    print("  Esc - Back")
    print("  Q - Quit")
    print("\nPress Q to exit test\n")
    
    handler = InputHandler()
    
    while True:
        print("Waiting for key press...")
        event = handler.get_input()
        
        if event == InputEvent.UP:
            print("✓ UP arrow detected")
        elif event == InputEvent.DOWN:
            print("✓ DOWN arrow detected")
        elif event == InputEvent.LEFT:
            print("✓ LEFT arrow detected")
        elif event == InputEvent.RIGHT:
            print("✓ RIGHT arrow detected")
        elif event == InputEvent.ENTER:
            print("✓ ENTER detected")
        elif event == InputEvent.NEW:
            print("✓ N (NEW) detected")
        elif event == InputEvent.DELETE:
            print("✓ D (DELETE) detected")
        elif event == InputEvent.ESCAPE:
            print("✓ ESC (ESCAPE) detected")
        elif event == InputEvent.QUIT:
            print("✓ Q (QUIT) detected - Exiting...")
            break
        else:
            print(f"? Unknown event: {event}")
        
        print()

if __name__ == "__main__":
    try:
        test_input()
        print("\n✅ Test completed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
