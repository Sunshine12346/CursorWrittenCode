#!/bin/bash
# Educational Encryption Tool - Linux Shell Script
# WARNING: This is for educational purposes only!

echo "================================================"
echo "     Educational File Encryption Tool"
echo "================================================"
echo "WARNING: This is for educational purposes only!"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    echo "Please install Python3 and try again."
    echo "Ubuntu/Debian: sudo apt install python3"
    echo "CentOS/RHEL: sudo yum install python3"
    echo "Arch: sudo pacman -S python"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if cryptography module is available
python3 -c "import cryptography" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ cryptography module is not installed"
    echo "📦 Installing cryptography..."
    
    # Try pip3 first
    if command -v pip3 &> /dev/null; then
        pip3 install cryptography
    # Try system package manager
    elif command -v apt &> /dev/null; then
        echo "Using system package manager (apt)..."
        sudo apt update && sudo apt install -y python3-cryptography
    elif command -v yum &> /dev/null; then
        echo "Using system package manager (yum)..."
        sudo yum install -y python3-cryptography
    elif command -v pacman &> /dev/null; then
        echo "Using system package manager (pacman)..."
        sudo pacman -S python-cryptography
    else
        echo "Failed to install cryptography. Please install it manually:"
        echo "pip3 install cryptography"
        echo "or use your system package manager"
        exit 1
    fi
    
    # Verify installation
    python3 -c "import cryptography" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install cryptography module"
        exit 1
    fi
fi

echo "✅ cryptography module is available"
echo

# Run the encryption script with all arguments passed to this script
echo "🚀 Starting encryption tool..."
python3 modern_encrypt.py "$@"

echo
echo "Press Enter to continue..."
read