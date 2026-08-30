# Windows Client

The `windows/` folder is reserved for the J.A.R.V.I.S. Windows desktop application. Flutter will provide the HUD, setup wizard, themes, model management, diagnostics, and device views. C++ will provide Windows system-tray behavior, global hotkeys, notifications, startup registration, and window management. Python will provide the local-AI, discovery, automation, and device-gateway services.

## Setup guide

Install Flutter with Windows desktop support, Visual Studio with the C++ desktop workload and Windows SDK, Python 3.11+, and a compatible llama.cpp build. Configure the backend and desktop-AI environment before building the client.

## Packaging

The planned release includes a signed Windows installer. Packaging must exclude secrets, private allowlists, local model files unless intentionally bundled, and development logs. The installer must verify prerequisites and report real diagnostics rather than displaying simulated online states.

## Security

The client communicates with the backend and paired devices through authenticated contracts. The desktop local-AI server remains loopback-only by default. High-impact commands require explicit user confirmation.
