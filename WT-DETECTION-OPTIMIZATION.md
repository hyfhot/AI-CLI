# Windows Terminal 检测优化

> **改进**: 启动时检测一次 wt，只在可用时显示 [T] New Tab  
> **逻辑**: 与 PowerShell 原版一致  
> **状态**: ✅ 已完成

---

## 🎯 改进目标

与 PowerShell 原版保持一致：
- 程序启动时检测一次 `wt` 命令
- 只有检测到 `wt` 时才显示 `[T] New Tab` 菜单项
- 避免显示无法使用的功能

---

## ✅ 实现方案

### 1. 启动时检测（只检测一次）

```python
class Application:
    def __init__(self):
        # ... 其他初始化 ...
        
        # Detect Windows Terminal availability once at startup
        self.wt_available = self._check_wt_available()
    
    def _check_wt_available(self) -> bool:
        """Check if Windows Terminal is available."""
        if sys.platform != 'win32':
            return False
        try:
            result = subprocess.run(["cmd.exe", "/c", "where", "wt"], 
                                  capture_output=True, timeout=2)
            return result.returncode == 0
        except:
            return False
```

### 2. 根据检测结果显示菜单

```python
# 传递 wt_available 到菜单渲染
self.menu.render_tools(tools, self.selected_index, show_new_tab=self.wt_available)

# 菜单渲染
def render_tools(self, tools, selected, show_new_tab=True):
    # ... 渲染工具列表 ...
    
    if show_new_tab:
        print("[↑↓] Select  [Enter] Launch  [T] New Tab  [I] Install  ...")
    else:
        print("[↑↓] Select  [Enter] Launch  [I] Install  ...")  # 没有 [T] New Tab
```

### 3. 忽略 T 键（如果 wt 不可用）

```python
elif event == InputEvent.NEW_TAB:
    if self.wt_available:
        return (tools[self.selected_index], True)
    # Ignore T key if wt not available
```

---

## 📊 功能对比

| 场景 | 有 Windows Terminal | 无 Windows Terminal |
|------|---------------------|---------------------|
| **菜单显示** | `[T] New Tab` 显示 | `[T] New Tab` 隐藏 |
| **按 T 键** | 新标签页打开 | 无反应（忽略） |
| **按 Enter** | 新窗口打开 | 新窗口打开 |

---

## 🔍 与 PowerShell 原版对比

### PowerShell 原版
```powershell
if ($useTab -and (Get-Command "wt" -ErrorAction SilentlyContinue)) {
    Start-Process "wt" -ArgumentList "-w", "0", "new-tab", ...
} else {
    Start-Process -FilePath $wslExe -ArgumentList $wslArgs
}
```

### Python 版本
```python
if new_tab and wt_available:
    subprocess.Popen(["wt", "-w", "0", "new-tab", ...])
else:
    subprocess.Popen(["wsl.exe", ...], creationflags=subprocess.CREATE_NEW_CONSOLE)
```

**一致性**: ✅ 逻辑完全一致

---

## 📋 修改文件

| 文件 | 修改内容 |
|------|----------|
| `ai_cli/app.py` | 添加 `_check_wt_available()` 和 `self.wt_available` |
| `ai_cli/ui/menu.py` | 添加 `show_new_tab` 参数，条件显示菜单项 |
| `ai_cli/platform/windows.py` | 接收 `wt_available` 参数，简化逻辑 |

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

**预期行为**:

#### 无 Windows Terminal
```
=== Select AI Tool ===

> [WSL] kiro-cli

[↑↓] Select  [Enter] Launch  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit
```
- ✅ 没有 `[T] New Tab`
- ✅ 按 T 键无反应

#### 有 Windows Terminal
```
=== Select AI Tool ===

> [WSL] kiro-cli

[↑↓] Select  [Enter] Launch  [T] New Tab  [I] Install  [R] Refresh  [Esc] Back  [Q] Quit
```
- ✅ 显示 `[T] New Tab`
- ✅ 按 T 键在新标签页打开

---

## ✅ 改进完成

- ✅ 启动时检测一次 `wt` 命令
- ✅ 只在可用时显示 `[T] New Tab`
- ✅ T 键在 wt 不可用时被忽略
- ✅ 与 PowerShell 原版逻辑一致
- ✅ 避免显示无法使用的功能

---

**完成时间**: 2026-03-01 12:29  
**版本**: 0.1.5  
**改进**: 用户体验优化
