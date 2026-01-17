#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

APK_PATH=${1:-}
if [ -z "$APK_PATH" ]; then
  APK_PATH=$(ls -t bin/*.apk 2>/dev/null | head -n1 || true)
fi

if [ -z "$APK_PATH" ]; then
  echo "No APK found in bin/. Build first with ./scripts/build_apk.sh"
  exit 1
fi

if ! command -v adb >/dev/null 2>&1; then
  echo "adb not found. On Ubuntu install: sudo apt update && sudo apt install -y android-tools-adb"
  exit 1
fi

echo "Starting adb server..."
adb start-server

# If user wants to connect over Wi‑Fi: `adb connect 192.168.x.y`
DEVICES=$(adb devices | awk 'NR>1 && $2=="device" {print $1}')
if [ -z "$DEVICES" ]; then
  echo "No device detected. Connect tablet via USB or run 'adb connect <IP>' then retry."
  adb devices
  exit 1
fi

echo "Installing $APK_PATH on connected device(s)..."
adb install -r "$APK_PATH"

echo "Install finished. If install fails, check 'adb logcat' for errors."
