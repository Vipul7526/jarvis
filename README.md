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

## Run the verified backend slice

```bash
cd backend
python3 -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use `backend/.env.example` as the configuration template. Real API keys, OAuth secrets, Gmail app passwords, and allowlists must be injected through deployment secrets. Do not commit `.env` files.

## Build-status discipline

The project will not mark Android permissions, Windows native integrations, voice, wake word, Bluetooth/BLE, cloud OAuth, Gmail SMTP, llama.cpp inference, or model readiness as complete until a real platform adapter or integration test has passed. The current environment does not provide Flutter/Dart, Android SDK, or Windows GUI SDK tooling, so those areas remain explicitly unimplemented rather than simulated.

## Documentation

Start with [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`contracts/JDP-1.0.md`](contracts/JDP-1.0.md), and [`contracts/SETUP_STATE_MACHINE.md`](contracts/SETUP_STATE_MACHINE.md). Legal drafts are under [`docs/legal/`](docs/legal/).
