# ==========================================
# AI-CLI 安装脚本
# ==========================================
# 此脚本用于将 AI-CLI 安装到系统并创建快捷方式
# 支持本地安装和远程安装两种模式
# ==========================================

param(
    [switch]$Uninstall,
    [string]$SourceUrl = "https://raw.githubusercontent.com/hyfhot/AI-CLI/master"
)

$ErrorActionPreference = "Stop"

# 颜色定义
function Write-Step { param($msg) Write-Host "[安装] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[成功] $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "[错误] $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "      $msg" -ForegroundColor Gray }

# 安装目录
$installDir = "$env:LOCALAPPDATA\AI-CLI"
$scriptName = "ai-cli.ps1"
$iconName = "ai-cli.ico"

# 检测是否为远程安装模式（通过检查命令路径或自动模式参数）
$isRemoteInstall = ($null -eq $MyInvocation.MyCommand.Path) -or ($MyInvocation.MyCommand.Path -like "$env:TEMP*") -or ($MyInvocation.MyCommand.Path -eq "")

# 卸载逻辑
if ($Uninstall) {
    Write-Step "开始卸载 AI-CLI..."

    # 删除安装目录
    if (Test-Path $installDir) {
        Remove-Item -Recurse -Force $installDir
        Write-Success "已删除安装目录: $installDir"
    }

    # 删除桌面快捷方式
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"
    if (Test-Path $shortcutPath) {
        Remove-Item -Force $shortcutPath
        Write-Success "已删除桌面快捷方式"
    }

    # 删除开始菜单快捷方式
    $startMenuPath = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs"
    $startShortcutPath = Join-Path $startMenuPath "AI-CLI.lnk"
    if (Test-Path $startShortcutPath) {
        Remove-Item -Force $startShortcutPath
        Write-Success "已删除开始菜单快捷方式"
    }

    Write-Success "卸载完成！"
    exit 0
}

# 检测是否为远程安装模式（临时目录）
$isRemoteInstall = $MyInvocation.MyCommand.Path -like "$env:TEMP*"

if ($isRemoteInstall) {
    Write-Step "正在从 GitHub 下载 AI-CLI..."

    # 创建临时目录下载文件
    $tempDir = Join-Path $env:TEMP "AI-CLI-Install"
    if (Test-Path $tempDir) {
        Remove-Item -Recurse -Force $tempDir
    }
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

    # 下载必要文件
    $filesToDownload = @($scriptName, $iconName, "tools-config.json")
    $langFiles = @("zh-CN.ps1", "en-US.ps1", "ja-JP.ps1", "de-DE.ps1")

    try {
        foreach ($file in $filesToDownload) {
            $url = "$SourceUrl/$file"
            $targetPath = Join-Path $tempDir $file
            Write-Info "下载 $file..."
            Invoke-RestMethod -Uri $url -OutFile $targetPath -UseBasicParsing
        }

        # 下载语言文件目录
        $langDir = Join-Path $tempDir "lang"
        New-Item -ItemType Directory -Path $langDir -Force | Out-Null
        foreach ($langFile in $langFiles) {
            $url = "$SourceUrl/lang/$langFile"
            $targetPath = Join-Path $langDir $langFile
            Invoke-RestMethod -Uri $url -OutFile $targetPath -UseBasicParsing -ErrorAction SilentlyContinue
        }

        Write-Success "文件下载完成"
    }
    catch {
        Write-Error "下载失败: $_"
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
        exit 1
    }

    $projectRoot = $tempDir
}
else {
    # 本地安装模式
    $projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
}

$scriptPath = Join-Path $projectRoot $scriptName
$iconPath = Join-Path $projectRoot $iconName

# 验证源文件存在
if (-not (Test-Path $scriptPath)) {
    Write-Error "未找到 $scriptName"
    exit 1
}

if (-not (Test-Path $iconPath)) {
    Write-Error "未找到 $iconName 图标文件"
    exit 1
}

