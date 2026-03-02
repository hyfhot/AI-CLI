# 依赖冲突说明

## 问题

```
ERROR: kimi-cli 1.14.0 requires rich==14.2.0, but you have rich 14.3.3 which is incompatible.
```

## 原因

- 用户系统中**已安装** `kimi-cli 1.14.0`（用户自己安装的）
- `kimi-cli` 严格要求 `rich==14.2.0`
- 安装 `ai-cli` 时，pip 安装了 `rich 14.3.3`
- 导致版本冲突警告

## 重要说明

**`ai-cli` 的职责**:
- ✅ `ai-cli` 是一个**启动器/管理器**
- ✅ **不会**自动安装任何 AI CLI 工具
- ✅ 只安装自己运行所需的依赖（rich, prompt-toolkit, click 等）

**AI 工具的安装**:
- ✅ 所有 AI 工具（kiro-cli, kimi-cli, cursor-agent 等）由**用户自行安装**
- ✅ 用户可通过程序内的安装功能（按 `I` 键）按需安装
- ✅ 程序会执行配置文件中的安装命令

## 解决方案

### 方案 1: 忽略警告（推荐）

**这只是警告，不是错误**。如果 `ai-cli` 能正常运行，可以安全忽略：

```bash
pip install -e ".[dev]"
# 看到警告但继续
ai-cli  # 正常运行
```

`rich 14.3.3` 向下兼容 `14.2.0`，不会影响 `kimi-cli` 的功能。

### 方案 2: 使用虚拟环境（开发推荐）

为 `ai-cli` 开发创建独立环境，不影响全局已安装的工具：

**Windows PowerShell**:
```powershell
cd C:\Projects\AIStudio\ai-cli-multi-platform
python -m venv venv
.\venv\Scripts\activate
pip install -e ".[dev]"
```

**Linux/WSL**:
```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 方案 3: 兼容安装（已实现）

`pyproject.toml` 已放宽版本约束：

```toml
dependencies = [
    "rich>=13.7.0,<15.0.0",  # 兼容范围
]
```

重新安装时，pip 会自动降级到 `rich==14.2.0`：

```bash
pip install -e ".[dev]" --force-reinstall
```

## 验证

```bash
# 检查 ai-cli 是否正常
ai-cli --version
ai-cli

# 检查 kimi-cli 是否正常
kimi-cli --version

# 检查 rich 版本
python -c "import rich; print(rich.__version__)"
```

如果所有命令都正常工作，说明没有实际问题。

## 最佳实践

### 对于用户（使用 ai-cli）

**不需要任何操作**，直接使用：

```bash
pip install ai-cli
ai-cli
```

如果看到依赖警告，可以安全忽略。

### 对于开发者（开发 ai-cli）

**使用虚拟环境**：

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

pip install -e ".[dev]"
```

### 对于 AI 工具安装

**通过 ai-cli 程序内安装**：

1. 运行 `ai-cli`
2. 在工具选择界面按 `I` 键
3. 选择要安装的工具
4. 程序会执行配置文件中的安装命令

**不要**通过 `ai-cli` 的依赖来安装 AI 工具。

## 总结

✅ **这是正常的依赖警告**，不影响使用  
✅ **ai-cli 不会安装 AI 工具**，由用户自行管理  
✅ **推荐使用虚拟环境**进行开发  
✅ **用户可以安全忽略警告**，程序正常工作  

---

**关键点**: `ai-cli` 是一个**启动器/管理器**，不负责安装 AI CLI 工具。所有工具由用户通过程序内的安装功能或手动安装。
