# AI-CLI Project Overview

## Purpose
AI-CLI is a cross-platform terminal launcher for managing multiple AI coding assistants (Kiro CLI, Claude Code, Cursor Agent, etc.). It provides a unified interface to switch between different AI tools seamlessly.

## Tech Stack
- **Language**: Python 3.8+
- **UI Framework**: Rich (terminal UI), prompt-toolkit (keyboard input)
- **CLI Framework**: Click
- **Build System**: setuptools with pyproject.toml
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Code Quality**: black, mypy, ruff

## Key Features
- Cross-platform support (Windows, Linux, macOS)
- WSL integration with automatic path conversion
- Project management with tree structure
- Async tool detection and installation
- Git worktree support
- Multi-language support (en, zh, ja, de)

## Project Structure
```
ai_cli/
├── cli.py          # CLI entry point
├── app.py          # Main application logic
├── models.py       # Data models
├── config.py       # Configuration management
├── utils.py        # Path utilities
├── core/           # Core modules (tools, projects, git, installer)
├── ui/             # UI modules (theme, menu, input)
├── platform/       # Platform adapters (windows, linux, macos)
└── i18n/           # Internationalization
```
