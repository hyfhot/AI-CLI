#!/bin/bash
# AI-CLI PyPI Publishing Script for Linux/macOS/Windows
#
# Required environment variables (optional, can use ~/.pypirc instead):
#   TWINE_USERNAME - Username or __token__ for PyPI
#   TWINE_PASSWORD - Password or API token for PyPI
#   TWINE_TEST_USERNAME - Username for TestPyPI (defaults to TWINE_USERNAME)
#   TWINE_TEST_PASSWORD - Password for TestPyPI (defaults to TWINE_PASSWORD)

# API tokens: read from environment; fall back to placeholder so twine uses ~/.pypirc.
# Set TWINE_PASSWORD / TWINE_TEST_PASSWORD in your environment to publish.
TWINE_USERNAME="${TWINE_USERNAME:-__token__}"
TWINE_PASSWORD="${TWINE_PASSWORD:-YOUR_PYPI_TOKEN_HERE}"
TWINE_TEST_USERNAME="${TWINE_TEST_USERNAME:-__token__}"
TWINE_TEST_PASSWORD="${TWINE_TEST_PASSWORD:-YOUR_TEST_PYPI_TOKEN_HERE}"

set -e

echo ""
echo "=== AI-CLI PyPI Publishing Tool ==="
echo ""

# Detect OS
detect_os() {
    case "$(uname -s)" in
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        Darwin) echo "macos" ;;
        Linux) echo "linux" ;;
        *) echo "unknown" ;;
    esac
}

OS=$(detect_os)
echo "[0/8] Detected OS: $OS"

# Detect Python command for the OS
detect_python() {
    local py_cmd=""

    # Try common Python commands in order of preference
    local python_candidates=("python3" "python" "python3.11" "python3.10" "python3.9" "python3.8")

    for py in "${python_candidates[@]}"; do
        if command -v "$py" &> /dev/null; then
            # Verify it actually works
            if "$py" -c "import sys; sys.exit(0)" 2> /dev/null; then
                py_cmd="$py"
                break
            fi
        fi
    done

    echo "$py_cmd"
}

PYTHON_CMD=$(detect_python)
if [ -z "$PYTHON_CMD" ]; then
    echo "  ✗ Error: Python is not installed or not in PATH"
    echo "  Please install Python 3.8 or later: https://www.python.org/downloads/"
    exit 1
fi

# Verify Python version
echo ""
echo "[0.5/8] Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
echo "  Python version: $PYTHON_VERSION"

# Check if version meets minimum requirement (3.8)
if [[ ! "$PYTHON_VERSION" =~ ^([0-9]+)\.([0-9]+)$ ]]; then
    echo "  ✗ Error: Could not determine Python version"
    exit 1
fi

MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "  ✗ Error: Python 3.8+ required, but found $PYTHON_VERSION"
    exit 1
fi
echo "  ✓ Python version OK"

# Install build tools function
install_build_tools() {
    local pip_cmd=""

    # Detect pip command
    if [ "$OS" = "windows" ]; then
        # On Windows, try python -m pip first
        if $PYTHON_CMD -m pip --version &> /dev/null; then
            pip_cmd="$PYTHON_CMD -m pip"
        elif command -v pip &> /dev/null; then
            pip_cmd="pip"
        elif command -v pip3 &> /dev/null; then
            pip_cmd="pip3"
        else
            echo "  ✗ Error: pip not found. Please install pip first."
            return 1
        fi
    else
        # On Linux/macOS, try python3 -m pip first
        if $PYTHON_CMD -m pip --version &> /dev/null; then
            pip_cmd="$PYTHON_CMD -m pip"
        elif command -v pip3 &> /dev/null; then
            pip_cmd="pip3"
        elif command -v pip &> /dev/null; then
            pip_cmd="pip"
        else
            echo "  ✗ Error: pip not found. Please install pip first."
            return 1
        fi
    fi

    echo "  Installing build tools using: $pip_cmd"

    # Upgrade pip first (some systems have old pip)
    $pip_cmd install --upgrade pip 2>/dev/null || true

    # Install build and twine
    if ! $pip_cmd install --upgrade build twine; then
        echo "  ✗ Error: Failed to install build tools"
        return 1
    fi

    return 0
}

