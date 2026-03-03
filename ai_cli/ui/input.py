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
        """Get text input with ESC cancellation support using raw keyboard input."""
        import sys
        
        # Print prompt
        sys.stdout.write(prompt)
        if placeholder:
            sys.stdout.write(placeholder)
        sys.stdout.flush()
        
        # Use raw keyboard input for immediate ESC response
        if sys.platform == 'win32':
            return self._get_text_input_windows(placeholder, allow_cancel)
        else:
            return self._get_text_input_unix(placeholder, allow_cancel)
    
    def _get_text_input_unix(self, initial: str = "", allow_cancel: bool = True) -> Optional[str]:
        """Get text input on Unix with raw keyboard handling."""
        import sys
        import tty
        import termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        buffer = list(initial)
        cursor_pos = len(buffer)
        
        try:
            tty.setraw(fd)
            
            while True:
                ch = sys.stdin.read(1)
                
                # ESC key - immediate cancel
                if ch == '\x1b':
                    # Check if it's a standalone ESC or part of escape sequence
                    import select
                    if select.select([sys.stdin], [], [], 0.0)[0]:
                        # More data available, it's an escape sequence
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            # Ignore arrow keys in text input
                            continue
                    else:
                        # Standalone ESC - cancel
                        if allow_cancel:
                            sys.stdout.write('\n')
                            sys.stdout.flush()
                            return None
                
                # Enter key
                elif ch == '\r' or ch == '\n':
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    return ''.join(buffer)
                
                # Backspace
                elif ch == '\x7f' or ch == '\x08':
                    if cursor_pos > 0:
                        buffer.pop(cursor_pos - 1)
                        cursor_pos -= 1
                        # Redraw line
                        sys.stdout.write('\r' + ' ' * (len(buffer) + 10) + '\r')
                        sys.stdout.write(''.join(buffer))
                        sys.stdout.flush()
                
                # Ctrl+C
                elif ch == '\x03':
                    if allow_cancel:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                        return None
                
                # Regular character
                elif ch.isprintable():
                    buffer.insert(cursor_pos, ch)
                    cursor_pos += 1
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _get_text_input_windows(self, initial: str = "", allow_cancel: bool = True) -> Optional[str]:
        """Get text input on Windows with raw keyboard handling."""
        import sys
        import msvcrt
        
        buffer = list(initial)
        cursor_pos = len(buffer)
        
        while True:
            ch = msvcrt.getch()
            
            # ESC key - immediate cancel
            if ch == b'\x1b':
                if allow_cancel:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    return None
            
            # Enter key
            elif ch == b'\r':
                sys.stdout.write('\n')
                sys.stdout.flush()
                return ''.join(buffer)
            
            # Backspace
            elif ch == b'\x08':
                if cursor_pos > 0:
                    buffer.pop(cursor_pos - 1)
                    cursor_pos -= 1
                    # Redraw line
                    sys.stdout.write('\r' + ' ' * (len(buffer) + 10) + '\r')
                    sys.stdout.write(''.join(buffer))
                    sys.stdout.flush()
            
            # Ctrl+C
            elif ch == b'\x03':
                if allow_cancel:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    return None
            
            # Arrow keys and special keys
            elif ch in (b'\xe0', b'\x00'):
                msvcrt.getch()  # Consume second byte
                continue
            
            # Regular character
            else:
                try:
                    char = ch.decode('utf-8')
                    if char.isprintable():
                        buffer.insert(cursor_pos, char)
                        cursor_pos += 1
                        sys.stdout.write(char)
                        sys.stdout.flush()
                except:
                    pass
    
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
