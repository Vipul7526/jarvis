# API Layer

The `api/` folder contains FastAPI HTTP and WebSocket routes. Routes validate typed request bodies, authenticate bearer sessions, enforce legal and role gates, call services, and return structured responses.

## Main route groups

- `/auth/check` evaluates a backend allowlist decision.
- `/legal/*` exposes public document history and protected acceptance status.
- `/pairing/*` starts and confirms numeric-code pairing.
- `/devices` lists authorized device records.
- `/commands` applies risk classification and confirmation requirements.
- `/ai/route` invokes the AI fallback orchestrator.
- `/diagnostics` reports actual component checks.
- `/admin/summary` requires the `ADMIN` role.
- `/ws` provides an authenticated WebSocket readiness channel.

## Guide

Keep authorization decisions in the backend services, not in client-provided natural language. Add rate limiting, request correlation, audit events, and production error handling before exposing the API publicly.
