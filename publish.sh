#!/bin/bash
# AI-CLI PyPI Publishing Script for Linux/macOS

set -e

echo ""
echo "=== AI-CLI PyPI Publishing Tool ==="
echo ""

# Get current version from pyproject.toml
echo "[1/8] Checking current version..."
if grep -q 'version = ' pyproject.toml; then
    current_version=$(grep 'version = ' pyproject.toml | sed -E 's/.*version = "([^"]+)".*/\1/')
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
        sed -i.bak -E "s/version = \"[^\"]+\"/version = \"$new_version\"/" pyproject.toml
        rm -f pyproject.toml.bak
        
        # Update version in __init__.py
        if [ -f "ai_cli/__init__.py" ]; then
            sed -i.bak -E "s/__version__ = \"[^\"]+\"/__version__ = \"$new_version\"/" ai_cli/__init__.py
            rm -f ai_cli/__init__.py.bak
        fi
        
        echo "  ✓ Version updated in source files"
    fi
else
    echo "  ✗ Could not find version in pyproject.toml"
    exit 1
fi

# Check if build and twine are installed
echo ""
echo "[2/8] Checking build tools..."
if ! python3 -m build --version &> /dev/null || ! python3 -m twine --version &> /dev/null; then
    echo "  Installing build tools..."
    pip3 install --upgrade build twine
fi
echo "  ✓ Build tools ready"

# Clean old build files
echo ""
echo "[3/8] Cleaning old build files..."
rm -rf dist build *.egg-info
echo "  ✓ Cleaned"

# Build distribution packages
echo ""
echo "[4/8] Building distribution packages..."
python3 -m build
echo "  ✓ Build complete"

# Check package integrity
echo ""
echo "[5/8] Checking package integrity..."
twine check dist/*
echo "  ✓ Package check passed"

# Select upload target
echo ""
echo "[6/8] Select upload target:"
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
echo ""
echo "[7/8] Uploading packages..."

case $choice in
    1)
        echo "  Uploading to TestPyPI..."
        twine upload --repository testpypi dist/* --verbose
        upload_success=$?
        install_cmd="pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cli-launcher"
        ;;
    2)
        echo "  Uploading to PyPI..."
        twine upload dist/* --verbose
        upload_success=$?
        install_cmd="pip install ai-cli-launcher"
        ;;
    3)
        echo "  Uploading to TestPyPI..."
        twine upload --repository testpypi dist/* --verbose
        if [ $? -eq 0 ]; then
            echo "  ✓ TestPyPI upload complete"
            echo ""
            echo "  Waiting 5 seconds before uploading to PyPI..."
            sleep 5
            echo "  Uploading to PyPI..."
            twine upload dist/* --verbose
            upload_success=$?
        else
            upload_success=1
        fi
        install_cmd="pip install ai-cli-launcher"
        ;;
    *)
        echo "  ✗ Invalid choice!"
        exit 1
        ;;
esac

# Show result
echo ""
if [ $upload_success -eq 0 ]; then
    echo "[8/8] ✓ Publishing successful!"
    echo ""
    echo "Install command:"
    echo "  $install_cmd"
    echo ""
    echo "Verify installation:"
    echo "  ai-cli --version"
else
    echo "[8/8] ✗ Publishing failed!"
    echo ""
    echo "Please check the error messages above."
    exit 1
fi

echo ""
