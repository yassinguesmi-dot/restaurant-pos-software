[app]
# Configuration pour TÉLÉPHONE (Portrait)
title = Cafe216 POS Phone

# (str) Package name
package.name = cafe216posphone

# (str) Package domain
package.domain = org.cafe216

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,kv,png,jpg,jpeg,ttf,db

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, venv, build, dist, .git, .github, __pycache__, restaurant-pos-software

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3==3.11.6,kivy==2.3.0,pillow,sqlite3

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# TÉLÉPHONE: Portrait, 720x1280 optimisé
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #6B4CE6

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (int) Target Android API (Android 13)
android.api = 33

# (int) Minimum API (Android 5.0+)
android.minapi = 21

# (str) Android NDK version
android.ndk = 25c

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
# arm64-v8a pour téléphones modernes (64-bit)
android.archs = arm64-v8a

# (bool) Use private storage
android.private_storage = True

# (str) Android logcat filters
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk).
# android.release_artifact = aab

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
