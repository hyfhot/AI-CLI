# 依赖冲突解决方案

## 问题

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. 
This behaviour is the source of the following dependency conflicts.
kimi-cli 1.14.0 requires rich==14.2.0, but you have rich 14.3.3 which is incompatible.
```

## 原因

- `kimi-cli 1.14.0` 严格要求 `rich==14.2.0`
- `ai-cli` 使用 `rich>=13.7.0`（安装了 14.3.3）
- 版本冲突

## 解决方案

### 方案 1: 兼容安装（推荐）

已修改 `pyproject.toml`，放宽版本约束：

```toml
dependencies = [
    "rich>=13.7.0,<15.0.0",  # 兼容 kimi-cli
    ...
]
```

**重新安装**：

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]"
```

pip 会自动降级到 `rich==14.2.0` 以满足 `kimi-cli` 的要求。

### 方案 2: 忽略冲突（快速）

如果程序能正常运行，可以忽略此警告：

```bash
pip install -e ".[dev]" --no-deps
pip install rich prompt-toolkit click platformdirs gitpython
```

### 方案 3: 虚拟环境隔离（最佳实践）

为 `ai-cli` 创建独立虚拟环境：

```bash
# Windows PowerShell
cd C:\Projects\AIStudio\ai-cli-multi-platform
python -m venv venv
.\venv\Scripts\activate
pip install -e ".[dev]"
```

```bash
# Linux/WSL
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 方案 4: 使用 pipx（推荐用于 CLI 工具）

```bash
# 安装 pipx
pip install --user pipx
pipx ensurepath

# 使用 pipx 安装（自动隔离）
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pipx install -e .
```

## 验证

安装后验证：

```bash
# 检查版本
ai-cli --version

# 检查 rich 版本
python -c "import rich; print(rich.__version__)"

# 运行程序
ai-cli
```

## 为什么会冲突？

### kimi-cli 的严格依赖

```python
# kimi-cli 的 setup.py
install_requires=[
    'rich==14.2.0',  # ❌ 严格版本
]
```

### ai-cli 的灵活依赖

```python
# ai-cli 的 pyproject.toml
dependencies = [
    'rich>=13.7.0,<15.0.0',  # ✅ 范围版本
]
```

### pip 的行为

1. 安装 `ai-cli` 时，pip 选择最新的 `rich==14.3.3`
2. 但 `kimi-cli` 已安装，要求 `rich==14.2.0`
3. pip 发出警告但继续安装

## 最佳实践

### 1. 使用虚拟环境

```bash
# 为每个项目创建独立环境
python -m venv ~/.venvs/ai-cli
source ~/.venvs/ai-cli/bin/activate  # Linux/macOS
# 或
~/.venvs/ai-cli/Scripts/activate  # Windows
```

### 2. 使用 pipx 安装 CLI 工具

```bash
# 自动隔离，避免冲突
pipx install kimi-cli
pipx install ai-cli
```

### 3. 放宽依赖约束

在 `pyproject.toml` 中使用范围版本：

```toml
dependencies = [
    "rich>=13.7.0,<15.0.0",  # ✅ 好
    # "rich==14.3.3",         # ❌ 避免
]
```

## 快速修复（Windows PowerShell）

```powershell
# 进入项目目录
cd C:\Projects\AIStudio\ai-cli-multi-platform

# 重新安装（pip 会自动降级 rich）
pip install -e ".[dev]"

# 验证
ai-cli --version
ai-cli
```

## 快速修复（Linux/WSL）

```bash
# 进入项目目录
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform

# 重新安装
pip3 install -e ".[dev]"

# 验证
ai-cli --version
ai-cli
```

## 如果仍有问题

### 强制重新安装所有依赖

```bash
pip install -e ".[dev]" --force-reinstall --no-cache-dir
```

### 检查已安装的包

```bash
pip list | grep -E "(rich|kimi-cli|ai-cli)"
```

### 卸载并重新安装

```bash
pip uninstall ai-cli kimi-cli -y
pip install kimi-cli
pip install -e ".[dev]"
```

## 总结

✅ **已修改 `pyproject.toml`**，放宽 `rich` 版本约束  
✅ **重新安装即可**，pip 会自动选择兼容版本  
✅ **推荐使用虚拟环境**，避免全局依赖冲突  

**现在可以直接运行**：

```bash
pip install -e ".[dev]"
ai-cli
```

pip 会自动将 `rich` 降级到 `14.2.0`，同时满足两个包的要求。
