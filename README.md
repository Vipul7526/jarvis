<div align="center">

# J.A.R.V.I.S.

### Just A Rather Very Intelligent System

<p>
  <strong>A secure, cross-platform personal AI assistant ecosystem for Android, Windows, and authorized devices.</strong>
</p>

<p>
  <a href="https://github.com/Vipul7526/jarvis"><img src="https://img.shields.io/badge/Project-J.A.R.V.I.S.-00D9FF?style=for-the-badge&logo=probot&logoColor=white" alt="J.A.R.V.I.S. project"></a>
  <a href="https://github.com/Vipul7526/jarvis/stargazers"><img src="https://img.shields.io/github/stars/Vipul7526/jarvis?style=for-the-badge&logo=github&logoColor=white&color=yellow" alt="GitHub stars"></a>
  <a href="https://github.com/Vipul7526/jarvis/issues"><img src="https://img.shields.io/github/issues/Vipul7526/jarvis?style=for-the-badge&logo=github&logoColor=white" alt="GitHub issues"></a>
  <a href="https://github.com/Vipul7526/jarvis/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Vipul7526/jarvis?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT license"></a>
</p>

<p>
  <a href="#-about"><strong>About</strong></a> ·
  <a href="#-features"><strong>Features</strong></a> ·
  <a href="#-architecture"><strong>Architecture</strong></a> ·
  <a href="#-roadmap"><strong>Roadmap</strong></a> ·
  <a href="#-contributing"><strong>Contribute</strong></a>
</p>

</div>

---

## About

**J.A.R.V.I.S.** is a security-first personal AI assistant designed to connect intelligent conversations, local inference, voice interaction, automation, and authorized device control into one ecosystem.

It can route requests between configured cloud AI providers, phone-local models, Windows desktop AI powered by **llama.cpp**, and a deterministic offline command core. When the Internet is unavailable, J.A.R.V.I.S. is designed to continue operating through local models, nearby authorized devices, and predefined offline capabilities.

The project is being developed as a distributed system rather than a UI-only demo. Android and Windows clients are designed to work as parts of the same ecosystem through authenticated sessions, structured device communication, secure pairing, and explicit permission controls.

> **Vision:** Build a private, extensible, and intelligent assistant that remains useful online and offline while keeping the user in control of credentials, permissions, devices, and data.

## Platforms

<p align="center">
  <a href="https://www.android.com/"><img src="https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android"></a>
  <a href="https://www.microsoft.com/windows/"><img src="https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"></a>
  <a href="https://flutter.dev/"><img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white" alt="Flutter"></a>
</p>

| Platform | Role |
|---|---|
| **Android** | Mobile assistant, voice interface, wake-word support, discovery, pairing, notifications, and device control. |
| **Windows** | Desktop HUD, system integration, local AI, llama.cpp management, model management, automation, and device gateway. |
| **Authorized devices** | Phones, PCs, tablets, TVs, media devices, and supported IoT devices connected through explicit pairing and permissions. |

## Features

### AI and intelligence

- Online AI through configurable cloud providers.
- Offline Core for predefined commands, calculations, cached information, and local status checks.
- Local AI support using **llama.cpp** and **GGUF** models.
- AI routing with graceful fallback between cloud, phone-local, desktop-local, and offline processing.
- Streaming response architecture for conversational experiences.
- Model detection, selection, health monitoring, and inference testing.

### Voice interaction

- Speech-to-text and text-to-speech support.
- Local voice activity detection.
- Local wake-word detection with `JARVIS` and optional `Hey JARVIS` support.
- Conversation states such as `IDLE`, `LISTENING`, `THINKING`, `SPEAKING`, `EXECUTING`, `OFFLINE`, and `ERROR`.
- Explicit microphone and speech permission explanations.

### Device ecosystem

- JARVIS Discovery over supported LAN, mDNS/DNS-SD, UDP, Bluetooth, and BLE transports.
- Structured **JDP/1.0** messages instead of natural-language security decisions.
- QR-code and numeric-code device pairing.
- Device trust states, capabilities, permissions, timestamps, and revocation.
- Authorized control for supported PCs, Android devices, TVs, media devices, and IoT hardware.
- Phone-to-desktop local AI through authenticated transport; the phone never treats the desktop's localhost as its own.

### Security and privacy

- Backend-controlled approved-user authorization.
- OAuth 2.0 / OpenID Connect integration boundary.
- Email OTP security boundary with expiry, one-time use, rate limits, and attempt limits.
- Signed, expiring sessions and replay protection.
- Role-based access control for users and administrators.
- High-risk command confirmation for shutdown, restart, deletion, and sensitive operations.
- Backend-only API keys, OAuth secrets, Gmail credentials, and allowlists.
- Audit events and truthful diagnostics that never claim unavailable components are online.

### Experience and operations

- Cinematic HUD with an original futuristic visual language.
- Theme system with blue, cyan, amber, green, purple, magenta, orange, red, white, and custom options.
- Online Google Fonts with bundled offline font fallbacks.
- Guided setup wizard from legal acceptance through initialization.
- Permission Center, Legal Center, Help Center, diagnostics, and administration surfaces.
- Plugin and skill architecture with capability-based access.

## Technology stack

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://dart.dev/"><img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white" alt="Dart"></a>
  <a href="https://www.java.com/"><img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java"></a>
  <a href="https://isocpp.org/"><img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://github.com/ggml-org/llama.cpp"><img src="https://img.shields.io/badge/llama.cpp-Local_AI-111111?style=for-the-badge&logo=github&logoColor=white" alt="llama.cpp"></a>
</p>

