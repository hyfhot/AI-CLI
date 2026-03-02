# WSL 工具启动失败修复

> **问题**: `bash: line 1: kiro-cli: command not found`  
> **原因**: 使用 `bash -c` 而不是 `bash -ic`  
> **修复**: 添加 `-i` 参数加载环境  
> **状态**: ✅ 已修复

---

## 🐛 问题

```
bash: line 1: kiro-cli: command not found
```

启动 WSL 工具时找不到命令。

---

## 🔍 原因分析

### bash -c vs bash -ic

**bash -c** (非交互式):
```bash
wsl.exe -e bash -c "kiro-cli"
# ❌ 不加载 .bashrc
# ❌ 不加载 PATH 环境变量
# ❌ 找不到通过 npm/pip 安装的工具
```

**bash -ic** (交互式):
```bash
wsl.exe -e bash -ic "kiro-cli"
# ✅ 加载 .bashrc
# ✅ 加载 PATH 环境变量
# ✅ 可以找到所有已安装的工具
```

### 为什么检测时能找到？

检测时使用了 `-ic`:
```python
# 工具检测 (正确)
wsl.exe -e bash -ic "command -v kiro-cli"  # ✅ 能找到
```

启动时使用了 `-c`:
```python
# 工具启动 (错误)
wsl.exe -e bash -c "kiro-cli"  # ❌ 找不到
```

---

## ✅ 修复

**文件**: `ai_cli/platform/windows.py`

**修复前**:
```python
if tool.environment == ToolEnvironment.WSL:
    cmd = ["wsl.exe", "-e", "bash", "-c", command]  # ❌ -c
    subprocess.Popen(cmd)
```

**修复后**:
```python
if tool.environment == ToolEnvironment.WSL:
    # Use -ic to load .bashrc and environment
    cmd = ["wsl.exe", "-e", "bash", "-ic", command]  # ✅ -ic
    subprocess.Popen(cmd)
```

---

## 🧪 验证

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
ai-cli
```

**测试步骤**:
1. 选择项目
2. 选择 WSL 工具 (如 kiro-cli)
3. 应该正常启动，不再报错

---

## 📝 技术说明

### bash 参数

| 参数 | 说明 | 加载 .bashrc | 用途 |
|------|------|--------------|------|
| `-c` | 非交互式 | ❌ | 执行简单命令 |
| `-ic` | 交互式 | ✅ | 执行需要环境的命令 |

### 为什么需要 -i？

大多数工具通过包管理器安装:
```bash
# npm 全局安装
npm install -g kiro-cli
# 安装到 ~/.npm-global/bin/

# pip 用户安装
pip install --user kiro-cli
# 安装到 ~/.local/bin/

# 这些路径在 .bashrc 中添加到 PATH
export PATH="$HOME/.npm-global/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
```

**不加载 .bashrc** → PATH 不包含这些目录 → 找不到命令

---

## 🎯 总结

**问题**: WSL 工具启动失败  
**原因**: 使用 `bash -c` 不加载环境  
**修复**: 改用 `bash -ic` 加载环境  
**影响**: 所有 WSL 工具  

---

**修复时间**: 2026-03-01 11:57  
**版本**: 0.1.5
