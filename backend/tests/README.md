# Backend Tests

The `tests/` folder contains unit and API-level tests for the first J.A.R.V.I.S. backend slice. Tests cover signed sessions, token expiry, allowlist decisions, replay protection, exact pairing codes, device authorization, high-risk command confirmation, offline AI fallback, health responses, and safe denial behavior.

## Run tests

```bash
cd backend
python -m pytest -q
```

Every new authentication, pairing, command, protocol, or provider change should include a regression test. Hardware, Android, Windows, Bluetooth, microphone, and real llama.cpp checks require platform-specific integration environments.
