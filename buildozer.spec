[app]
title = Auto-Downloader
package.name = autodownloader
package.domain = com.autodownloader

version = 1.0.0
orientation = portrait
fullscreen = 0

requirements = python3,flet,gallery-dl,requests,html2text,imageio,mutagen

[presplash]
icon = presplash.png

[android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a,armeabi-v7a
android.minapi = 21
android.sdk = 34
