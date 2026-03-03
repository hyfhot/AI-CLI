"""Git worktree management."""
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console

class GitManager:
    """Git worktree management using subprocess."""
    
    def __init__(self):
        self.console = Console()
    
    def detect_worktrees(self, path: str) -> List[Dict[str, str]]:
        """Detect Git worktrees in repository."""
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            
            worktrees = []
            current = {}
            
            for line in result.stdout.strip().split('\n'):
                if line.startswith('worktree '):
                    if current:
                        worktrees.append(current)
                    current = {'path': line[9:]}
                elif line.startswith('branch '):
                    current['branch'] = line[7:]
                elif line == 'bare':
                    current['bare'] = True
                elif line == 'detached':
                    current['detached'] = True
            
            if current:
                worktrees.append(current)
                
            return worktrees
        except subprocess.CalledProcessError:
            return []
    
    def get_branch_status(self, path: str) -> Optional[Dict[str, int]]:
        """Get branch ahead/behind status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain=v1", "--branch"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            
            first_line = result.stdout.split('\n')[0]
            if '[ahead' in first_line or '[behind' in first_line:
                ahead = behind = 0
                if 'ahead ' in first_line:
                    ahead = int(first_line.split('ahead ')[1].split(']')[0].split(',')[0])
                if 'behind ' in first_line:
                    behind = int(first_line.split('behind ')[1].split(']')[0])
                return {'ahead': ahead, 'behind': behind}
            
            return {'ahead': 0, 'behind': 0}
        except (subprocess.CalledProcessError, ValueError, IndexError):
            return None
    
    def select_worktree(self, worktrees: List[Dict[str, str]], current_path: str) -> Optional[str]:
        """Show worktree selection menu and return selected path."""
        if len(worktrees) <= 1:
            return None
        
        from ai_cli.ui.input import InputHandler, InputEvent
        from rich.live import Live
        from rich.console import Group
        from rich.text import Text
        
        selected = 0
        input_handler = InputHandler()
        
        def render_menu():
            """Render the worktree selection menu."""
            lines = []
            lines.append(Text("\n=== Select Git Worktree ===\n", style="bold cyan"))
            
            for i, wt in enumerate(worktrees):
                is_current = wt['path'] == current_path
                branch = wt.get('branch', 'detached HEAD')
                if branch.startswith('refs/heads/'):
                    branch = branch[11:]
                
                # Get status (with error handling)
                status_str = ""
                if not wt.get('detached') and not wt.get('bare'):
                    try:
                        status = self.get_branch_status(wt['path'])
                        if status:
                            if status['ahead'] > 0:
                                status_str += f" ↑{status['ahead']}"
                            if status['behind'] > 0:
                                status_str += f" ↓{status['behind']}"
                    except:
                        pass
                
                prefix = "> " if i == selected else "  "
                current_mark = " [current]" if is_current else ""
                style = "bold green" if i == selected else "dim"
                
                lines.append(Text(f"{prefix}{branch}{status_str}{current_mark}", style=style))
                lines.append(Text(f"   {wt['path']}", style="dim"))
            
            lines.append(Text("\n[↑↓] Select  [Enter] Confirm  [Esc] Cancel", style="dim"))
            return Group(*lines)
        
        self.console.clear()
        
        with Live(render_menu(), console=self.console, refresh_per_second=10) as live:
            while True:
                event = input_handler.get_input()
                
                if event == InputEvent.UP:
                    selected = max(0, selected - 1)
                    live.update(render_menu())
                elif event == InputEvent.DOWN:
                    selected = min(len(worktrees) - 1, selected + 1)
                    live.update(render_menu())
                elif event == InputEvent.ENTER:
                    return worktrees[selected]['path']
                elif event == InputEvent.ESCAPE or event == InputEvent.QUIT:
                    return None
