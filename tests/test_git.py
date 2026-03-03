"""Tests for Git integration."""
import pytest
from unittest.mock import Mock, patch
from ai_cli.core.git import GitManager


class TestGitManager:
    """Test GitManager class."""
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_detect_worktrees_success(self, mock_run):
        """Test successful worktree detection."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="worktree /path/to/main\nbranch refs/heads/main\n\nworktree /path/to/feature\nbranch refs/heads/feature\n"
        )
        
        manager = GitManager()
        worktrees = manager.detect_worktrees("/path/to/repo")
        
        assert len(worktrees) == 2
        assert worktrees[0]['path'] == '/path/to/main'
        assert worktrees[0]['branch'] == 'refs/heads/main'
        assert worktrees[1]['path'] == '/path/to/feature'
        assert worktrees[1]['branch'] == 'refs/heads/feature'
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_detect_worktrees_failure(self, mock_run):
        """Test worktree detection failure."""
        mock_run.side_effect = Exception("Git command failed")
        
        manager = GitManager()
        worktrees = manager.detect_worktrees("/path/to/repo")
        
        assert worktrees == []
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_detect_worktrees_bare(self, mock_run):
        """Test bare repository detection."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="worktree /path/to/bare\nbare\n"
        )
        
        manager = GitManager()
        worktrees = manager.detect_worktrees("/path/to/repo")
        
        assert len(worktrees) == 1
        assert worktrees[0]['bare'] is True
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_detect_worktrees_detached(self, mock_run):
        """Test detached HEAD detection."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="worktree /path/to/detached\ndetached\n"
        )
        
        manager = GitManager()
        worktrees = manager.detect_worktrees("/path/to/repo")
        
        assert len(worktrees) == 1
        assert worktrees[0]['detached'] is True
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_ahead(self, mock_run):
        """Test branch ahead status."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="## main...origin/main [ahead 3]\n"
        )
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/repo")
        
        assert status is not None
        assert status['ahead'] == 3
        assert status['behind'] == 0
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_behind(self, mock_run):
        """Test branch behind status."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="## main...origin/main [behind 2]\n"
        )
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/repo")
        
        assert status is not None
        assert status['ahead'] == 0
        assert status['behind'] == 2
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_ahead_behind(self, mock_run):
        """Test branch ahead and behind status."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="## main...origin/main [ahead 3, behind 2]\n"
        )
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/repo")
        
        assert status is not None
        assert status['ahead'] == 3
        assert status['behind'] == 2
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_up_to_date(self, mock_run):
        """Test branch up to date status."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="## main...origin/main\n"
        )
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/repo")
        
        assert status is not None
        assert status['ahead'] == 0
        assert status['behind'] == 0
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_failure(self, mock_run):
        """Test branch status failure."""
        mock_run.side_effect = Exception("Git command failed")
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/repo")
        
        assert status is None
    
    @patch('ai_cli.core.git.subprocess.run')
    def test_get_branch_status_not_git_repo(self, mock_run):
        """Test non-git repository."""
        mock_run.return_value = Mock(returncode=128)
        
        manager = GitManager()
        status = manager.get_branch_status("/path/to/not-repo")
        
        assert status is None
