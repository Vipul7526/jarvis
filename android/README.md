# Android Client

The `android/` folder is reserved for the J.A.R.V.I.S. Android application built with Flutter and Java. Flutter will own the HUD, navigation, setup wizard, settings, AI interface, discovery UI, pairing UI, and diagnostics. Java will own Android permissions, microphone, speech recognition, TTS, notifications, Bluetooth, BLE, nearby devices, and foreground-service integrations where the operating system permits them.

## Setup guide

Install the pinned Flutter SDK, Android SDK, JDK, and an emulator or test device. Create the Flutter project in this folder, connect Java functionality through platform channels, and run the backend locally before testing authenticated flows.

## Permission rules

Explain each permission before requesting it, including why it is needed, what it enables, what data is involved, and how to disable it. Read the real operating-system permission state after every request. Never display a permission as granted when Android reports denied, restricted, unavailable, or not requested.

## Security

Store sessions using Android secure storage. Do not embed API keys, OAuth secrets, Gmail credentials, or the backend allowlist in the APK or Flutter assets. Use JDP/1.0 and authenticated pairing for device communication.