# 安装逻辑
Write-Step "开始安装 AI-CLI..."
Write-Info "安装目录: $installDir"

# 创建安装目录
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Info "已创建安装目录"
}

# 复制文件
Write-Info "复制文件..."

# 复制主脚本
Copy-Item -Path $scriptPath -Destination $installDir -Force

# 复制图标
$targetIconPath = Join-Path $installDir $iconName
Copy-Item -Path $iconPath -Destination $installDir -Force

# 复制语言文件目录
$langDir = Join-Path $projectRoot "lang"
$targetLangDir = Join-Path $installDir "lang"
if (Test-Path $langDir) {
    if (Test-Path $targetLangDir) {
        Remove-Item -Recurse -Force $targetLangDir
    }
    Copy-Item -Path $langDir -Destination $installDir -Recurse -Force
    Write-Info "已复制语言文件"
}

# 复制配置文件
$configPath = Join-Path $projectRoot "tools-config.json"
$targetConfigPath = Join-Path $installDir "tools-config.json"
if (Test-Path $configPath) {
    Copy-Item -Path $configPath -Destination $installDir -Force
    Write-Info "已复制配置文件"
}

# 清理远程安装的临时文件
if ($isRemoteInstall) {
    Remove-Item -Recurse -Force $projectRoot -ErrorAction SilentlyContinue
}

Write-Success "文件复制完成"

# 创建 PowerShell 启动器
$targetScriptPath = Join-Path $installDir $scriptName
$launcherPath = Join-Path $installDir "AI-CLI.bat"
$launcherContent = "@echo off
powershell.exe -ExecutionPolicy Bypass -File `"%LOCALAPPDATA%\AI-CLI\ai-cli.ps1`" %*
"
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($launcherPath, $launcherContent, $utf8Bom)
Write-Info "已创建启动器"

# 创建桌面快捷方式
Write-Step "创建桌面快捷方式..."

$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$targetScriptPath`""
$shortcut.WorkingDirectory = $installDir
$shortcut.Description = "AI CLI - AI Tools Command Line Interface"
$shortcut.IconLocation = $targetIconPath
$shortcut.Save()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($shell) | Out-Null

Write-Success "已创建桌面快捷方式"

# 创建开始菜单快捷方式
Write-Step "创建开始菜单快捷方式..."

$startMenuPath = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs"
$startShortcutPath = Join-Path $startMenuPath "AI-CLI.lnk"

if (-not (Test-Path $startMenuPath)) {
    New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null
}

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($startShortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$targetScriptPath`""
$shortcut.WorkingDirectory = $installDir
$shortcut.Description = "AI CLI - AI Tools Command Line Interface"
$shortcut.IconLocation = $targetIconPath
$shortcut.Save()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($shell) | Out-Null

Write-Success "已创建开始菜单快捷方式"

# 注册 PATH 环境变量
Write-Step "检查环境变量..."

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    $newPath = "$userPath;$installDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Info "已将安装目录添加到用户 PATH 环境变量"
} else {
    Write-Info "安装目录已在 PATH 中"
}

# 完成
Write-Host ""
Write-Success "=========================================="
Write-Success "  AI-CLI 安装完成！"
Write-Success "=========================================="
Write-Host ""
Write-Info "安装位置: $installDir"
Write-Info "桌面快捷方式: 已创建"
Write-Info "开始菜单: 已创建"
Write-Host ""
Write-Host "您可以通过以下方式启动 AI-CLI:" -ForegroundColor Yellow
Write-Host "  1. 双击桌面上的 'AI-CLI' 快捷方式"
Write-Host "  2. 从开始菜单中选择 'AI-CLI'"
Write-Host "  3. 在命令行中运行 'ai-cli' (需重新打开终端)"
Write-Host ""
Write-Host "卸载命令: ai-cli --uninstall" -ForegroundColor Gray
Write-Host ""
