#!/usr/bin/env pwsh
# AI-CLI PyPI Publishing Script for Windows (PowerShell)
#
# Required environment variables (optional, can use ~/.pypirc instead):
#   TWINE_USERNAME - Username or __token__ for PyPI
#   TWINE_PASSWORD - Password or API token for PyPI
#   TWINE_TEST_USERNAME - Username for TestPyPI (defaults to TWINE_USERNAME)
#   TWINE_TEST_PASSWORD - Password for TestPyPI (defaults to TWINE_PASSWORD)

$ErrorActionPreference = "Stop"

# API tokens: read from environment; fall back to placeholder so twine uses ~/.pypirc.
# Set TWINE_PASSWORD / TWINE_TEST_PASSWORD in your environment to publish.
if (-not $env:TWINE_USERNAME) { $env:TWINE_USERNAME = "__token__" }
if (-not $env:TWINE_PASSWORD) { $env:TWINE_PASSWORD = "YOUR_PYPI_TOKEN_HERE" }
if (-not $env:TWINE_TEST_USERNAME) { $env:TWINE_TEST_USERNAME = "__token__" }
if (-not $env:TWINE_TEST_PASSWORD) { $env:TWINE_TEST_PASSWORD = "YOUR_TEST_PYPI_TOKEN_HERE" }

$TWINE_USERNAME = $env:TWINE_USERNAME
$TWINE_PASSWORD = $env:TWINE_PASSWORD
$TWINE_TEST_USERNAME = $env:TWINE_TEST_USERNAME
$TWINE_TEST_PASSWORD = $env:TWINE_TEST_PASSWORD

Write-Host "`n=== AI-CLI PyPI Publishing Tool (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# Detect OS
Write-Host "[0/8] Detected OS: windows"

# Detect Python command
function Get-PythonCommand {
    $candidates = @("python3", "python", "python3.11", "python3.10", "python3.9", "python3.8", "py")
    foreach ($py in $candidates) {
        $cmd = Get-Command $py -ErrorAction SilentlyContinue
        if ($cmd) {
            try {
                $result = & $py -c "import sys; sys.exit(0)" 2>&1
                if ($LASTEXITCODE -eq 0) {
                    return $py
                }
            } catch {}
        }
    }
    return $null
}

Write-Host "`n[0.5/8] Checking Python version..." -ForegroundColor Yellow
$PYTHON_CMD = Get-PythonCommand
if (-not $PYTHON_CMD) {
    Write-Host "  ✗ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8 or later: https://www.python.org/downloads/"
    exit 1
}

$PYTHON_VERSION = & $PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
Write-Host "  Python version: $PYTHON_VERSION"
Write-Host "  Python command: $PYTHON_CMD"

# Validate version
if ($PYTHON_VERSION -match '^(\d+)\.(\d+)$') {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "  ✗ Error: Python 3.8+ required, but found $PYTHON_VERSION" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✓ Python version OK" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error: Could not determine Python version" -ForegroundColor Red
    exit 1
}

# Install build tools function
function Install-BuildTools {
    Write-Host "  Installing build tools using: $PYTHON_CMD -m pip" -ForegroundColor Cyan
    & $PYTHON_CMD -m pip install --upgrade pip 2>$null
    & $PYTHON_CMD -m pip install --upgrade build twine
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ Error: Failed to install build tools" -ForegroundColor Red
        return $false
    }
    return $true
}

# Check build tools
Write-Host "`n[2/8] Checking build tools..." -ForegroundColor Yellow

$buildOk = $false
$twineOk = $false

try {
    & $PYTHON_CMD -m build --version 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ build is installed" -ForegroundColor Green
        $buildOk = $true
    } else {
        Write-Host "  ✗ build not found" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ build not found" -ForegroundColor Red
}

try {
    & $PYTHON_CMD -m twine --version 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ twine is installed" -ForegroundColor Green
        $twineOk = $true
    } else {
        Write-Host "  ✗ twine not found" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ twine not found" -ForegroundColor Red
}

if (-not $buildOk -or -not $twineOk) {
    Write-Host "`n  Installing missing build tools..." -ForegroundColor Cyan
    if (-not (Install-BuildTools)) {
        exit 1
    }
    Write-Host "  ✓ Build tools installed successfully" -ForegroundColor Green
} else {
    Write-Host "`n  Checking for updates..." -ForegroundColor Cyan
    Install-BuildTools | Out-Null
}
Write-Host "  ✓ Build tools ready" -ForegroundColor Green

