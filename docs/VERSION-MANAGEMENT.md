# Version Management Guide

## Version Number Locations

AI-CLI maintains version numbers in the following locations:

1. **`pyproject.toml`** - Package metadata version (used by PyPI)
   ```toml
   [project]
   version = "3.0.4"
   ```

2. **`ai_cli/__init__.py`** - Python package version (source of truth)
   ```python
   __version__ = "3.0.4"
   ```

3. **`ai_cli/cli.py`** - Imports from `__init__.py`
   ```python
   from . import __version__
   ```

## Version Synchronization

### Automatic (Recommended)

Use the publish scripts which automatically update all version numbers:

**Linux/macOS:**
```bash
./publish.sh
```

**Windows:**
```powershell
.\publish.ps1
```

The scripts will:
1. Show current version
2. Suggest next version (auto-increment patch)
3. Prompt for new version
4. Update `pyproject.toml`
5. Update `ai_cli/__init__.py`
6. Build and publish to PyPI

### Manual

If you need to update versions manually:

1. **Update `ai_cli/__init__.py`:**
   ```python
   __version__ = "X.Y.Z"
   ```

2. **Update `pyproject.toml`:**
   ```toml
   version = "X.Y.Z"
   ```

3. **Verify synchronization:**
   ```bash
   python3 test_version_sync.py
   ```

## Version Verification

### Check Current Version

```bash
# From command line
ai-cli --version

# From Python
python3 -c "from ai_cli import __version__; print(__version__)"

# From package metadata
pip show ai-cli-launcher | grep Version
```

### Test Version Sync

```bash
# Run the version sync test
python3 test_version_sync.py
```

This will check:
- `pyproject.toml` version
- `ai_cli/__init__.py` version
- Runtime import consistency

## Version Numbering Scheme

AI-CLI follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Examples

- `3.0.0` → `3.0.1`: Bug fix
- `3.0.1` → `3.1.0`: New feature
- `3.1.0` → `4.0.0`: Breaking change

## Publishing Workflow

1. **Make changes** to code
2. **Update CHANGELOG.md** with changes
3. **Run publish script:**
   ```bash
   ./publish.sh  # or publish.ps1 on Windows
   ```
4. **Enter new version** when prompted
5. **Select target:**
   - TestPyPI (for testing)
   - PyPI (production)
   - Both (test first, then production)
6. **Verify installation:**
   ```bash
   pip install --upgrade ai-cli-launcher
   ai-cli --version
   ```

## Troubleshooting

### Version Mismatch

If versions don't match:

```bash
# Check all versions
python3 test_version_sync.py

# Fix manually
# 1. Edit ai_cli/__init__.py
# 2. Edit pyproject.toml
# 3. Verify again
```

### PyPI Version Doesn't Match CLI

This happens if:
1. Package was built with old version
2. Old package is still installed

**Solution:**
```bash
# Rebuild and reinstall
pip uninstall ai-cli-launcher
./publish.sh
pip install ai-cli-launcher
ai-cli --version
```

### Can't Update Version

If publish script fails to update versions:

1. Check file permissions
2. Check file encoding (should be UTF-8)
3. Update manually (see Manual section above)

## Best Practices

1. **Always use publish scripts** for releases
2. **Test on TestPyPI first** before production
3. **Update CHANGELOG.md** before publishing
4. **Verify version sync** before publishing
5. **Test installation** after publishing
6. **Tag releases** in Git:
   ```bash
   git tag -a v3.0.4 -m "Release version 3.0.4"
   git push origin v3.0.4
   ```

## Common Issues

### Issue: `ai-cli --version` shows old version

**Cause:** Old package still installed

**Solution:**
```bash
pip install --upgrade --force-reinstall ai-cli-launcher
```

### Issue: PyPI shows different version than local

**Cause:** Local changes not published

**Solution:**
```bash
./publish.sh  # Publish new version
```

### Issue: Version in code doesn't match pyproject.toml

**Cause:** Manual edit without sync

**Solution:**
```bash
python3 test_version_sync.py  # Check
# Fix manually or run publish script
```
