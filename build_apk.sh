#!/bin/bash
# APK Build Script for Cafe216 POS
# This script automates the APK building process using Buildozer

set -e  # Exit on error

echo "========================================="
echo "  Cafe216 POS APK Build Script"
echo "========================================="
echo ""

# Check if we're in WSL or Linux
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "✓ Running in WSL"
    ENV_TYPE="WSL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✓ Running in Linux"
    ENV_TYPE="Linux"
else
    echo "✗ This script must run in Linux or WSL"
    exit 1
fi

# Check Python version
echo ""
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if buildozer is installed
echo ""
echo "Checking Buildozer installation..."
if ! command -v buildozer &> /dev/null; then
    echo "✗ Buildozer not found. Installing..."
    pip3 install --upgrade buildozer
    pip3 install --upgrade cython
else
    echo "✓ Buildozer is installed"
fi

# Install system dependencies (Ubuntu/Debian)
echo ""
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libgstreamer1.0-dev \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config

echo "✓ System dependencies installed"

# Clean previous builds (optional)
read -p "Clean previous builds? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleaning .buildozer and bin directories..."
    rm -rf .buildozer
    rm -rf bin
    echo "✓ Cleaned"
fi

# Build debug APK
echo ""
echo "========================================="
echo "  Starting APK Build (Debug Mode)"
echo "========================================="
echo ""
buildozer -v android debug

# Check if build was successful
if [ -f "bin/*.apk" ]; then
    echo ""
    echo "========================================="
    echo "  ✓ BUILD SUCCESSFUL!"
    echo "========================================="
    echo ""
    echo "APK Location:"
    ls -lh bin/*.apk
    echo ""
    echo "To install on device:"
    echo "  adb install bin/cafe216pos-1.0-debug.apk"
    echo ""
    echo "Or transfer the APK to your Android device and install manually."
else
    echo ""
    echo "========================================="
    echo "  ✗ BUILD FAILED"
    echo "========================================="
    echo ""
    echo "Check the output above for errors."
    echo "Common issues:"
    echo "  - Missing system dependencies"
    echo "  - Network connectivity issues"
    echo "  - Java/SDK version conflicts"
    exit 1
fi
