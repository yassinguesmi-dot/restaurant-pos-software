# 🚀 Quick Start - Build APK in 5 Minutes

## Choose Your Method:

### 1️⃣ Automated Build Script (Easiest)
**Best for: First-time builders**

```bash
# Open WSL/Ubuntu terminal
cd /mnt/c/Users/yassi/Downloads/restaurant-pos-software\ \(2\)/restaurant-pos-software\ \(1\)/

# Run the build script
chmod +x build_apk.sh
./build_apk.sh
```

The script will:
- ✅ Check your environment
- ✅ Install dependencies
- ✅ Build the APK
- ✅ Show you where the APK is

**Time:** 30-60 minutes (first time)

---

### 2️⃣ Manual Build (Full Control)
**Best for: Experienced users**

```bash
# 1. Open WSL/Ubuntu
wsl

# 2. Navigate to project
cd /mnt/c/Users/yassi/Downloads/restaurant-pos-software\ \(2\)/restaurant-pos-software\ \(1\)/

# 3. Install buildozer
pip3 install --upgrade buildozer cython

# 4. Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential git openjdk-17-jdk \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    zip unzip autoconf libtool pkg-config zlib1g-dev

# 5. Build APK
buildozer -v android debug

# 6. Find your APK
ls -lh bin/
```

**Time:** 30-60 minutes (first time)

---

### 3️⃣ GitHub Actions (No Local Build)
**Best for: Cloud builds**

1. Push code to GitHub
2. GitHub automatically builds APK
3. Download from Actions tab

See [APK_BUILD_GUIDE.md](APK_BUILD_GUIDE.md) for setup.

---

## 📱 Install APK on Device

### Method A: Direct Transfer
1. Copy APK from `bin/` to your phone
2. Open file on phone
3. Tap "Install"

### Method B: ADB Install
```bash
# Connect device via USB
adb devices

# Install APK
adb install bin/cafe216pos-1.0-debug.apk
```

---

## ⚡ Super Quick Test (No Build)

Don't want to build? Test directly on your Android tablet:

1. Install [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) from Play Store
2. In Pydroid, run: `pip install kivy pillow`
3. Copy `main_kivy.py` and `ui/main.kv` to Pydroid
4. Run `main_kivy.py`

**Time:** 10 minutes

---

## 🔧 Prerequisites

Before starting:
- [ ] Windows 10/11 with WSL2 installed
- [ ] At least 10 GB free disk space
- [ ] Internet connection
- [ ] Android device for testing (optional)

**Don't have WSL?** Install it:
```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-22.04
```

---

## 📋 Build Checklist

Check these files exist:
- [x] `main_kivy.py` - Main app file
- [x] `ui/main.kv` - UI layout
- [x] `buildozer.spec` - Build configuration
- [x] `build_apk.sh` - Build script

All files are ready! ✅

---

## 🐛 Common Issues

### "buildozer: command not found"
```bash
pip3 install --upgrade buildozer
```

### "Cannot connect to WSL"
```powershell
# In Windows PowerShell
wsl --shutdown
wsl
```

### "No space left on device"
```bash
# Clean buildozer cache
rm -rf ~/.buildozer
```

### "Build failed"
```bash
# Try clean build
buildozer android clean
buildozer -v android debug
```

---

## 📚 Need More Help?

- **Detailed Guide:** [APK_BUILD_GUIDE.md](APK_BUILD_GUIDE.md)
- **Full Checklist:** [BUILD_CHECKLIST.md](BUILD_CHECKLIST.md)
- **Buildozer Docs:** https://buildozer.readthedocs.io/

---

## ⏱️ Expected Build Times

| Build Type | First Time | Subsequent |
|------------|------------|------------|
| Debug APK | 30-60 min | 5-10 min |
| Release APK | 30-60 min | 5-10 min |
| Clean Build | 30-60 min | 30-60 min |

*First build downloads Android SDK (~2GB) and NDK (~1GB)*

---

## 🎯 TL;DR

```bash
# The absolute fastest way:
cd /mnt/c/Users/yassi/Downloads/restaurant-pos-software\ \(2\)/restaurant-pos-software\ \(1\)/
chmod +x build_apk.sh
./build_apk.sh
```

Wait 30-60 minutes. APK appears in `bin/` folder. Done! 🎉

---

**Login credentials:**
- Username: `admin`
- Password: `admin`