# Setup isolated build environment (optional on Windows)
Write-Host "`n[2.5/8] Setting up isolated build environment..." -ForegroundColor Yellow

# Clean old venv first to ensure a fresh environment
if (Test-Path ".venv") {
    Remove-Item -Recurse -Force ".venv" -ErrorAction SilentlyContinue
}

$VENV_PYTHON = ""
try {
    & $PYTHON_CMD -m venv .venv 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Virtual environment created at .venv" -ForegroundColor Green
        $venvActivate = ".venv\Scripts\activate.ps1"
        if (Test-Path $venvActivate) {
            & $venvActivate
            $VENV_PYTHON = "python"
            Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

            # Re-check and install build tools in venv if needed
            & python -m build --version 2>$null | Out-Null
            $buildInVenv = ($LASTEXITCODE -eq 0)
            & python -m twine --version 2>$null | Out-Null
            $twineInVenv = ($LASTEXITCODE -eq 0)

            if (-not $buildInVenv -or -not $twineInVenv) {
                Write-Host "  Installing build tools in virtual environment..." -ForegroundColor Cyan
                python -m pip install --upgrade pip build twine
            }
        }
    }
} catch {
    Write-Host "  ⚠ venv creation failed, using system Python" -ForegroundColor Yellow
    $VENV_PYTHON = ""
}

$FINAL_PYTHON = if ($VENV_PYTHON) { $VENV_PYTHON } else { $PYTHON_CMD }
Write-Host "`n  Using Python: $FINAL_PYTHON" -ForegroundColor Cyan
Write-Host ""

