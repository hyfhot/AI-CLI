#!/usr/bin/env pwsh
# AI-CLI PyPI Publishing Script for Windows

$ErrorActionPreference = "Stop"

Write-Host "`n=== AI-CLI PyPI Publishing Tool ===" -ForegroundColor Cyan
Write-Host ""

# Get current version from pyproject.toml
Write-Host "[1/8] Checking current version..." -ForegroundColor Yellow
$pyprojectContent = Get-Content "pyproject.toml" -Raw
if ($pyprojectContent -match 'version\s*=\s*"([^"]+)"') {
    $currentVersion = $matches[1]
    Write-Host "  Current version: $currentVersion" -ForegroundColor Cyan
    
    # Calculate suggested next version (increment patch version)
    if ($currentVersion -match '^(\d+)\.(\d+)\.(\d+)$') {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        $patch = [int]$matches[3]
        $suggestedVersion = "$major.$minor.$($patch + 1)"
    } else {
        $suggestedVersion = $currentVersion
    }
    
    Write-Host "  Suggested version: $suggestedVersion" -ForegroundColor Green
    $newVersion = Read-Host "`nEnter new version (press Enter for $suggestedVersion)"
    
    if ([string]::IsNullOrWhiteSpace($newVersion)) {
        $newVersion = $suggestedVersion
    }
    
    # Validate version format
    if ($newVersion -notmatch '^\d+\.\d+\.\d+$') {
        Write-Host "  ✗ Invalid version format! Use X.Y.Z (e.g., 3.0.1)" -ForegroundColor Red
        exit 1
    }
    
    if ($newVersion -eq $currentVersion) {
        Write-Host "  ⚠ Warning: Version unchanged ($currentVersion)" -ForegroundColor Yellow
        $confirm = Read-Host "Continue anyway? (y/N)"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "  Cancelled by user" -ForegroundColor Yellow
            exit 0
        }
    } else {
        Write-Host "  ✓ New version: $newVersion" -ForegroundColor Green
        
        # Update version in pyproject.toml
        $pyprojectContent = $pyprojectContent -replace 'version\s*=\s*"[^"]+"', "version = `"$newVersion`""
        Set-Content "pyproject.toml" -Value $pyprojectContent -NoNewline
        
        # Update version in __init__.py
        $initPath = "ai_cli\__init__.py"
        if (Test-Path $initPath) {
            $initContent = Get-Content $initPath -Raw
            $initContent = $initContent -replace '__version__\s*=\s*"[^"]+"', "__version__ = `"$newVersion`""
            Set-Content $initPath -Value $initContent -NoNewline
        }
        
        Write-Host "  ✓ Version updated in source files" -ForegroundColor Green
    }
} else {
    Write-Host "  ✗ Could not find version in pyproject.toml" -ForegroundColor Red
    exit 1
}

# Check if build and twine are installed
Write-Host "`n[2/8] Checking build tools..." -ForegroundColor Yellow
try {
    python -m build --version | Out-Null
    python -m twine --version | Out-Null
    Write-Host "  ✓ Build tools ready" -ForegroundColor Green
} catch {
    Write-Host "  Installing build tools..." -ForegroundColor Cyan
    pip install --upgrade build twine
}

# Clean old build files
Write-Host "`n[3/8] Cleaning old build files..." -ForegroundColor Yellow
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
Write-Host "  ✓ Cleaned" -ForegroundColor Green

# Build distribution packages
Write-Host "`n[4/8] Building distribution packages..." -ForegroundColor Yellow
python -m build
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Build complete" -ForegroundColor Green

# Check package integrity
Write-Host "`n[5/8] Checking package integrity..." -ForegroundColor Yellow
twine check dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Package check failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Package check passed" -ForegroundColor Green

# Select upload target
Write-Host "`n[6/8] Select upload target:" -ForegroundColor Yellow
Write-Host "  1) TestPyPI (test environment)"
Write-Host "  2) PyPI (production)"
Write-Host "  3) Both (TestPyPI first, then PyPI)"
Write-Host "  0) Cancel"
$choice = Read-Host "`nYour choice (0/1/2/3)"

if ($choice -eq "0") {
    Write-Host "`nCancelled by user" -ForegroundColor Yellow
    exit 0
}

# Upload packages
Write-Host "`n[7/8] Uploading packages..." -ForegroundColor Yellow

switch ($choice) {
    "1" {
        Write-Host "  Uploading to TestPyPI..." -ForegroundColor Cyan
        twine upload --repository testpypi dist/* --verbose
        $uploadSuccess = $LASTEXITCODE -eq 0
        $installCmd = "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cli-launcher"
    }
    "2" {
        Write-Host "  Uploading to PyPI..." -ForegroundColor Cyan
        twine upload dist/* --verbose
        $uploadSuccess = $LASTEXITCODE -eq 0
        $installCmd = "pip install ai-cli-launcher"
    }
    "3" {
        Write-Host "  Uploading to TestPyPI..." -ForegroundColor Cyan
        twine upload --repository testpypi dist/* --verbose
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ TestPyPI upload complete" -ForegroundColor Green
            Write-Host "`n  Waiting 5 seconds before uploading to PyPI..." -ForegroundColor Cyan
            Start-Sleep -Seconds 5
            Write-Host "  Uploading to PyPI..." -ForegroundColor Cyan
            twine upload dist/* --verbose
            $uploadSuccess = $LASTEXITCODE -eq 0
        } else {
            $uploadSuccess = $false
        }
        $installCmd = "pip install ai-cli-launcher"
    }
    default {
        Write-Host "  ✗ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

# Show result
Write-Host ""
if ($uploadSuccess) {
    Write-Host "[8/8] ✓ Publishing successful!" -ForegroundColor Green
    Write-Host "`nInstall command:" -ForegroundColor Cyan
    Write-Host "  $installCmd" -ForegroundColor White
    Write-Host "`nVerify installation:" -ForegroundColor Cyan
    Write-Host "  ai-cli --version" -ForegroundColor White
} else {
    Write-Host "[8/8] ✗ Publishing failed!" -ForegroundColor Red
    Write-Host "`nPlease check the error messages above." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
