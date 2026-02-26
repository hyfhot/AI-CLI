🌐 [English](BUGFIX.md) | [中文](BUGFIX.zh.md) | [日本語](BUGFIX.ja.md)

# AI-CLI v2.0 Bug Fix Documentation

## 🐛 Problem Description

**Error Message**:
```
The filename, directory name, or volume label syntax is incorrect.
'kiro-cli' is not recognized as an internal or external command,
operable program or batch file.
```

**Root Cause**:
1. The `Show-Menu` function had `return $selected`, which caused it to return a value on every loop iteration, turning the variable into an array
2. The WSL startup command used an array parameter passing method, which was incompatible with older versions

---

## ✅ Fix Solutions

### Fix 1: Remove the return statement from Show-Menu

**Problem**: The `Show-Menu` function returned `$selected` inside the loop, causing multiple return values

**Before Fix**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # Display menu items
    }
    return $selected  # ❌ Error: Returns on every call
}
```

**After Fix**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # Display menu items
    }
    # ✅ No return value, only responsible for display
}
```

### Fix 2: Use the Legacy Startup Method

**Problem**: Using array parameter passing caused WSL startup to fail

**Before Fix**:
```powershell
Start-Process "wsl.exe" -ArgumentList @("-e", "bash", "-ic", $bashCmd)
```

**After Fix** (using legacy approach):
```powershell
$wslExe = "C:\Windows\System32\wsl.exe"
$wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
Start-Process -FilePath $wslExe -ArgumentList $wslArgs
```

---

## 📝 Final Code

### WSL Startup
```powershell
if ($env -eq "wsl") {
    $wslPath = ConvertTo-WslPath $projectPath
    $wslExe = "C:\Windows\System32\wsl.exe"
    $wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
    Start-Process -FilePath $wslExe -ArgumentList $wslArgs
}
```

### Windows Startup
```powershell
else {
    $cmdArgs = "/k `"title $title & cd /d `"$projectPath`" & $tool`""
    Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
}
```

---

## ✅ Verification Results

- ✅ WSL tools start normally
- ✅ Windows tools start normally
- ✅ Path conversion is correct
- ✅ Terminal remains open
- ✅ Variable passing is correct

---

**Fix Date**: 2026-02-26
**Version**: 2.0.1
**Status**: ✅ Fixed and tested successfully
