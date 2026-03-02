#!/usr/bin/env pwsh
# AI-CLI Installer for Windows

$ErrorActionPreference = "Stop"

Write-Host "`nAI-CLI Installer" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor DarkGray

# Check Python
Write-Host "`nChecking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Install via pip
Write-Host "`nInstalling AI-CLI..." -ForegroundColor Yellow
try {
    pip install -e ".[dev]"
    Write-Host "  Installation complete!" -ForegroundColor Green
} catch {
    Write-Host "  Installation failed!" -ForegroundColor Red
    exit 1
}

# Initialize config
Write-Host "`nInitializing configuration..." -ForegroundColor Yellow
ai-cli --init

# Create desktop shortcut with icon
Write-Host "`nCreating desktop shortcut..." -ForegroundColor Yellow
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "AI-CLI 3.0.lnk"
$scriptDir = $PSScriptRoot
$iconPath = Join-Path $scriptDir "ai-cli.ico"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -Command `"ai-cli`""
$shortcut.WorkingDirectory = $HOME
if (Test-Path $iconPath) {
    $shortcut.IconLocation = $iconPath
}
$shortcut.Save()

Write-Host "  Desktop shortcut created: AI-CLI 3.0" -ForegroundColor Green

Write-Host "`n" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor DarkGray
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor DarkGray
Write-Host "`nRun 'ai-cli' to start" -ForegroundColor Cyan
Write-Host "Run 'ai-cli --help' for more options" -ForegroundColor Cyan
Write-Host ""
