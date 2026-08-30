# Backend

The `backend/` folder contains the J.A.R.V.I.S. FastAPI control plane. It owns authentication decisions, legal acceptance records, secure pairing, device authorization, command-risk policies, AI routing, discovery contracts, diagnostics, and the WebSocket readiness channel.

## Setup

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
cp .env.example .env
python -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use deployment secrets for API keys, OAuth credentials, Gmail app passwords, session secrets, and approved identities. Never commit `.env`.

## Folder map

| Folder | Purpose |
|---|---|
| `app/api/` | FastAPI routes and authenticated request handling |
| `app/core/` | Strict data contracts and security primitives |
| `app/models/` | Reserved for persistent database models and migrations |
| `app/services/` | Authentication, legal, pairing, AI, discovery, and command services |
| `tests/` | Unit and API-level tests |

## Important notes

The current repositories are in-memory for the first deterministic implementation slice. Replace them with a shared database and cache before production. The API must not claim OAuth, email delivery, voice, Bluetooth, model readiness, or native platform availability until real adapters and integration tests pass.
