# Git Worktree Support

> 🌐 **English** | [中文](GIT-WORKTREE.zh.md)

## Overview

AI CLI Launcher now supports automatic Git Worktree detection and selection, allowing developers to quickly switch between multiple working trees of the same Git repository for true parallel development.

## Features

### 🔍 Auto Detection
- Automatically detects if project is a Git repository after selection
- Queries all worktrees in the repository
- Transparent when single worktree exists
- Shows selection interface when multiple worktrees detected

### 📋 Smart Selection Interface
```
=== Select Git Worktree (Project: MyProject) ===

Multiple worktrees detected. Select one to work with:

> main (↑2, current) - C:/Projects/MyProject
  feature-a (↓1) - C:/Projects/MyProject-feature
  hotfix - C:/Projects/MyProject-hotfix

[↑↓] Select  [Enter] Confirm  [Esc] Back
```

### ✨ Interface Features
- **Branch name highlighting**: Cyan/Green color, most prominent
- **Status indicators**: Shows ahead/behind commits (↑↓) and current worktree
- **Path display**: Gray color, least prominent
- **Keyboard navigation**: Arrow keys to select, Enter to confirm, Esc to go back

### 🎯 Use Cases

#### Scenario 1: Parallel Feature Development
```bash
# Main repository
git worktree add ../myproject-feature-a feature-a
git worktree add ../myproject-feature-b feature-b

# In AI CLI Launcher, after selecting project
# Auto-detects 3 worktrees, choose which branch to work on
```

#### Scenario 2: Development + Hotfix
```bash
# While developing new feature, urgent bug fix needed
git worktree add ../myproject-hotfix hotfix

# Quickly switch to hotfix worktree for fix
# Return to feature worktree to continue development
```

#### Scenario 3: Code Review
```bash
# Create temporary worktree for PR review
git worktree add ../myproject-review pr-123

# Test and review code in isolated environment
# Main development environment unaffected
```

## Technical Implementation

### Detection Logic
1. Check if `.git` directory exists in project path
2. Verify `git` command availability
3. Execute `git worktree list` to get all worktrees
4. Parse output to extract path, branch, HEAD info

### Path Handling
- Auto-normalize paths for comparison (remove trailing slashes, lowercase)
- Identify worktree corresponding to current project path
- Support both Windows and WSL path formats

### User Interaction
- Uses existing keyboard navigation system
- Real-time display refresh without flicker
- Esc key for quick return to default path

## Requirements

### Required
- Git installed and available in PATH
- Project is a Git repository (contains `.git` directory)

### Optional
- Multiple worktrees configured (feature is transparent with single worktree)

## Usage Examples

### Creating Worktrees
```bash
# Navigate to project directory
cd C:\Projects\MyProject

# Create new worktrees
git worktree add ..\MyProject-feature feature-branch
git worktree add ..\MyProject-hotfix hotfix-branch

# List all worktrees
git worktree list
```

### Using in AI CLI Launcher
1. Launch `ai-cli`
2. Select configured project
3. If multiple worktrees detected, selection interface appears automatically
4. Use ↑↓ keys to select worktree
5. Press Enter to confirm, or Esc to go back to project selection
6. Select AI tool to launch

**Display Format:**
```
> main (↑3, current) - C:/Projects/MyProject
  feature (↓1) - C:/Projects/MyProject-feature
```
- Branch name in cyan/green (most prominent)
- Status: `↑` ahead, `↓` behind, `current` for current directory
- Path in gray (least prominent)

### Cleaning Up Worktrees
```bash
# Remove unneeded worktree
git worktree remove ..\MyProject-feature

# Or manually delete directory then clean up
git worktree prune
```

## FAQ

**Q: Why isn't the worktree selection interface showing?**
A: Possible reasons:
- Project is not a Git repository
- Only one worktree exists (default behavior)
- Git command unavailable

**Q: Path incorrect after selecting worktree?**
A: Ensure worktree path exists and is accessible. Verify with `git worktree list`.

**Q: Can I skip worktree selection?**
A: Yes, press Esc to go back to project selection and choose a different project or action.

**Q: Does it support WSL environment?**
A: Fully supported, paths are automatically converted to WSL format.

**Q: What's the performance impact?**
A: `git worktree list` is very fast (typically <100ms), executed only once when selecting project.

## Related Resources

- [Git Worktree Official Docs](https://git-scm.com/docs/git-worktree)
- [Git Worktree Guide](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging)
- [AI CLI Launcher Main Docs](../README.md)

---

*Last updated: 2026-02-28*
