# APK Build - Pre-Build Checklist

## ✅ Environment Setup
- [ ] WSL2 or Linux environment installed
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Buildozer installed (`buildozer --version`)
- [ ] At least 10 GB free disk space
- [ ] Internet connection active and working

## ✅ Project Files
- [ ] `main_kivy.py` exists in project root
- [ ] `ui/main.kv` exists with complete UI layout
- [ ] `buildozer.spec` configured correctly
- [ ] No syntax errors in Python files
- [ ] Kivy version specified (kivy==2.2.0)

## ✅ Build Configuration
- [ ] Package name set: `cafe216pos`
- [ ] Version number updated
- [ ] Orientation set to landscape
- [ ] Android API levels configured (min 21, target 31)
- [ ] Permissions listed (if needed)
- [ ] Architecture set (arm64-v8a, armeabi-v7a)

## ✅ System Dependencies Installed
```bash
sudo apt-get install -y \
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
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config
```
- [ ] All system packages installed without errors

## ✅ Python Dependencies
```bash
pip3 install --upgrade buildozer cython
```
- [ ] Buildozer installed successfully
- [ ] Cython installed successfully

## ✅ First Build Preparation
- [ ] Java installed (`java -version`)
- [ ] Git installed (`git --version`)
- [ ] Understand first build takes 30-60 minutes
- [ ] Ready to accept SDK licenses

## ✅ Build Commands Ready

### Debug Build (for testing)
```bash
buildozer -v android debug
```

### Clean Build (if rebuild needed)
```bash
buildozer android clean
buildozer -v android debug
```

### Release Build (for distribution)
```bash
buildozer -v android release
```

## ✅ Post-Build Verification
- [ ] APK file created in `bin/` directory
- [ ] APK file size is reasonable (10-50 MB)
- [ ] No critical errors in build log
- [ ] APK filename: `cafe216pos-1.0-debug.apk`

## ✅ Testing Setup
- [ ] Android device available for testing
- [ ] USB debugging enabled on device
- [ ] ADB installed (optional): `sudo apt-get install android-tools-adb`
- [ ] Device recognized: `adb devices`

## ✅ Installation Methods Prepared

### Method 1: Direct Install
- [ ] Copy APK to device
- [ ] Enable "Install from Unknown Sources"
- [ ] Open APK file on device

### Method 2: ADB Install
```bash
adb install bin/cafe216pos-1.0-debug.apk
```
- [ ] ADB connection working

### Method 3: Cloud Transfer
- [ ] Upload location ready (Drive, Dropbox, etc.)
- [ ] Device can download from cloud

## 🔧 Troubleshooting Checklist

### If Build Fails
- [ ] Check build log in `.buildozer/logs/`
- [ ] Verify internet connection: `ping google.com`
- [ ] Check disk space: `df -h`
- [ ] Try clean build: `buildozer android clean`
- [ ] Update buildozer: `pip3 install --upgrade buildozer`

### Network Issues (WSL)
```bash
# Fix DNS in WSL
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```
- [ ] DNS resolution working

### Java Issues
```bash
# Set correct Java version
sudo update-alternatives --config java
```
- [ ] Java 11 or 17 selected

### Permission Issues
```bash
# Make script executable
chmod +x build_apk.sh
```
- [ ] Build script has execute permissions

## 📝 Build Logs Location
- Main log: `.buildozer/logs/`
- Android log: `.buildozer/android/platform/python-for-android/`
- Keep logs for debugging if build fails

## 🚀 Ready to Build!

Once all checkboxes are marked:
```bash
# Run the automated build script
./build_apk.sh

# Or manual build
buildozer -v android debug
```

## 📱 After Successful Build

Test these on device:
- [ ] App launches successfully
- [ ] Login screen displays correctly
- [ ] Login with admin/admin works
- [ ] Navigation to home screen works
- [ ] All menu buttons visible
- [ ] Landscape orientation works
- [ ] No crashes on basic navigation

## 🎯 Build Time Expectations

**First Build:**
- Download SDK: 10-15 minutes
- Download NDK: 5-10 minutes
- Compile dependencies: 15-30 minutes
- Build APK: 5-10 minutes
- **Total: 30-60 minutes**

**Subsequent Builds:**
- Code changes only: 2-5 minutes
- Dependency changes: 5-10 minutes

---

## Quick Command Reference

```bash
# Check buildozer version
buildozer --version

# Initialize buildozer.spec (if needed)
buildozer init

# Show buildozer help
buildozer --help

# Build debug APK
buildozer -v android debug

# Build and deploy to connected device
buildozer android debug deploy run

# Clean everything
buildozer android clean

# Build release APK
buildozer android release

# Show device logs
adb logcat | grep python
```

---

**Remember:** Be patient with the first build. It downloads and compiles a lot of dependencies!
