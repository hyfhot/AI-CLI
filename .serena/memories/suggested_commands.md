# Suggested Commands

## Development
```bash
# Install in development mode
pip install -e ".[dev]"

# Run the application
ai-cli
ai-cli --init          # Initialize config
ai-cli --lang zh       # Start with Chinese
```

## Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_cli

# Run specific test file
pytest tests/test_models.py

# Generate HTML coverage report
pytest --cov=ai_cli --cov-report=html
```

## Code Quality
```bash
# Format code
black ai_cli tests

# Lint code
ruff check ai_cli tests

# Type checking
mypy ai_cli
```

## Build & Package
```bash
# Build distribution packages
python -m build

# Install build tools
pip install build twine

# Upload to PyPI (test)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Git Commands (Linux/WSL)
```bash
git status
git add .
git commit -m "message"
git push
```
