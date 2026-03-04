# Code Style & Conventions

## Python Style
- **PEP 8** compliance
- **Line length**: 100 characters
- **Target version**: Python 3.8+
- **Formatter**: black
- **Linter**: ruff

## Naming Conventions
- **Classes**: PascalCase (e.g., `ProjectNode`, `ToolConfig`)
- **Functions/Methods**: snake_case (e.g., `detect_tools`, `launch_tool`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_CONFIG`)
- **Private members**: prefix with underscore (e.g., `_internal_method`)

## Type Hints
- Use type hints for function parameters and return values
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]` for collections

## Docstrings
- Use docstrings for public classes and functions
- Follow Google or NumPy style

## Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Use absolute imports

## Testing
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use pytest fixtures for common setup
