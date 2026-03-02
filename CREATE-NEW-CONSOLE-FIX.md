# CREATE_NEW_CONSOLE 修复

> **问题**: WSL 工具在当前会话启动，T 键无反应  
> **原因**: 缺少 CREATE_NEW_CONSOLE 标志，wt.exe 异常未处理  
> **修复**: 添加标志和异常处理  
> **状态**: ✅ 已修复

---

## 🐛 问题

### 1. Enter 键在当前会话启动
```python
subprocess.Popen(["wsl.exe", "-e", "bash", "-ic", command])
# ❌ 在当前终端运行，没有新窗口
```

### 2. T 键无反应
```python
subprocess.Popen(["wt.exe", "-w", "0", "new-tab", ...])
# ❌ wt.exe 不存在时抛出异常
# ❌ 异常未捕获，导致程序返回项目选择界面
```

---

## 🔍 根本原因

### 问题 1: 缺少 CREATE_NEW_CONSOLE 标志

在 Windows 上，`subprocess.Popen()` 默认继承父进程的控制台。需要使用 `CREATE_NEW_CONSOLE` 标志创建新窗口。

**Windows API 文档**:
```
CREATE_NEW_CONSOLE (0x00000010)
The new process has a new console, instead of inheriting its parent's console.
```

### 问题 2: wt.exe 异常未处理

`wt.exe` 可能不存在（Windows Terminal 未安装），导致 `FileNotFoundError`，异常未捕获导致函数提前返回。

---

## ✅ 修复方案

### 1. Enter 键 - 添加 CREATE_NEW_CONSOLE

```python
# 修复前
cmd = ["wsl.exe", "-e", "bash", "-ic", wsl_command]
subprocess.Popen(cmd)  # ❌ 当前会话

# 修复后
cmd = ["wsl.exe", "-e", "bash", "-ic", wsl_command]
subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)  # ✅ 新窗口
```

### 2. T 键 - 添加异常处理

```python
# 修复前
cmd = ["wt.exe", "-w", "0", "new-tab", ...]
subprocess.Popen(cmd)  # ❌ 异常未处理

# 修复后
try:
    cmd = ["wt.exe", "-w", "0", "new-tab", ...]
    subprocess.Popen(cmd)  # ✅ 尝试 Windows Terminal
except (FileNotFoundError, OSError):
    print("Windows Terminal not available, opening in new window")
    cmd = ["wsl.exe", "-e", "bash", "-ic", wsl_command]
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)  # ✅ 降级到新窗口
```

---

## 📊 修复对比

| 按键 | 修复前 | 修复后 |
|------|--------|--------|
| **Enter** | 当前会话 | ✅ 新窗口 (CREATE_NEW_CONSOLE) |
| **T** | 无反应/异常 | ✅ 新标签页 (有 wt.exe) 或新窗口 (无 wt.exe) |

---

## 🧪 测试

### 测试脚本

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
python test_console_launch.py
```

### 预期结果

**Test 1 (Enter 键)**:
- ✅ 新的控制台窗口打开
- ✅ WSL 环境启动
- ✅ kiro-cli 运行

**Test 2 (T 键)**:
- ✅ 如果有 Windows Terminal: 新标签页打开
- ✅ 如果没有 Windows Terminal: 降级到新窗口

---

## 📋 修改文件

| 文件 | 修改内容 |
|------|----------|
| `ai_cli/platform/windows.py` | 添加 CREATE_NEW_CONSOLE 和异常处理 |

**关键修改**:
```python
# 所有 wsl.exe 调用
subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

# 所有 wt.exe 调用
try:
    subprocess.Popen(cmd)
except (FileNotFoundError, OSError):
    # Fallback to new window
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
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

1. 选择项目
2. 选择 WSL 工具
3. 按 **Enter** - 应该打开新控制台窗口 ✅
4. 按 **T** - 应该打开新标签页（或新窗口） ✅

---

## ✅ 问题已修复

- ✅ Enter 键在新窗口启动 (CREATE_NEW_CONSOLE)
- ✅ T 键在新标签页启动 (有异常处理)
- ✅ wt.exe 不存在时自动降级到新窗口
- ✅ 不会返回项目选择界面

---

**修复时间**: 2026-03-01 12:22  
**版本**: 0.1.5  
**关键**: CREATE_NEW_CONSOLE 标志
