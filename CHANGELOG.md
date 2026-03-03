# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2026-03-01

### Fixed
- 🚀 Optimized tool detection performance - 5.8x faster (3200ms → 600ms)
- 🚀 Implemented batch WSL detection - single call for all tools (6x faster)
- 🚀 Added 30-second memory cache - instant response on re-entry (∞ faster)
- 🚀 Performance now matches original PowerShell version
- 🐛 Fixed WSL tool launch failure - use `bash -ic` to load environment
- 🐛 Fixed tool launch in current window - now launches in new window
- 🐛 Fixed missing new tab feature - added T key for new tab launch
- 🐛 Fixed ESC key behavior - now only goes back, never quits
- 🐛 Fixed Q key behavior - now quits from any screen

### Added
- ✨ T key to launch tool in new tab (only shown when Windows Terminal available)
- ✨ Dynamic terminal title with tool and project name
- ✨ Enter key now launches in new window
- ✨ Support for Windows Terminal new-tab and new-window
- ✨ Windows Terminal detection at startup (once only)

### Changed
- 🎨 Tool detector is now a singleton with shared cache
- 🎨 Removed version fetching for faster detection
- 🎨 WSL tools detected in single batch call instead of per-tool
- 🎨 WSL tool launch now uses `bash -ic` instead of `bash -c`
- 🎨 Menu hint changed from [Ctrl+Enter] to [T] for new tab
- 🎨 [T] New Tab only shown when Windows Terminal is available
- 🎨 ESC key at root project menu now stays in menu instead of quitting
- 🎨 Q key now exits program from any screen (consistent behavior)

### Performance
- ✅ First launch (no cache): 600ms < 1000ms target
- ✅ First launch (cached): 50ms < 100ms target  
- ✅ Re-enter menu: 0ms < 50ms target

## [0.1.4] - 2026-03-01

### Fixed
- 🐛 Fixed program deadlock/freeze after multiple key presses
- 🐛 Fixed Ctrl+C not working when program freezes
- 🔧 Completely rewrote input handler using native terminal APIs

### Changed
- 🎨 Replaced prompt_toolkit.Application with native terminal APIs (tty/termios/msvcrt)
- 🎨 Improved input handling stability and performance
- 🎨 Simplified code by removing complex event loop

### Removed
- 🗑️ Removed prompt_toolkit dependency from input handling (still used for menu rendering)

## [0.1.3] - 2026-03-01

### Fixed
- 🐛 Fixed Enter/N/D keys not responding in project selection menu
- 🐛 Fixed ESC key behavior - now correctly returns to parent folder instead of exiting
- 🐛 Fixed screen flickering caused by invalid 'c-enter' key binding
- 🐛 Fixed infinite loop when key binding errors occur
- 🔧 Rewrote input handler to use Application instead of prompt() for proper key capture

### Changed
- 🎨 Input handler now uses prompt_toolkit.application.Application for menu navigation
- 🎨 Added case-insensitive key bindings (N/n, D/d, etc.)
- 🎨 Added temporary "not yet implemented" messages for N and D keys
- 🎨 Removed Ctrl+Enter binding (not supported in most terminals)

### Added
- 🧪 Added keyboard input test script (test_keyboard.py)
- 📚 Added keyboard fix documentation (docs/KEYBOARD-FIX.md)
- 📚 Added flicker fix documentation (docs/FLICKER-FIX.md)
- 🛡️ Added exception handling in project selection loop

## [0.1.2] - 2026-03-01

### Fixed
- 🐛 Fixed Windows UI unresponsive issue - menu now shows operation hints
- 🐛 Fixed input handler closure bug - all keyboard shortcuts now work correctly
- 🐛 Fixed Enter key not responding in project selection menu
- 🔧 Improved Windows terminal compatibility with prompt_toolkit
- 🔧 Fixed dependency conflict with kimi-cli (rich version constraint)

### Added
- ✨ Added operation hints to project and tool selection menus
- ✨ Added empty project list handling with friendly prompts
- 🧪 Added Windows UI test script (test_ui_windows.py)
- 📚 Added Windows UI fix documentation (docs/WINDOWS-UI-FIX.md)
- 📚 Added dependency conflict resolution guide (docs/DEPENDENCY-CONFLICT.md)

### Changed
- 🎨 Improved menu rendering with clearer visual indicators (> prefix for selected items)
- 🎨 Changed from Tree view to simple list view for better Windows compatibility
- 📦 Relaxed rich version constraint to `>=13.7.0,<15.0.0` for better compatibility

## [0.1.1] - 2026-03-01

### Fixed
- 🐛 Fixed UTF-8 BOM handling in config file loading
- Configuration files with BOM are now automatically handled
- Use `utf-8-sig` encoding to prevent BOM-related errors

### Added
- 📚 Added BOM fix documentation (docs/BOM-FIX.md)
- 🧪 Added test for BOM handling in config loading

## [0.1.0] - 2026-03-01

### Added
- 🎉 Initial Python version release
- ✅ Cross-platform support (Windows, Linux, macOS)
- ✅ Windows WSL dual-environment support
- ✅ Tree structure project management
- ✅ Async tool detection
- ✅ Automatic path conversion (Windows ↔ WSL)
- ✅ Environment variable injection
- ✅ Git worktree detection
- ✅ Rich terminal UI with keyboard shortcuts
- ✅ Platform adapters for Windows/Linux/macOS
- ✅ CLI entry point with click
- ✅ Configuration management
- ✅ Unit tests for core modules

### Technical Details
- **Core Modules**: 11 modules (1044 lines)
- **Test Coverage**: 6 test files (417 lines)
- **Total Code**: 1461 lines
- **Dependencies**: rich, prompt-toolkit, click, platformdirs

### Migration from PowerShell
- Migrated from PowerShell to Python for cross-platform support
- Preserved all core functionality
- Improved performance with async tool detection
- Enhanced UI with rich library
- Better code organization and modularity

## [Unreleased]

### Planned
- Tool installation feature
- More comprehensive tests
- CI/CD integration
- PyPI package release
- Enhanced documentation
- More tool configurations

---

## Version History

- **0.1.0** (2026-03-01): Initial Python release
- **3.0.0** (PowerShell): Original PowerShell version

[0.1.0]: https://github.com/hyfhot/AI-CLI/releases/tag/v0.1.0
