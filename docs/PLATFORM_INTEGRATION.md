# J.A.R.V.I.S. Platform Integration Guide

## Android: Flutter + Java

The Flutter layer should own navigation, HUD state, settings, setup progress, legal screens, diagnostics presentation, and discovery/pairing UI. Java platform channels should own Android permission checks and requests, microphone and speech-recognition adapters, TTS, notifications, Bluetooth/BLE, nearby-device access, foreground-service behavior where permitted, and battery-optimization guidance.

Every permission screen should show why the permission is needed, what it enables, what data is involved, and how to disable it. The result must be read from the operating system after the request. A denied, restricted, unavailable, or not-yet-requested permission must never be displayed as granted.

The Android client should use the shared JDP contract for device communication and should never connect to a desktop's localhost address as if it belonged to the phone. The Android build must keep backend session tokens in an appropriate secure storage implementation and must not include provider secrets or the backend allowlist.

## Windows: Flutter + C++ + Python

The Flutter layer should own the HUD, setup wizard, theme/font configuration, model-management UI, diagnostics, and device views. The C++ bridge should own Windows-specific system-tray behavior, global hotkeys, notifications, startup registration, and window-management operations. The Python local-AI service should own llama.cpp process management, GGUF model detection, local HTTP health, inference requests, resource checks, and streaming adaptation.

The local-AI service should bind to loopback by default and should expose executable detection, model detection, process state, HTTP health, and inference-test results separately. Only a successful real inference test may mark the model as ready. A Windows packaging stage must define the final supervisor and port arrangement so the manager, adapter, and llama.cpp server do not collide.

## OAuth and email OTP

OAuth must be completed server-side with state validation, redirect URI allowlisting, PKCE where supported, secure token handling, and short-lived sessions. Email OTP must use cryptographically secure random values, a short expiry, one-time use, attempt limits, resend cooldowns, rate limiting, and audit events that never contain OTP values. Gmail SMTP/application-password configuration is backend-only and must be injected as deployment secrets.

## Production persistence

The current backend repositories are in-memory for deterministic first-slice tests. Before production, replace them with a shared database and a cache or key-value store for sessions, replay IDs, OTP throttles, pairing sessions, legal acceptance history, devices, audit logs, and admin changes. Add migrations, backups, key rotation, retention jobs, observability, and failure recovery before enabling public access.

## Setup-wizard acceptance criteria

A complete client must execute the ordered setup state machine in `contracts/SETUP_STATE_MACHINE.md`. It must not open the main HUD immediately after legal acceptance. It must continue through permissions, account, provider configuration, local AI, llama.cpp, model, voice, wake word, discovery, pairing, theme, fonts, diagnostics, initialization, and only then `READY`.

## Native build prerequisites

This initial environment did not provide the Flutter/Dart, Android SDK, or Windows GUI toolchains. To build the clients, install and pin the required Flutter SDK, Android SDK/JDK, Windows desktop SDK, Visual Studio C++ workload, and platform-specific voice/Bluetooth dependencies. The backend and local-AI code are intentionally structured so those client adapters can be added without changing the security or protocol contracts.
