# J.A.R.V.I.S.

**Just A Rather Very Intelligent System**

J.A.R.V.I.S. is being built as a distributed personal-assistant ecosystem spanning Android, Windows, backend services, local AI, discovery, device control, setup, administration, and legal/operational documentation.

## Current implementation slice

The repository currently contains an executable FastAPI control-plane foundation with:

- Backend-only configuration and secret placeholders.
- Signed, expiring sessions and backend allowlist decisions.
- Versioned legal acceptance records and setup gating.
- Numeric-code device pairing with salted code digests.
- Structured JDP/1.0 contracts.
- Risk classification and confirmation gates for device commands.
- Offline Core fallback for deterministic local responses.
- Loopback-only llama.cpp/local-model manager boundary.
- Discovery transport abstractions with no false-positive availability.
- Diagnostics that report `PASS`, `FAIL`, `SKIPPED`, or `UNKNOWN` based on real checks.
- Unit tests for security-sensitive behavior.
- Legal-center drafts and platform integration contracts.

## Repository map

| Path | Purpose |
|---|---|
| `backend/` | FastAPI control plane and unit tests |
| `contracts/` | Shared JDP and setup-state specifications |
| `docs/` | Architecture and legal-center documentation |
| `desktop_ai/` | Reserved for the Windows Python local-AI service adapter |
| `android/` | Reserved for Flutter + Java client implementation |
| `windows/` | Reserved for Flutter + C++ client implementation |
| `admin/` | Reserved for the ADMIN surface |
| `portal/` | React public portal with Legal Center, Help Center, releases, and platform roadmap |
| `packaging/` | Windows, Linux, Debian, and future macOS packaging definitions |
| `.github/workflows/` | Backend, portal, source-safety, and source-release automation |

## Run the verified backend slice

```bash
cd backend
python3 -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use `backend/.env.example` as the configuration template. Real API keys, OAuth secrets, Gmail app passwords, and allowlists must be injected through deployment secrets. Do not commit `.env` files.

## Build-status discipline

The project will not mark Android permissions, Windows native integrations, voice, wake word, Bluetooth/BLE, cloud OAuth, Gmail SMTP, llama.cpp inference, or model readiness as complete until a real platform adapter or integration test has passed. The current environment does not provide Flutter/Dart, Android SDK, or Windows GUI SDK tooling, so those areas remain explicitly unimplemented rather than simulated.

## Public portal and project media

The public portal is available at [jarvisport-mehqtqf5.manus.space](https://jarvisport-mehqtqf5.manus.space). It includes the Legal Center, Help Center, release readiness board, API setup guide, and roadmap for Android, Windows, Linux, Ubuntu, Debian, Kali Linux, and macOS DMG packaging.

Project videos and updates are published through [@jarvissubsystems on YouTube](https://www.youtube.com/@jarvissubsystems).

## Documentation

Start with [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`contracts/JDP-1.0.md`](contracts/JDP-1.0.md), and [`contracts/SETUP_STATE_MACHINE.md`](contracts/SETUP_STATE_MACHINE.md). Legal drafts are under [`docs/legal/`](docs/legal/). The portal guide is in [`portal/README.md`](portal/README.md), and release definitions are in [`packaging/README.md`](packaging/README.md).
