# 依赖冲突快速修复

## 问题

```
ERROR: kimi-cli 1.14.0 requires rich==14.2.0, but you have rich 14.3.3 which is incompatible.
```

## 重要说明

**`ai-cli` 不会安装 AI 工具**:
- ✅ `ai-cli` 只安装自己的依赖（rich, prompt-toolkit 等）
- ✅ 所有 AI 工具（kiro-cli, kimi-cli 等）由用户自行安装
- ✅ 用户可通过程序内按 `I` 键安装工具

**这个警告的原因**:
- 用户系统中已有 `kimi-cli`（用户自己安装的）
- `kimi-cli` 要求 `rich==14.2.0`
- 安装 `ai-cli` 时安装了 `rich 14.3.3`
- 导致版本冲突警告

## ✅ 解决方案

### 方案 1: 忽略警告（推荐）

**这只是警告，不是错误**。程序能正常运行：

```bash
pip install -e ".[dev]"
# 看到警告但继续
ai-cli  # 正常工作
```

### 方案 2: 使用虚拟环境（开发推荐）

```bash
# Windows
cd C:\Projects\AIStudio\ai-cli-multi-platform
python -m venv venv
.\venv\Scripts\activate
pip install -e ".[dev]"

# Linux/WSL
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 方案 3: 强制重新安装

```bash
pip install -e ".[dev]" --force-reinstall --no-cache-dir
```

pip 会自动降级到 `rich==14.2.0`。

## 验证

```bash
ai-cli --version
ai-cli
```

应该正常工作！

---

详细文档: [docs/DEPENDENCY-CONFLICT-v2.md](docs/DEPENDENCY-CONFLICT-v2.md)

