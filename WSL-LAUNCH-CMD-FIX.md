# WSL 启动命令修复

> **问题**: WSL 工具不启动  
> **原因**: `wsl.exe -e bash -ic` 参数错误  
> **修复**: 使用 `wsl.exe bash -ic`  
> **状态**: ✅ 已修复

---

## 问题

WSL 工具既不在当前进程启动，也不在新窗口启动。

---

## 原因

**错误的命令格式**:
```bash
# ❌ 错误
wt.exe new-window wsl.exe -e bash -ic "cd /path && kiro-cli"
# -e 参数与 bash -ic 冲突
```

**正确的命令格式**:
```bash
# ✅ 正确
wt.exe new-window wsl.exe bash -ic "cd /path && kiro-cli"
# 移除 -e 参数
```

---

## 修复

**文件**: `ai_cli/platform/windows.py`

```python
# 修复前
cmd = ["wt.exe", "new-window", "--title", title, "wsl.exe", "-e", "bash", "-ic", command]

# 修复后
cmd = ["wt.exe", "new-window", "--title", title, "wsl.exe", "bash", "-ic", wsl_command]
```

---

## 验证

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
ai-cli
```

**测试**:
1. 选择项目和 WSL 工具
2. 按 Enter - 应该在新窗口启动 ✅
3. 按 T - 应该在新标签页启动 ✅

---

**修复时间**: 2026-03-01 12:05  
**版本**: 0.1.5
