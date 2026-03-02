"""Unit tests for project management."""

import pytest
from ai_cli.core.projects import ProjectManager
from ai_cli.models import ProjectNode


class TestProjectManager:
    """Test ProjectManager class."""
    
    def test_add_child(self, sample_folder):
        """Test adding child node."""
        new_child = ProjectNode(type="project", name="NewProject", path="/test/new")
        ProjectManager.add_child(sample_folder, new_child)
        
        assert len(sample_folder.children) == 3
        assert sample_folder.children[-1].name == "NewProject"
    
    def test_remove_child(self, sample_folder):
        """Test removing child node."""
        initial_count = len(sample_folder.children)
        ProjectManager.remove_child(sample_folder, "Child1")
        
        assert len(sample_folder.children) == initial_count - 1
        assert not any(c.name == "Child1" for c in sample_folder.children)
    
    def test_find_node(self, sample_folder):
        """Test finding node by name."""
        result = ProjectManager.find_node(sample_folder, "Child1")
        
        assert result is not None
        assert result.name == "Child1"
    
    def test_find_node_not_found(self, sample_folder):
        """Test finding non-existent node."""
        result = ProjectManager.find_node(sample_folder, "NonExistent")
        
        assert result is None
    
    def test_flatten(self, sample_folder):
        """Test flattening tree structure."""
        flat = ProjectManager.flatten(sample_folder)
        
        assert len(flat) >= 2
        assert any(p.name == "Child1" for p in flat)
    
    def test_get_all_projects(self, sample_folder):
        """Test getting all project nodes."""
        projects = ProjectManager.get_all_projects(sample_folder)
        
        assert len(projects) == 2
        assert all(p.type == "project" for p in projects)
    
    def test_count_children_recursive(self, sample_folder):
        """Test recursive child counting."""
        count = ProjectManager.count_children_recursive(sample_folder)
        
        assert count == 2
