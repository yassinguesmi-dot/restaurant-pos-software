#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[build_apk] Project root: $ROOT_DIR"

if ! command -v buildozer >/dev/null 2>&1; then
  echo "buildozer not found. Install in WSL/Ubuntu: sudo apt install -y python3-pip && pip3 install --user --upgrade buildozer cython"
  exit 1
fi

echo "Building APK (debug)... this may take 20-60 minutes on first run"
# Use a storage dir without spaces to avoid pythonforandroid errors
STORAGE_DIR="${STORAGE_DIR:-$HOME/.buildozer_storage}"
mkdir -p "$STORAGE_DIR"

echo "Using storage dir: $STORAGE_DIR"
buildozer --storage-dir="$STORAGE_DIR" android debug

APK=$(ls -t bin/*.apk 2>/dev/null | head -n1 || true)
if [ -z "$APK" ]; then
  echo "No APK found in bin/. Check buildozer output for errors."
  exit 1
fi

echo "APK built: $APK"
echo "To install on a connected device run: ./scripts/deploy_apk_adb.sh \"$APK\""
