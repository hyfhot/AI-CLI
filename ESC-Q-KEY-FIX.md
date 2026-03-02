# ESC/Q 键交互逻辑修复

> **改进**: ESC 只返回，Q 键直接退出  
> **逻辑**: 与 PowerShell 原版一致  
> **状态**: ✅ 已完成

---

## 🎯 交互逻辑

### ESC 键 - 只返回，不退出

| 界面 | ESC 行为 |
|------|----------|
| **项目选择（根目录）** | 无操作（停留在菜单） |
| **项目选择（子目录）** | 返回上级目录 |
| **工具选择** | 返回项目选择 |

**关键**: ESC 绝对不会退出程序

### Q 键 - 直接退出

| 界面 | Q 行为 |
|------|--------|
| **任何界面** | 立即退出程序 |

**关键**: Q 键在任何界面都直接退出

---

## ✅ 实现方案

### 1. 项目选择界面

```python
elif event == InputEvent.ESCAPE:
    # ESC only goes back, never quits
    if self.current_path:
        self.current_path.pop()  # 返回上级目录
        self.selected_index = 0
    # If at root, do nothing (stay in menu)

elif event == InputEvent.QUIT:
    # Q always quits
    return None
```

### 2. 工具选择界面

```python
elif event == InputEvent.ESCAPE:
    # ESC returns to project selection
    return None

elif event == InputEvent.QUIT:
    # Q quits the program - raise exception to exit main loop
    raise KeyboardInterrupt
```

**关键**: 工具选择界面的 Q 键抛出 `KeyboardInterrupt` 异常，直接退出主循环。

---

## 📊 行为对比

### 修复前

| 按键 | 项目选择（根目录） | 项目选择（子目录） | 工具选择 |
|------|-------------------|-------------------|----------|
| **ESC** | ❌ 退出程序 | ✅ 返回上级 | ✅ 返回项目选择 |
| **Q** | ✅ 退出程序 | ✅ 退出程序 | ❌ 返回项目选择 |

### 修复后

| 按键 | 项目选择（根目录） | 项目选择（子目录） | 工具选择 |
|------|-------------------|-------------------|----------|
| **ESC** | ✅ 无操作 | ✅ 返回上级 | ✅ 返回项目选择 |
| **Q** | ✅ 退出程序 | ✅ 退出程序 | ✅ 退出程序 |

---

## 🎯 用户体验

### ESC 键 - 安全返回

```
项目选择（根目录）
  按 ESC → 无操作（停留在菜单）
  
项目选择（子目录）
  按 ESC → 返回上级目录
  
工具选择
  按 ESC → 返回项目选择
```

**优点**: 不会误操作退出程序

### Q 键 - 快速退出

```
任何界面
  按 Q → 立即退出程序
```

**优点**: 随时可以快速退出

---

## 📋 修改文件

| 文件 | 修改内容 |
|------|----------|
| `ai_cli/app.py` | 修改 ESC/Q 键逻辑 |

**关键修改**:

```python
# 项目选择 - ESC 在根目录不退出
elif event == InputEvent.ESCAPE:
    if self.current_path:
        self.current_path.pop()
    # 如果在根目录，不做任何操作

# 工具选择 - Q 键抛出异常退出
elif event == InputEvent.QUIT:
    raise KeyboardInterrupt
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

**测试场景**:

1. **项目选择（根目录）**
   - 按 ESC → 停留在菜单 ✅
   - 按 Q → 退出程序 ✅

2. **项目选择（子目录）**
   - 按 ESC → 返回上级 ✅
   - 按 Q → 退出程序 ✅

3. **工具选择**
   - 按 ESC → 返回项目选择 ✅
   - 按 Q → 退出程序 ✅

---

## ✅ 改进完成

- ✅ ESC 键只返回，不退出
- ✅ Q 键在任何界面都退出
- ✅ 与 PowerShell 原版逻辑一致
- ✅ 避免误操作退出程序

---

**完成时间**: 2026-03-01 12:33  
**版本**: 0.1.5  
**改进**: 交互逻辑优化
