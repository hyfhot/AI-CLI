#!/usr/bin/env python3
"""Simple syntax and import test without dependencies."""

import sys
import ast

def test_syntax():
    """Test Python syntax of modified files."""
    files = [
        'ai_cli/ui/menu.py',
        'ai_cli/ui/input.py',
        'ai_cli/app.py'
    ]
    
    print("Testing Python syntax...")
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
                ast.parse(code)
            print(f"✓ {file}")
        except SyntaxError as e:
            print(f"✗ {file}: {e}")
            return False
    
    return True

def test_structure():
    """Test code structure."""
    print("\nTesting code structure...")
    
    # Check menu.py has operation hints
    with open('ai_cli/ui/menu.py', 'r') as f:
        menu_code = f.read()
        if '[↑↓] Select' in menu_code:
            print("✓ Menu has operation hints")
        else:
            print("✗ Menu missing operation hints")
            return False
    
    # Check input.py has individual key bindings
    with open('ai_cli/ui/input.py', 'r') as f:
        input_code = f.read()
        if "@self.bindings.add('n')" in input_code:
            print("✓ Input handler has individual key bindings")
        else:
            print("✗ Input handler missing individual key bindings")
            return False
    
    # Check app.py has empty list handling
    with open('ai_cli/app.py', 'r') as f:
        app_code = f.read()
        if 'if not items:' in app_code:
            print("✓ App has empty list handling")
        else:
            print("✗ App missing empty list handling")
            return False
    
    return True

if __name__ == "__main__":
    try:
        if test_syntax() and test_structure():
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
