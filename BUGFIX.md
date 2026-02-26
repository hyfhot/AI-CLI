# AI-CLI v2.0 Bug 修复说明

## 🐛 问题描述

**错误信息**:
```
The filename, directory name, or volume label syntax is incorrect.
'kiro-cli' is not recognized as an internal or external command,
operable program or batch file.
```

**根本原因**: 
1. `Show-Menu` 函数有 `return $selected`，导致每次循环都返回值，使变量变成数组
2. WSL 启动命令使用数组参数传递方式，与旧版本不兼容

---

## ✅ 修复方案

### 修复 1: 移除 Show-Menu 的 return 语句

**问题**: `Show-Menu` 函数在循环中返回 `$selected`，导致返回多个值

**修复前**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # 显示菜单项
    }
    return $selected  # ❌ 错误：每次调用都返回
}
```

**修复后**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # 显示菜单项
    }
    # ✅ 不返回值，只负责显示
}
```

### 修复 2: 使用旧版本的启动方式

**问题**: 使用数组方式传递参数导致 WSL 启动失败

**修复前**:
```powershell
Start-Process "wsl.exe" -ArgumentList @("-e", "bash", "-ic", $bashCmd)
```

**修复后** (采用旧版本方式):
```powershell
$wslExe = "C:\Windows\System32\wsl.exe"
$wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
Start-Process -FilePath $wslExe -ArgumentList $wslArgs
```

---

## 📝 最终代码

### WSL 启动
```powershell
if ($env -eq "wsl") {
    $wslPath = ConvertTo-WslPath $projectPath
    $wslExe = "C:\Windows\System32\wsl.exe"
    $wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
    Start-Process -FilePath $wslExe -ArgumentList $wslArgs
}
```

### Windows 启动
```powershell
else {
    $cmdArgs = "/k `"title $title & cd /d `"$projectPath`" & $tool`""
    Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
}
```

---

## ✅ 验证结果

- ✅ WSL 工具正常启动
- ✅ Windows 工具正常启动
- ✅ 路径转换正确
- ✅ 终端保持打开
- ✅ 变量传递正确

---

**修复日期**: 2026-02-26  
**版本**: 2.0.1  
**状态**: ✅ 已修复并测试通过
