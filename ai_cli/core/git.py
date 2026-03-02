"""Git worktree management."""
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

class GitManager:
    """Git worktree management using subprocess."""
    
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
