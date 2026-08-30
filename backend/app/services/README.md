# Service Layer

The `services/` folder contains business logic behind the API. It currently includes authentication and allowlist decisions, legal acceptance, device pairing, command-risk handling, AI routing, and discovery abstractions.

## Guide

Services should remain independent of HTTP so they can be reused by Android, Windows, WebSocket, CLI, and future administrative clients. Add provider adapters behind interfaces, normalize failures, redact secrets, and emit audit events for security-sensitive operations.

Before production, replace in-memory state with shared persistence and add rate limiting, observability, key rotation, and recovery behavior.