# Check if build and twine are installed
echo ""
echo "[2/8] Checking build tools..."

BUILD_OK=false
TWINE_OK=false

# Check build
if $PYTHON_CMD -m build --version &> /dev/null; then
    echo "  ✓ build is installed"
    BUILD_OK=true
else
    echo "  ✗ build not found"
fi

# Check twine
if $PYTHON_CMD -m twine --version &> /dev/null; then
    echo "  ✓ twine is installed"
    TWINE_OK=true
else
    echo "  ✗ twine not found"
fi

# Install if missing
if [ "$BUILD_OK" = false ] || [ "$TWINE_OK" = false ]; then
    echo ""
    echo "  Installing missing build tools..."
    if install_build_tools; then
        echo "  ✓ Build tools installed successfully"
    else
        echo "  ✗ Failed to install build tools"
        exit 1
    fi
else
    echo ""
    echo "  Checking for updates..."
    install_build_tools || true
fi
echo "  ✓ Build tools ready"

# On Windows, optionally create virtual environment for isolation
echo ""
echo "[2.5/8] Setting up isolated build environment (optional on Windows)..."

VENV_PYTHON=""
if [ "$OS" = "windows" ]; then
    if $PYTHON_CMD -m venv .venv &> /dev/null; then
        echo "  ✓ Virtual environment created at .venv"
        if [ -f ".venv/Scripts/activate" ]; then
            source .venv/Scripts/activate
            # In venv, use 'python' directly since it points to the venv python
            VENV_PYTHON="python"
            echo "  ✓ Virtual environment activated"

            # Re-check and install build tools in venv if needed
            if ! python -m build --version &> /dev/null || ! python -m twine --version &> /dev/null; then
                echo "  Installing build tools in virtual environment..."
                python -m pip install --upgrade pip build twine
            fi
        fi
    else
        echo "  ⚠ venv creation failed, using system Python"
    fi
fi

# Determine which python to use for the rest of the script
FINAL_PYTHON="${VENV_PYTHON:-$PYTHON_CMD}"
echo ""
echo "  Using Python: $FINAL_PYTHON"
echo ""

# Detect the correct pip command for installing ai-cli
# Traces from the ai-cli executable back to its Python
detect_install_pip() {
    local ai_cli_path=""
    local pip_cmd=""

    # Find ai-cli in PATH
    ai_cli_path=$(command -v ai-cli 2>/dev/null || command -v ai-cli.exe 2>/dev/null || echo "")

    if [ -n "$ai_cli_path" ]; then
        case "$OS" in
            windows)
                # Extract Python version from path like .../Python313/Scripts/ai-cli.exe
                if [[ "$ai_cli_path" =~ Python([0-9]+) ]]; then
                    local ver="${BASH_REMATCH[1]}"
                    local major="${ver:0:1}"
                    local minor="${ver:1}"
                    if command -v py &>/dev/null; then
                        pip_cmd="py -$major.$minor -m pip"
                    fi
                fi
                # Fallback: try prefix python.exe directly
                if [ -z "$pip_cmd" ]; then
                    local scripts_dir
                    scripts_dir=$(dirname "$ai_cli_path")
                    local prefix_dir
                    prefix_dir=$(dirname "$scripts_dir")
                    if [ -f "$prefix_dir/python.exe" ]; then
                        pip_cmd="\"$prefix_dir/python.exe\" -m pip"
                    fi
                fi
                ;;
            *)
                # On Unix, read shebang to find the Python
                if [ -f "$ai_cli_path" ] && [ -x "$ai_cli_path" ]; then
                    local shebang
                    shebang=$(head -1 "$ai_cli_path" 2>/dev/null)
                    if [[ "$shebang" =~ python([0-9]+\.[0-9]+) ]]; then
                        local py_ver="${BASH_REMATCH[1]}"
                        if command -v "python$py_ver" &>/dev/null; then
                            pip_cmd="python$py_ver -m pip"
                        fi
                    fi
                fi
                if [ -z "$pip_cmd" ] && command -v python3 &>/dev/null; then
                    pip_cmd="python3 -m pip"
                fi
                if [ -z "$pip_cmd" ] && command -v python &>/dev/null; then
                    pip_cmd="python -m pip"
                fi
                ;;
        esac
    fi

    # Fallback to the Python used by the build
    if [ -z "$pip_cmd" ]; then
        pip_cmd="$FINAL_PYTHON -m pip"
    fi

    echo "$pip_cmd"
}