# Detect the pip command matching the user's ai-cli installation
function Get-InstallPip {
    $aiCliPath = Get-Command ai-cli, ai-cli.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($aiCliPath) {
        $path = $aiCliPath.Source
        # Extract Python version from path like .../Python313/Scripts/ai-cli.exe
        if ($path -match 'Python(\d)(\d+)') {
            $major = $matches[1]
            $minor = $matches[2]
            $pyCmd = Get-Command py -ErrorAction SilentlyContinue
            if ($pyCmd) {
                return "py -$major.$minor -m pip"
            }
        }
        # Fallback: try prefix python.exe directly
        $scriptsDir = Split-Path $path -Parent
        $prefixDir = Split-Path $scriptsDir -Parent
        $prefixPython = Join-Path $prefixDir "python.exe"
        if (Test-Path $prefixPython) {
            return "`"$prefixPython`" -m pip"
        }
    }
    # Fallback to default
    return "$FINAL_PYTHON -m pip"
}

# Get current version from pyproject.toml
Write-Host "[3/8] Checking current version..." -ForegroundColor Yellow
$pyprojectContent = Get-Content "pyproject.toml" -Raw
if ($pyprojectContent -match '(?m)^version\s*=\s*"([^"]+)"') {
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
        $pyprojectContent = $pyprojectContent -replace '(?m)^(version\s*=\s*)"[^"]+"', "`${1}`"$newVersion`""
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

# Clean old build files
Write-Host "`n[4/8] Cleaning old build files..." -ForegroundColor Yellow
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Get-ChildItem -Directory -Filter "*.egg-info" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Write-Host "  ✓ Cleaned" -ForegroundColor Green

# Build distribution packages
Write-Host "`n[5/8] Building distribution packages..." -ForegroundColor Yellow
& $FINAL_PYTHON -m build
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Build complete" -ForegroundColor Green

# Check package integrity
Write-Host "`n[6/8] Checking package integrity..." -ForegroundColor Yellow
& $FINAL_PYTHON -m twine check dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Package check failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Package check passed" -ForegroundColor Green

# Check credentials
Write-Host "`n[6.5/8] Checking credentials..." -ForegroundColor Yellow
$USE_ENV_CREDS = $false
if ($TWINE_USERNAME -and $TWINE_PASSWORD -and $TWINE_USERNAME -eq "__token__" -and $TWINE_PASSWORD -ne "YOUR_PYPI_TOKEN_HERE") {
    Write-Host "  ✓ Using embedded API tokens" -ForegroundColor Green
    $USE_ENV_CREDS = $true
} elseif ($TWINE_USERNAME -and $TWINE_PASSWORD) {
    Write-Host "  ✓ Using environment variables for authentication" -ForegroundColor Green
    $USE_ENV_CREDS = $true
} else {
    Write-Host "  ⚠ No credentials found in script or environment" -ForegroundColor Yellow
    Write-Host "  ✓ Will try ~/.pypirc config (or enter credentials when prompted)" -ForegroundColor Green
}

# Detect the pip command matching the user's ai-cli installation
$INSTALL_PIP = Get-InstallPip

# Select upload target
Write-Host "`n[7/8] Select upload target:" -ForegroundColor Yellow
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
Write-Host "`n[8/8] Uploading packages..." -ForegroundColor Yellow
Write-Host "  Install pip: $INSTALL_PIP" -ForegroundColor Cyan
Write-Host ""

$uploadSuccess = $false

switch ($choice) {
    "1" {
        Write-Host "  Uploading to TestPyPI..." -ForegroundColor Cyan
        if ($USE_ENV_CREDS) {
            $testUser = if ($TWINE_TEST_USERNAME) { $TWINE_TEST_USERNAME } else { $TWINE_USERNAME }
            $testPass = if ($TWINE_TEST_PASSWORD) { $TWINE_TEST_PASSWORD } else { $TWINE_PASSWORD }
            & $FINAL_PYTHON -m twine upload --repository testpypi -u $testUser -p $testPass dist/* --verbose
        } else {
            & $FINAL_PYTHON -m twine upload --repository testpypi dist/* --verbose
        }
        $uploadSuccess = ($LASTEXITCODE -eq 0)
        $installCmd = "$INSTALL_PIP install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cli-launcher==$newVersion"
    }
    "2" {
        Write-Host "  Uploading to PyPI..." -ForegroundColor Cyan
        if ($USE_ENV_CREDS) {
            & $FINAL_PYTHON -m twine upload -u $TWINE_USERNAME -p $TWINE_PASSWORD dist/* --verbose
        } else {
            & $FINAL_PYTHON -m twine upload dist/* --verbose
        }
        $uploadSuccess = ($LASTEXITCODE -eq 0)
        $installCmd = "$INSTALL_PIP install --upgrade ai-cli-launcher==$newVersion"
    }
    "3" {
        Write-Host "  Uploading to TestPyPI..." -ForegroundColor Cyan
        if ($USE_ENV_CREDS) {
            $testUser = if ($TWINE_TEST_USERNAME) { $TWINE_TEST_USERNAME } else { $TWINE_USERNAME }
            $testPass = if ($TWINE_TEST_PASSWORD) { $TWINE_TEST_PASSWORD } else { $TWINE_PASSWORD }
            & $FINAL_PYTHON -m twine upload --repository testpypi -u $testUser -p $testPass dist/* --verbose
        } else {
            & $FINAL_PYTHON -m twine upload --repository testpypi dist/* --verbose
        }
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ TestPyPI upload complete" -ForegroundColor Green
            Write-Host "`n  Waiting 5 seconds before uploading to PyPI..." -ForegroundColor Cyan
            Start-Sleep -Seconds 5
            Write-Host "  Uploading to PyPI..." -ForegroundColor Cyan
            if ($USE_ENV_CREDS) {
                & $FINAL_PYTHON -m twine upload -u $TWINE_USERNAME -p $TWINE_PASSWORD dist/* --verbose
            } else {
                & $FINAL_PYTHON -m twine upload dist/* --verbose
            }
            $uploadSuccess = ($LASTEXITCODE -eq 0)
        } else {
            $uploadSuccess = $false
        }
        $installCmd = "$INSTALL_PIP install --upgrade ai-cli-launcher==$newVersion"
    }
    default {
        Write-Host "  ✗ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

# Show result
Write-Host ""
if ($uploadSuccess) {
    Write-Host "[9/9] ✓ Publishing successful!" -ForegroundColor Green
    Write-Host "`nInstall command:" -ForegroundColor Cyan
    Write-Host "  $installCmd" -ForegroundColor White
    Write-Host "`nVerify installation:" -ForegroundColor Cyan
    Write-Host "  ai-cli --version" -ForegroundColor White
} else {
    Write-Host "[9/9] ✗ Publishing failed!" -ForegroundColor Red
    Write-Host "`nPlease check the error messages above." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
