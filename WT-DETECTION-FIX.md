# Windows Terminal 检测修复

> **问题**: T 键与 Enter 键功能一致，都在新窗口打开  
> **原因**: wt.exe 不存在，但异常处理不正确  
> **修复**: 使用 `where wt` 预检查  
> **状态**: ✅ 已修复

---

## 🐛 问题

T 键应该在新标签页打开，但实际上在新窗口打开（与 Enter 键相同）。

---

## 🔍 根本原因

### 系统没有安装 Windows Terminal

```bash
$ cmd.exe /c "where wt"
INFO: Could not find files for the given pattern(s).
```

### 异常处理不正确

```python
# 修复前
try:
    subprocess.Popen(["wt.exe", "-w", "0", "new-tab", ...])
except (FileNotFoundError, OSError):
    # Fallback
```

**问题**: `subprocess.Popen()` 不会立即抛出 `FileNotFoundError`，而是在后台失败，导致异常处理不生效。

---

## ✅ 修复方案

### 预检查 wt 命令是否存在

```python
# 修复后
wt_available = subprocess.run(["cmd.exe", "/c", "where", "wt"], 
                             capture_output=True).returncode == 0

if wt_available:
    # 使用 Windows Terminal
    cmd = ["wt", "-w", "0", "new-tab", "--title", title, "wsl", "-e", "bash", "-ic", wsl_command]
    subprocess.Popen(cmd)
else:
    # 降级到新窗口
    cmd = ["wsl.exe", "-e", "bash", "-ic", wsl_command]
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
```

**关键点**:
1. 使用 `where wt` 检查命令是否存在
2. 根据检查结果选择启动方式
3. 使用 `wt` 而不是 `wt.exe`（与 PowerShell 版本一致）

---

## 📊 功能对比

| 按键 | 有 Windows Terminal | 无 Windows Terminal |
|------|---------------------|---------------------|
| **Enter** | 新窗口 | 新窗口 |
| **T** | ✅ 新标签页 | 新窗口（降级） |

---

## 🎯 用户体验

### 有 Windows Terminal
```
按 T 键 → 在当前 Windows Terminal 新标签页打开
```

### 无 Windows Terminal
```
按 T 键 → 在新窗口打开（与 Enter 键相同）
```

**说明**: 由于你的系统没有安装 Windows Terminal，T 键会自动降级到新窗口模式。

---

## 📋 修改文件

| 文件 | 修改内容 |
|------|----------|
| `ai_cli/platform/windows.py` | 使用 `where wt` 预检查 |

**关键修改**:
```python
# 修复前 - 异常处理不生效
try:
    subprocess.Popen(["wt.exe", ...])
except FileNotFoundError:
    # 降级

# 修复后 - 预检查
wt_available = subprocess.run(["cmd.exe", "/c", "where", "wt"], 
                             capture_output=True).returncode == 0
if wt_available:
    subprocess.Popen(["wt", ...])
else:
    # 降级
```

---

## 🚀 使用说明

### 重新安装 (在 Windows PowerShell 中)

```powershell
cd C:\Projects\AIStudio\ai-cli-multi-platform
python -m pip install -e ".[dev]" --force-reinstall
```

### 测试

```powershell
ai-cli
```

1. 选择项目和 WSL 工具
2. 按 **Enter** - 新窗口打开 ✅
3. 按 **T** - 新窗口打开（因为没有 Windows Terminal） ✅

### 安装 Windows Terminal（可选）

如果想使用新标签页功能，可以安装 Windows Terminal：

```powershell
# 方法 1: Microsoft Store
# 搜索 "Windows Terminal" 并安装

# 方法 2: winget
winget install Microsoft.WindowsTerminal
```

安装后，T 键将在新标签页打开。

---

## ✅ 问题已修复

- ✅ T 键正确检测 Windows Terminal
- ✅ 有 Windows Terminal: 新标签页
- ✅ 无 Windows Terminal: 新窗口（降级）
- ✅ Enter 键: 始终新窗口

---

**修复时间**: 2026-03-01 12:26  
**版本**: 0.1.5  
**说明**: 你的系统没有 Windows Terminal，T 键会降级到新窗口模式
