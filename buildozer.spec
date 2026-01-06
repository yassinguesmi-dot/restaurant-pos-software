[app]
title = Cafe216 POS
package.name = cafe216pos
package.domain = org.cafe216
source.dir = .
source.include_exts = py,kv,png,jpg,ttf
version = 0.1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.release_artifact = apk
p4a.bootstrap = sdl2
log_level = 2
warn_on_root = 0

[buildozer]
log_level = 2
warn_on_root = 0
