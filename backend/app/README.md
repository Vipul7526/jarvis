# Backend Application Package

The `app/` folder is the Python application package for the J.A.R.V.I.S. control plane. It wires FastAPI routes to security, authentication, legal, device, AI, discovery, command, and diagnostic services.

## Setup

Run commands from `backend/`. The application starts with `uvicorn app.main:app --host 127.0.0.1 --port 8000`.

## Structure

- `api/` contains HTTP and WebSocket routes.
- `core/` contains strict Pydantic contracts and security primitives.
- `models/` is reserved for database models.
- `services/` contains business logic and integration boundaries.
- `config.py` loads backend-only environment configuration.
- `main.py` creates the FastAPI application context.

## Security guide

All protected routes require a valid expiring session. Admin routes require the `ADMIN` role. Legal acceptance is checked before pairing, commands, and AI use. Secrets and complete approved-user lists must never be returned to clients.
