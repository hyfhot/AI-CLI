# Windows 导入错误修复

> **问题**: `Error: No module named 'termios'`  
> **原因**: termios 在模块顶部导入，Windows 上不存在  
> **修复**: 将导入移到函数内部  
> **状态**: ✅ 已修复

---

## 问题

```
PS C:\Users\hyfho> ai-cli
Error: No module named 'termios'
```

## 原因

```python
# ❌ 错误：在模块顶部导入
import termios  # Windows 上不存在
```

## 修复

```python
# ✅ 正确：在函数内部导入
def _get_input_unix(self):
    import tty
    import termios  # 只在 Unix 上调用
```

## 验证

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
python3 -c "from ai_cli.ui.input import InputHandler; print('OK')"
# ✓ Import OK

ai-cli
# 应该正常运行
```

---

**修复时间**: 2026-03-01 11:38  
**版本**: 0.1.4
