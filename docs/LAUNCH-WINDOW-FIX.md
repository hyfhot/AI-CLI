# 工具启动窗口问题修复

> **问题**: Enter 在当前窗口启动，Ctrl+Enter 未实现  
> **修复**: Enter 新窗口，T 键新标签页  
> **状态**: ✅ 已修复

---

## 🐛 问题

### 1. Enter 键在当前窗口启动
```
[Enter] Launch - 在当前窗口开启 wsl 进程
```
- ❌ 工具在当前终端运行
- ❌ 无法继续使用 ai-cli
- ❌ 需要手动打开新窗口

### 2. Ctrl+Enter 未实现
```
[Ctrl+Enter] New Tab - 功能未实现
```
- ❌ 原生终端 API 不支持 Ctrl+Enter
- ❌ 按键无响应

---

## ✅ 修复方案

### 1. Enter 键 → 新窗口启动

**修复前**:
```python
# WSL 工具在当前窗口启动
cmd = ["wsl.exe", "-e", "bash", "-ic", command]
subprocess.Popen(cmd)  # ❌ 当前窗口
```

**修复后**:
```python
# WSL 工具在新窗口启动
cmd = ["wt.exe", "new-window", "--title", title, "wsl.exe", "-e", "bash", "-ic", command]
subprocess.Popen(cmd)  # ✅ 新窗口
```

### 2. T 键 → 新标签页启动

**添加 T 键支持**:
```python
# 输入事件
class InputEvent(Enum):
    NEW_TAB = "new_tab"  # T 键

# 输入处理
elif ch.lower() == 't':
    return InputEvent.NEW_TAB

# 事件处理
elif event == InputEvent.NEW_TAB:
    return (tools[self.selected_index], True)  # new_tab=True
```

**启动逻辑**:
```python
if new_tab:
    # Windows Terminal 新标签页
    cmd = ["wt.exe", "-w", "0", "new-tab", "--title", title, "wsl.exe", "-e", "bash", "-ic", command]
else:
    # 新窗口
    cmd = ["wt.exe", "new-window", "--title", title, "wsl.exe", "-e", "bash", "-ic", command]
```

---

## 📊 功能对比

| 按键 | 修复前 | 修复后 |
|------|--------|--------|
| **Enter** | 当前窗口 | ✅ 新窗口 |
| **T** | 无功能 | ✅ 新标签页 |
| **Ctrl+Enter** | 未实现 | ❌ 不支持 (用 T 替代) |

---

## 🎯 使用说明

### Enter 键 - 新窗口启动

```
=== Select AI Tool ===

> [WSL] kiro-cli

[↑↓] Select  [Enter] Launch  [T] New Tab  ...
```

**按 Enter**:
- ✅ 在新窗口启动工具
- ✅ 当前窗口继续使用 ai-cli
- ✅ 可以启动多个工具

### T 键 - 新标签页启动

**按 T**:
- ✅ 在当前 Windows Terminal 新标签页启动
- ✅ 所有工具在同一窗口管理
- ✅ 方便切换

---

## 🔍 技术细节

### Windows Terminal 命令

#### 新窗口
```bash
wt.exe new-window --title "kiro-cli - MyProject" wsl.exe -e bash -ic "cd /path && kiro-cli"
```

#### 新标签页
```bash
wt.exe -w 0 new-tab --title "kiro-cli - MyProject" wsl.exe -e bash -ic "cd /path && kiro-cli"
```

**参数说明**:
- `new-window` - 创建新窗口
- `new-tab` - 创建新标签页
- `-w 0` - 在当前窗口 (ID=0)
- `--title` - 设置标签标题

### 为什么不支持 Ctrl+Enter？

原生终端 API (`msvcrt.getch()`, `termios`) 无法捕获 Ctrl+Enter:
- Ctrl+Enter 在大多数终端中被映射为 Enter
- 无法区分 Enter 和 Ctrl+Enter
- 需要使用其他按键 (T 键)

---

## 📋 修改文件

| 文件 | 修改内容 |
|------|----------|
| `ai_cli/platform/windows.py` | WSL 工具新窗口/标签页启动 |
| `ai_cli/ui/input.py` | 添加 T 键支持 |
| `ai_cli/ui/menu.py` | 更新菜单提示 |
| `ai_cli/app.py` | 支持 new_tab 参数 |

---

## 🚀 立即使用

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
ai-cli
```

**测试**:
1. 选择项目和工具
2. 按 **Enter** - 应该在新窗口启动 ✅
3. 再次选择工具
4. 按 **T** - 应该在新标签页启动 ✅

---

## ✅ 问题已修复

- ✅ Enter 键在新窗口启动
- ✅ T 键在新标签页启动
- ✅ 可以同时运行多个工具
- ✅ 动态标签标题显示

---

**修复时间**: 2026-03-01 12:02  
**版本**: 0.1.5
