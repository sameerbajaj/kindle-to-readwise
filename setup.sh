#!/bin/bash

# Setup script for Kindle to Readwise Converter

echo "======================================"
echo "Kindle to Readwise - Setup"
echo "======================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.7 or higher from https://www.python.org/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check pip installation
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    echo "Please install pip: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

echo "✅ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All dependencies installed successfully!"
    echo ""
    echo "🎉 Setup complete! You can now run:"
    echo "   python3 kindle_to_readwise.py example.html"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
