"""Keyboard input handling."""
import sys
from enum import Enum
from typing import Optional

class InputEvent(Enum):
    """Input event types."""
    UP = "up"
    DOWN = "down" 
    LEFT = "left"
    RIGHT = "right"
    ENTER = "enter"
    ESCAPE = "escape"
    NEW = "new"
    DELETE = "delete"
    INSTALL = "install"
    RUN = "run"
    QUIT = "quit"
    NEW_TAB = "new_tab"  # T key for new tab
    CANCEL = "cancel"  # ESC in input mode

class InputHandler:
    """Handles keyboard input using raw terminal mode."""
    
    def get_input(self) -> Optional[InputEvent]:
        """Get next input event."""
        if sys.platform == 'win32':
            return self._get_input_windows()
        else:
            return self._get_input_unix()
    
    def get_text_input(self, prompt: str, placeholder: str = "", allow_cancel: bool = True) -> Optional[str]:
        """Get text input with ESC cancellation support."""
        from prompt_toolkit import prompt as pt_prompt
        from prompt_toolkit.key_binding import KeyBindings
        
        bindings = KeyBindings()
        
        @bindings.add('escape')
        def _(event):
            if allow_cancel:
                event.app.exit(result='__CANCEL__')
        
        try:
            result = pt_prompt(
                prompt,
                default=placeholder,
                key_bindings=bindings if allow_cancel else None
            )
            
            if result == '__CANCEL__':
                return None
            
            return result.strip() if result else None
        except (KeyboardInterrupt, EOFError):
            return None
    
    def _get_input_unix(self) -> Optional[InputEvent]:
        """Get input on Unix/Linux/macOS."""
        import tty
        import termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            
            # Handle escape sequences
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':
                        return InputEvent.UP
                    elif ch3 == 'B':
                        return InputEvent.DOWN
                    elif ch3 == 'C':
                        return InputEvent.RIGHT
                    elif ch3 == 'D':
                        return InputEvent.LEFT
                else:
                    return InputEvent.ESCAPE
            
            # Handle regular keys
            if ch == '\r' or ch == '\n':
                return InputEvent.ENTER
            elif ch == '\x03':  # Ctrl+C
                return InputEvent.QUIT
            elif ch.lower() == 'n':
                return InputEvent.NEW
            elif ch.lower() == 'd':
                return InputEvent.DELETE
            elif ch.lower() == 'i':
                return InputEvent.INSTALL
            elif ch.lower() == 'r':
                return InputEvent.RUN
            elif ch.lower() == 't':
                return InputEvent.NEW_TAB
            elif ch.lower() == 'q':
                return InputEvent.QUIT
            
            return None
        except (KeyboardInterrupt, EOFError):
            return InputEvent.QUIT
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _get_input_windows(self) -> Optional[InputEvent]:
        """Get input on Windows."""
        import msvcrt
        
        try:
            # Wait for key press (blocking)
            ch = msvcrt.getch()
            
            # Handle special keys
            if ch in (b'\xe0', b'\x00'):
                ch2 = msvcrt.getch()
                if ch2 == b'H':
                    return InputEvent.UP
                elif ch2 == b'P':
                    return InputEvent.DOWN
                elif ch2 == b'M':
                    return InputEvent.RIGHT
                elif ch2 == b'K':
                    return InputEvent.LEFT
                return None
            
            # Handle regular keys
            if ch == b'\r':
                return InputEvent.ENTER
            elif ch == b'\x1b':
                return InputEvent.ESCAPE
            elif ch == b'\x03':  # Ctrl+C
                return InputEvent.QUIT
            elif ch.lower() == b'n':
                return InputEvent.NEW
            elif ch.lower() == b'd':
                return InputEvent.DELETE
            elif ch.lower() == b'i':
                return InputEvent.INSTALL
            elif ch.lower() == b'r':
                return InputEvent.RUN
            elif ch.lower() == b't':
                return InputEvent.NEW_TAB
            elif ch.lower() == b'q':
                return InputEvent.QUIT
            
            return None
        except (KeyboardInterrupt, EOFError):
            return InputEvent.QUIT
