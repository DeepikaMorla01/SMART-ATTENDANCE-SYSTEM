[app]

# App info
title = Smart Attendance System
package.name = smartattendance
package.domain = org.example
version = 1.0
orientation = portrait

# Source files
source.dir = .
source.include_exts = py,csv,jpg,png,kv

# Requirements (all Python dependencies for your AI app)
requirements = python3,kivy,opencv-python,face_recognition,numpy,pandas,openpyxl

# Permissions to read/write storage for CSV and Excel files
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# Fullscreen (optional)
fullscreen = 0

[buildozer]

# Log level (for debugging builds)
log_level = 2
warn_on_root = 1
