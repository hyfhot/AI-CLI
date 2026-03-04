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
    # Try to install from current directory (for local development)
    if (Test-Path "pyproject.toml") {
        Write-Host "  Installing from local directory..." -ForegroundColor Cyan
        pip install -e ".[dev]"
    } else {
        # Install from PyPI
        Write-Host "  Installing from PyPI..." -ForegroundColor Cyan
        pip install ai-cli-launcher
    }
    Write-Host "  Installation complete!" -ForegroundColor Green
} catch {
    Write-Host "  Installation failed!" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Red
    exit 1
}

# Initialize config
Write-Host "`nInitializing configuration..." -ForegroundColor Yellow
ai-cli --init

# Create desktop shortcut with icon
Write-Host "`nCreating desktop shortcut..." -ForegroundColor Yellow
try {
    # Verify ai-cli is installed
    $aiCliPath = Get-Command ai-cli -ErrorAction SilentlyContinue
    if (-not $aiCliPath) {
        Write-Host "  Warning: ai-cli command not found, skipping shortcut creation" -ForegroundColor Yellow
    } else {
        $desktopPath = [Environment]::GetFolderPath("Desktop")
        $shortcutPath = Join-Path $desktopPath "AI-CLI 3.0.lnk"
        
        # Download icon from GitHub
        $iconPath = Join-Path $env:TEMP "ai-cli.ico"
        try {
            Invoke-WebRequest -Uri "https://raw.githubusercontent.com/hyfhot/AI-CLI/master/ai-cli.ico" -OutFile $iconPath -ErrorAction SilentlyContinue
        } catch {
            # If download fails, check local directory
            if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "ai-cli.ico"))) {
                $iconPath = Join-Path $PSScriptRoot "ai-cli.ico"
            } else {
                $iconPath = $null
            }
        }

        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = "powershell.exe"
        $shortcut.Arguments = "-NoProfile -Command `"ai-cli`""
        $shortcut.WorkingDirectory = $HOME
        if ($iconPath -and (Test-Path $iconPath)) {
            # Copy icon to permanent location
            $permanentIconPath = Join-Path $env:APPDATA "AI-CLI\ai-cli.ico"
            $iconDir = Split-Path $permanentIconPath -Parent
            if (-not (Test-Path $iconDir)) {
                New-Item -ItemType Directory -Path $iconDir -Force | Out-Null
            }
            Copy-Item $iconPath $permanentIconPath -Force
            $shortcut.IconLocation = $permanentIconPath
        }
        $shortcut.Save()

        Write-Host "  Desktop shortcut created: AI-CLI 3.0" -ForegroundColor Green
    }
} catch {
    Write-Host "  Warning: Failed to create desktop shortcut" -ForegroundColor Yellow
    Write-Host "  You can still run 'ai-cli' from the command line" -ForegroundColor Cyan
}

Write-Host "`n" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor DarkGray
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor DarkGray
Write-Host "`nQuick Start:" -ForegroundColor Cyan
Write-Host "  ai-cli              # Start interactive launcher"
Write-Host "  ai-cli --init       # Initialize/update configuration"
Write-Host "  ai-cli --config     # Edit configuration file"
Write-Host "  ai-cli --version    # Show version information"
Write-Host "  ai-cli --uninstall  # Uninstall AI-CLI"
Write-Host "  ai-cli --help       # Show all options"
Write-Host ""