| Layer | Technologies |
|---|---|
| **Mobile client** | Flutter, Dart, Java, Android APIs, platform channels |
| **Desktop client** | Flutter, Dart, C++, Windows APIs, Python |
| **Backend** | Python, FastAPI, WebSocket, typed contracts |
| **Local AI** | llama.cpp, GGUF, localhost HTTP service |
| **Communication** | JDP/1.0, LAN, mDNS/DNS-SD, UDP, Bluetooth, BLE |
| **Security** | OAuth 2.0 / OIDC, PKCE where supported, OTP, RBAC, signed sessions |
| **Testing** | Pytest, API-level tests, platform integration tests planned |

## Architecture

```text
                         J.A.R.V.I.S.
                               |
                          JARVIS CORE
                               |
                       AI ORCHESTRATOR
                               |
             +-----------------+-----------------+
             |                 |                 |
          CLOUD AI       PHONE LOCAL       DESKTOP AI
             |                 |                 |
       +-----+-----+           |           llama.cpp
       |     |     |           |               |
     Groq  OpenAI Google   Phone Model     GGUF Model
                                                 |
                                      localhost-only service

Android / Windows / authorized devices
                |
       JARVIS Discovery + JDP/1.0
                |
        Secure pairing + permissions
                |
          Device Gateway / Automation
```

### AI fallback flow

```text
Internet available?
  |
  +-- Yes -> Configured cloud provider -> Response
  |
  +-- No or provider failure
          |
          +-- Phone local model available -> Phone Local AI
          |
          +-- Authorized desktop available -> Desktop llama.cpp AI
          |
          +-- Otherwise -> Offline Core
```

## Security principles

J.A.R.V.I.S. follows a **permission-first and trust-by-pairing** model:

1. A device is never trusted only because it is on the same LAN.
2. Unknown devices are denied by default.
3. Natural-language messages never make security decisions.
4. High-impact operations require explicit confirmation.
5. API keys and OAuth secrets remain outside client binaries and public repositories.
6. Diagnostics report `PASS` only after a real check succeeds.
7. Optional analytics remain separate from required functional consent.

## Project status

The repository currently contains the initial project description and MIT license. The broader J.A.R.V.I.S. implementation is being developed in staged components, beginning with the secure backend control-plane contracts and local-AI boundaries.

| Component | Status |
|---|---|
| Project definition and architecture | In progress |
| Backend control plane | Foundation implemented |
| JDP/1.0 protocol | Contract defined |
| Secure pairing and command safety | Foundation implemented |
| llama.cpp local-AI boundary | Service boundary implemented |
| Android application | Planned / requires Flutter and Android SDK |
| Windows desktop application | Planned / requires Flutter and Windows SDK |
| Voice and wake word | Planned / requires platform audio adapters |
| OAuth and Gmail OTP delivery | Planned / requires provider configuration |
| Production database and deployment | Planned |
| Setup wizard and installer | Planned |

## Roadmap

- [ ] Complete the production database, migrations, and session persistence.
- [ ] Add real OAuth providers and backend email OTP delivery.
- [ ] Build the Flutter Android client and Java platform integrations.
- [ ] Build the Flutter Windows client and C++ Windows bridge.
- [ ] Integrate and test llama.cpp with selected GGUF models.
- [ ] Add real LAN, mDNS, UDP, Bluetooth, and BLE discovery adapters.
- [ ] Implement voice, TTS, STT, VAD, and local wake-word adapters.
- [ ] Build the admin dashboard, Help Center, Legal Center UI, and setup wizard.
- [ ] Create signed Android, Windows, and installer release pipelines.
- [ ] Add end-to-end security, device, offline, and hardware testing.

## Getting started

### Backend foundation

```bash
git clone https://github.com/Vipul7526/jarvis.git
cd jarvis
```

The backend implementation is being maintained as a separate staged workspace while the multi-platform repository structure is finalized. When the backend directory is present, run it with:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
cp .env.example .env
python -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Configuration safety

Never commit `.env` files, API keys, OAuth client secrets, Gmail app passwords, pairing secrets, GGUF model files, or private allowlists. Use deployment environment variables or a secure secret manager.

## Repository structure

```text
jarvis/
├── README.md
├── LICENSE
├── backend/              # FastAPI control plane
├── contracts/            # JDP and shared setup contracts
├── desktop_ai/           # llama.cpp and GGUF service boundary
├── android/              # Flutter + Java Android client
├── windows/              # Flutter + C++ Windows client
├── admin/                # Administration surface
└── docs/                 # Architecture, legal, and integration documents
```

## Contributing

Contributions are welcome. Before opening a pull request, explain the change, include tests where practical, avoid adding secrets or personal data, and preserve the security boundaries around authentication, pairing, device control, and local AI. Changes that affect legal documents, protocol contracts, permissions, or destructive commands should include updated documentation and explicit review notes.

1. Fork the repository.
2. Create a focused feature branch.
3. Make the change with tests and documentation.
4. Run the relevant checks locally.
5. Open a pull request describing the security and platform impact.

## License

J.A.R.V.I.S. is distributed under the [MIT License](LICENSE). Third-party software, AI providers, GGUF models, fonts, icons, and media may have separate licenses and terms.

## Support and contact

For project questions, support, privacy questions, or security reports:

- **jarvissubsystems@gmail.com**
- **princesingh305305@gmail.com**

<div align="center">

### Build the future of personal AI.

<a href="https://github.com/Vipul7526/jarvis/issues">Report an Issue</a> ·
<a href="https://github.com/Vipul7526/jarvis/discussions">Join the Discussion</a> ·
<a href="https://github.com/Vipul7526/jarvis">View Repository</a>

</div>