# Get current version from pyproject.toml (only match version = at start of line)
echo "[3/8] Checking current version..."
if grep -qE '^version = ' pyproject.toml; then
    current_version=$(grep -E '^version = ' pyproject.toml | head -1 | sed -E 's/.*version = "([^"]+)".*/\1/')
    echo "  Current version: $current_version"

    # Calculate suggested next version (increment patch version)
    if [[ $current_version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
        patch="${BASH_REMATCH[3]}"
        suggested_version="$major.$minor.$((patch + 1))"
    else
        suggested_version="$current_version"
    fi

    echo "  Suggested version: $suggested_version"
    read -p $'\nEnter new version (press Enter for '"$suggested_version"'): ' new_version

    if [ -z "$new_version" ]; then
        new_version="$suggested_version"
    fi

    # Validate version format
    if ! [[ $new_version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "  ✗ Invalid version format! Use X.Y.Z (e.g., 3.0.1)"
        exit 1
    fi

    if [ "$new_version" = "$current_version" ]; then
        echo "  ⚠ Warning: Version unchanged ($current_version)"
        read -p "Continue anyway? (y/N): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            echo "  Cancelled by user"
            exit 0
        fi
    else
        echo "  ✓ New version: $new_version"

        # Update version in pyproject.toml
        if sed --version &> /dev/null; then
            # GNU sed (Linux, Git Bash on Windows)
            sed -i.bak -E "s/^version = \"[^^\"]+\"/version = \"$new_version\"/" pyproject.toml
        else
            # BSD sed (macOS)
            sed -i '' -E "s/^version = \"[^^\"]+\"/version = \"$new_version\"/" pyproject.toml
        fi
        rm -f pyproject.toml.bak

        # Update version in __init__.py
        if [ -f "ai_cli/__init__.py" ]; then
            if sed --version &> /dev/null; then
                sed -i.bak -E "s/__version__ = \"[^\"]+\"/__version__ = \"$new_version\"/" ai_cli/__init__.py
            else
                sed -i '' -E "s/__version__ = \"[^\"]+\"/__version__ = \"$new_version\"/" ai_cli/__init__.py
            fi
            rm -f ai_cli/__init__.py.bak
        fi

        echo "  ✓ Version updated in source files"
    fi
else
    echo "  ✗ Could not find version in pyproject.toml"
    exit 1
fi

# Clean old build files
echo ""
echo "[4/8] Cleaning old build files..."
rm -rf dist build *.egg-info .venv 2>/dev/null || true
find . -maxdepth 1 -type d -name "*.egg-info" -exec rm -rf {} + 2> /dev/null || true
find . -maxdepth 1 -type d -name "dist" -exec rm -rf {} + 2> /dev/null || true
find . -maxdepth 1 -type d -name "build" -exec rm -rf {} + 2> /dev/null || true
echo "  ✓ Cleaned"

# Build distribution packages
echo ""
echo "[5/8] Building distribution packages..."
$FINAL_PYTHON -m build
echo "  ✓ Build complete"

# Check package integrity
echo ""
echo "[6/8] Checking package integrity..."
$FINAL_PYTHON -m twine check dist/*
echo "  ✓ Package check passed"

# Check for credentials
echo ""
echo "[6.5/8] Checking credentials..."

# Check if embedded tokens are set (not placeholders)
if [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ] && [ "$TWINE_USERNAME" != "__token__" ] && [ "$TWINE_PASSWORD" != "YOUR_PYPI_TOKEN_HERE" ]; then
    echo "  ✓ Using embedded API tokens"
    USE_ENV_CREDS=true
elif [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ]; then
    echo "  ✓ Using environment variables for authentication"
    USE_ENV_CREDS=true
else
    echo "  ⚠ No credentials found in script or environment"
    echo "  ✓ Will try ~/.pypirc config (or enter credentials when prompted)"
    USE_ENV_CREDS=false
fi

echo ""
echo "[7/8] Select upload target:"
echo "  1) TestPyPI (test environment)"
echo "  2) PyPI (production)"
echo "  3) Both (TestPyPI first, then PyPI)"
echo "  0) Cancel"
read -p $'\nYour choice (0/1/2/3): ' choice

if [ "$choice" = "0" ]; then
    echo ""
    echo "Cancelled by user"
    exit 0
fi

# Upload packages
# Detect the pip command matching the user's ai-cli installation
INSTALL_PIP=$(detect_install_pip)
echo ""
echo "  Install pip: $INSTALL_PIP"
echo ""

echo "[8/8] Uploading packages..."

case $choice in
    1)
        echo "  Uploading to TestPyPI..."
        if [ "$USE_ENV_CREDS" = true ]; then
            test_user="${TWINE_TEST_USERNAME:-$TWINE_USERNAME}"
            test_pass="${TWINE_TEST_PASSWORD:-$TWINE_PASSWORD}"
            $FINAL_PYTHON -m twine upload --repository testpypi -u "$test_user" -p "$test_pass" dist/* --verbose
        else
            $FINAL_PYTHON -m twine upload --repository testpypi dist/* --verbose
        fi
        upload_success=$?
        install_cmd="$INSTALL_PIP install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cli-launcher==$new_version"
        ;;
    2)
        echo "  Uploading to PyPI..."
        if [ "$USE_ENV_CREDS" = true ]; then
            $FINAL_PYTHON -m twine upload -u "$TWINE_USERNAME" -p "$TWINE_PASSWORD" dist/* --verbose
        else
            $FINAL_PYTHON -m twine upload dist/* --verbose
        fi
        upload_success=$?
        install_cmd="$INSTALL_PIP install --upgrade ai-cli-launcher==$new_version"
        ;;
    3)
        echo "  Uploading to TestPyPI..."
        if [ "$USE_ENV_CREDS" = true ]; then
            test_user="${TWINE_TEST_USERNAME:-$TWINE_USERNAME}"
            test_pass="${TWINE_TEST_PASSWORD:-$TWINE_PASSWORD}"
            $FINAL_PYTHON -m twine upload --repository testpypi -u "$test_user" -p "$test_pass" dist/* --verbose
        else
            $FINAL_PYTHON -m twine upload --repository testpypi dist/* --verbose
        fi
        if [ $? -eq 0 ]; then
            echo "  ✓ TestPyPI upload complete"
            echo ""
            echo "  Waiting 5 seconds before uploading to PyPI..."
            sleep 5
            echo "  Uploading to PyPI..."
            if [ "$USE_ENV_CREDS" = true ]; then
                $FINAL_PYTHON -m twine upload -u "$TWINE_USERNAME" -p "$TWINE_PASSWORD" dist/* --verbose
            else
                $FINAL_PYTHON -m twine upload dist/* --verbose
            fi
            upload_success=$?
        else
            upload_success=1
        fi
        install_cmd="$INSTALL_PIP install --upgrade ai-cli-launcher==$new_version"
        ;;
    *)
        echo "  ✗ Invalid choice!"
        exit 1
        ;;
esac

# Show result
echo ""
if [ $upload_success -eq 0 ]; then
    echo "[9/9] ✓ Publishing successful!"
    echo ""
    echo "Install command:"
    echo "  $install_cmd"
    echo ""
    echo "Verify installation:"
    echo "  ai-cli --version"
else
    echo "[9/9] ✗ Publishing failed!"
    echo ""
    echo "Please check the error messages above."
    exit 1
fi

echo ""
