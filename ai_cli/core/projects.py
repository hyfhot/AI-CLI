"""Project management module for AI-CLI."""

from typing import List, Optional

from ..models import ProjectNode


class ProjectManager:
    """Manages project tree operations."""
    
    @staticmethod
    def add_child(parent: ProjectNode, child: ProjectNode) -> None:
        """Add a child node to parent.
        
        Args:
            parent: Parent node
            child: Child node to add
        """
        # Check for duplicate names
        if child.name not in [c.name for c in parent.children]:
            parent.children.append(child)
    
    @staticmethod
    def remove_child(parent: ProjectNode, name: str) -> bool:
        """Remove child by name.
        
        Args:
            parent: Parent node
            name: Name of child to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, child in enumerate(parent.children):
            if child.name == name:
                parent.children.pop(i)
                return True
        return False
    
    @staticmethod
    def find_node(root: ProjectNode, path: List[str]) -> Optional[ProjectNode]:
        """Find node by path.
        
        Args:
            root: Root node to search from
            path: List of node names forming the path
            
        Returns:
            Found node or None
        """
        if not path:
            return root
        
        for child in root.children:
            if child.name == path[0]:
                return ProjectManager.find_node(child, path[1:])
        
        return None
    
    @staticmethod
    def flatten(node: ProjectNode, level: int = 0) -> List[tuple]:
        """Flatten tree to list with depth levels.
        
        Args:
            node: Root node
            level: Current depth level
            
        Returns:
            List of (node, level) tuples
        """
        result = [(node, level)]
        for child in node.children:
            result.extend(ProjectManager.flatten(child, level + 1))
        return result
    
    @staticmethod
    def get_all_projects(root: ProjectNode) -> List[ProjectNode]:
        """Get all project nodes (excluding folders).
        
        Args:
            root: Root node
            
        Returns:
            List of project nodes
        """
        projects = []
        
        # Check if current node is a project
        if root.type == "project":
            projects.append(root)
        
        # Recursively get projects from children
        for child in root.children:
            projects.extend(ProjectManager.get_all_projects(child))
        
        return projects
    
    @staticmethod
    def count_children_recursive(node: ProjectNode) -> int:
        """Count all descendant nodes recursively.
        
        Args:
            node: Root node
            
        Returns:
            Total count of descendants
        """
        count = len(node.children)
        for child in node.children:
            count += ProjectManager.count_children_recursive(child)
        return count
