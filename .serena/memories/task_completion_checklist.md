# Task Completion Checklist

When completing a task, ensure:

## 1. Code Quality
- [ ] Code is formatted with `black ai_cli tests`
- [ ] No linting errors: `ruff check ai_cli tests`
- [ ] Type checking passes: `mypy ai_cli` (if applicable)

## 2. Testing
- [ ] All tests pass: `pytest`
- [ ] New code has test coverage
- [ ] Coverage report reviewed: `pytest --cov=ai_cli`

## 3. Documentation
- [ ] Update README.md if adding features
- [ ] Update CHANGELOG.md with changes
- [ ] Add docstrings to new functions/classes

## 4. Git Commit
- [ ] Follow commit convention (see .github/GIT_COMMIT_CONVENTION.md)
- [ ] Commit message format: `type: description`
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation
  - `style:` formatting
  - `refactor:` code refactoring
  - `test:` tests
  - `chore:` build/tools

## 5. Before Release
- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Build package: `python -m build`
- [ ] Test installation locally
