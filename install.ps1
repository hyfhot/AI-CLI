#!/usr/bin/env pwsh
# AI-CLI Installer v2.0

param([switch]$Uninstall)

$installDir = "$env:LOCALAPPDATA\AI-CLI"
$repoUrl = "https://raw.githubusercontent.com/hyfhot/AI-CLI/master"

function Install-AICLI {
    Write-Host "Installing AI-CLI..." -ForegroundColor Cyan
    
    # 创建安装目录
    if (-not (Test-Path $installDir)) {
        New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    }
    
    # 下载文件
    $files = @("ai-cli.ps1", "config.json")
    foreach ($file in $files) {
        $url = "$repoUrl/$file"
        $dest = Join-Path $installDir $file
        try {
            Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
            Write-Host "  Downloaded: $file" -ForegroundColor Green
        } catch {
            Write-Host "  Failed to download: $file" -ForegroundColor Red
        }
    }
    
    # 创建启动脚本
    $launcherPath = Join-Path $installDir "ai-cli.ps1"
    @"
#!/usr/bin/env pwsh
& "$installDir\ai-cli.ps1" `$args
"@ | Set-Content $launcherPath -Encoding UTF8
    
    # 添加到 PATH
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$installDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
        Write-Host "  Added to PATH" -ForegroundColor Green
    }
    
    # 创建桌面快捷方式
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "pwsh.exe"
    $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$launcherPath`""
    $shortcut.WorkingDirectory = $installDir
    $shortcut.Save()
    
    Write-Host "`nInstallation complete!" -ForegroundColor Green
    Write-Host "  Run 'ai-cli -Init' to initialize config" -ForegroundColor Yellow
    Write-Host "  Run 'ai-cli -Config' to edit config" -ForegroundColor Yellow
    Write-Host "  Run 'ai-cli' to start" -ForegroundColor Yellow
}

function Uninstall-AICLI {
    Write-Host "Uninstalling AI-CLI..." -ForegroundColor Yellow
    
    if (Test-Path $installDir) {
        Remove-Item -Recurse -Force $installDir
        Write-Host "  Removed installation directory" -ForegroundColor Green
    }
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"
    if (Test-Path $shortcutPath) {
        Remove-Item -Force $shortcutPath
        Write-Host "  Removed desktop shortcut" -ForegroundColor Green
    }
    
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -like "*$installDir*") {
        $newPath = ($userPath -split ';' | Where-Object { $_ -ne $installDir }) -join ';'
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "  Removed from PATH" -ForegroundColor Green
    }
    
    Write-Host "`nUninstallation complete!" -ForegroundColor Green
}

if ($Uninstall) {
    Uninstall-AICLI
} else {
    Install-AICLI
}
