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
# Try to install from current directory (for local development)
if [ -f "pyproject.toml" ]; then
    echo "  Installing from local directory..."
    pip3 install -e ".[dev]"
else
    # Install from GitHub
    echo "  Installing from GitHub..."
    pip3 install git+https://github.com/hyfhot/AI-CLI.git@master
fi
echo "  Installation complete!"

# Initialize config
echo ""
echo "Initializing configuration..."
ai-cli --init

# Create desktop shortcut
echo ""
echo "Creating desktop shortcut..."

# Verify ai-cli is installed
if ! command -v ai-cli &> /dev/null; then
    echo "  Warning: ai-cli command not found, skipping shortcut creation"
else
    # Determine desktop directory
    if [ -n "$XDG_DESKTOP_DIR" ]; then
        DESKTOP_DIR="$XDG_DESKTOP_DIR"
    elif [ -d "$HOME/Desktop" ]; then
        DESKTOP_DIR="$HOME/Desktop"
    elif [ -d "$HOME/Рабочий стол" ]; then
        DESKTOP_DIR="$HOME/Рабочий стол"
    else
        DESKTOP_DIR=""
    fi

    if [ -n "$DESKTOP_DIR" ]; then
        # Download icon if not present locally
        ICON_PATH="$HOME/.local/share/icons/ai-cli.png"
        mkdir -p "$HOME/.local/share/icons"
        
        if [ -f "ai-cli.ico" ]; then
            # Convert .ico to .png if ImageMagick is available
            if command -v convert &> /dev/null; then
                convert "ai-cli.ico[0]" "$ICON_PATH" 2>/dev/null || cp "ai-cli.ico" "$ICON_PATH"
            else
                cp "ai-cli.ico" "$ICON_PATH"
            fi
        else
            # Download from GitHub
            curl -fsSL "https://raw.githubusercontent.com/hyfhot/AI-CLI/master/ai-cli.ico" -o "$ICON_PATH" 2>/dev/null || true
        fi

        # Create .desktop file
        DESKTOP_FILE="$DESKTOP_DIR/ai-cli.desktop"
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AI-CLI 3.0
Comment=AI Coding Assistant Launcher
Exec=bash -c 'ai-cli; exec bash'
Icon=$ICON_PATH
Terminal=true
Categories=Development;Utility;
EOF
        
        chmod +x "$DESKTOP_FILE"
        echo "  Desktop shortcut created: AI-CLI 3.0"
    else
        echo "  Desktop directory not found, skipping shortcut creation"
    fi
fi

echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "Quick Start:"
echo "  ai-cli              # Start interactive launcher"
echo "  ai-cli --init       # Initialize/update configuration"
echo "  ai-cli --config     # Edit configuration file"
echo "  ai-cli --version    # Show version information"
echo "  ai-cli --uninstall  # Uninstall AI-CLI"
echo "  ai-cli --help       # Show all options"
echo ""
