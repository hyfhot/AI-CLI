#!/bin/bash
# AI-CLI Installer for Linux/macOS

set -e

echo ""
echo "AI-CLI Installer"
echo "=================================================="

# Check Python
echo ""
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  Found: $PYTHON_VERSION"
else
    echo "  Python 3 not found!"
    echo "  Please install Python 3.8+ first"
    exit 1
fi

# Install via pip
echo ""
echo "Installing AI-CLI..."
pip3 install -e ".[dev]"
echo "  Installation complete!"

# Initialize config
echo ""
echo "Initializing configuration..."
ai-cli --init

echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "Run 'ai-cli' to start"
echo "Run 'ai-cli --help' for more options"
echo ""
