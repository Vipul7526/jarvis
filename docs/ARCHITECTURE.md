# J.A.R.V.I.S. Architecture

**Project name:** J.A.R.V.I.S. — Just A Rather Very Intelligent System  
**Document status:** Initial implementation baseline  
**Owner:** Prince Singh  
**Support contacts:** jarvissubsystems@gmail.com; princesingh305305@gmail.com

## 1. Scope interpretation

The master prompt describes a distributed assistant ecosystem rather than a single application. The implementation is therefore organized as a monorepo with independently deployable services and client shells. The first executable slice is the secure FastAPI control plane and its protocol contracts. Android and Windows clients will consume those contracts, while the Windows local-AI service remains a separate localhost-only process.

The repository must never embed API keys, OAuth client secrets, Gmail app passwords, the complete approved-user allowlist, or private authentication data in a client binary, source bundle, discovery packet, or log. Server-side configuration is the source of truth for access control and provider credentials.

## 2. Logical components

| Component | Responsibility | Initial implementation boundary |
|---|---|---|
| Backend control plane | Authentication, legal acceptance records, device registry, pairing sessions, audit events, WebSocket gateway, health endpoints | Python/FastAPI service with typed contracts and testable service interfaces |
| AI orchestrator | Provider fallback and routing across cloud, phone-local, desktop-local, and offline core | Backend routing contract plus provider adapters; secrets stay server-side |
| Desktop local-AI service | Detect and manage llama.cpp, GGUF models, localhost server, health, streaming | Python service contract and localhost security policy; native process integration is isolated behind a manager interface |
| Discovery service | JDP/1.0 announcements, LAN/mDNS/UDP/Bluetooth/BLE capability abstraction | Typed JDP messages and transport interfaces; platform transports are client-side adapters |
| Device gateway | Commands to paired and authorized devices with risk classification and confirmation | Backend command policy and device capability contract |
| Android client | Flutter UI plus Java platform channels for permissions, voice, TTS, Bluetooth, BLE, and notifications | Client contract and integration guide; requires Flutter/Android SDK build environment |
| Windows client | Flutter UI plus native C++ bridge and Python local service | Client contract and integration guide; requires Flutter/Windows SDK and native toolchain |
| Setup wizard | Legal acceptance, permissions, account/API/local-AI/model/voice/discovery/theme/diagnostic sequence | State-machine specification and backend persistence contract |
| Admin surface | ADMIN-only user, device, security, legal, support, and health operations | Authorization contract and endpoint plan; UI can be layered on the same API |

## 3. Trust boundaries

1. **Client boundary:** Android and Windows clients are untrusted callers. They receive short-lived access tokens and capability-specific responses only.
2. **Control-plane boundary:** The backend validates identity, approved-user status, session expiry, request IDs, timestamps, replay state, permissions, and role before performing protected operations.
3. **Local-AI boundary:** llama.cpp binds to `127.0.0.1` on a configurable port. A phone never treats the desktop localhost address as its own; phone-to-desktop traffic uses an authenticated JARVIS transport.
4. **Device boundary:** LAN proximity is not trust. A device must be paired, enabled, and authorized for the requested capability.
5. **Secrets boundary:** Provider keys, OAuth secrets, Gmail SMTP credentials, and the complete allowlist exist only in backend runtime configuration or a secret manager.

## 4. AI fallback order

The orchestrator evaluates configured sources in this order: configured cloud provider, alternate configured cloud provider, phone-local model, authorized desktop-local model, and offline command engine. Each response records the selected route and a non-sensitive reason code. Provider failures are normalized and must not leak credentials or raw upstream payloads.

## 5. Setup state machine

The setup wizard is a persisted state machine. The legal checkbox is never preselected, and normal application access remains locked until the applicable legal versions are explicitly accepted. Legal acceptance transitions to the permission center rather than directly to the HUD.

```text
LEGAL_ACCEPTANCE
  -> PERMISSION_CENTER
  -> ACCOUNT_CONFIGURATION
  -> AI_PROVIDER_CONFIGURATION
  -> LOCAL_AI_CONFIGURATION
  -> LLAMA_CPP_CONFIGURATION
  -> MODEL_CONFIGURATION
  -> VOICE_CONFIGURATION
  -> WAKE_WORD_CONFIGURATION
  -> DISCOVERY
  -> DEVICE_PAIRING
  -> THEME
  -> FONTS
  -> HUD
  -> DIAGNOSTICS
  -> INITIALIZATION
  -> READY
```

Every transition is validated by the backend or the real operating-system capability check that owns it. A skipped optional feature is represented as skipped, not as passed.

## 6. Security baseline

The baseline requires OAuth state validation and PKCE where supported, redirect URI allowlisting, secure server-side sessions, expiring tokens, one-time OTPs, OTP rate limits and attempt limits, timestamp and request-ID validation, replay protection, command risk classification, explicit confirmation for high-impact actions, structured audit events, and role checks on all admin APIs.

Discovery messages are structured JDP/1.0 data. Natural-language content is never used as an authorization decision. Unknown devices receive denial responses. Pairing stores only the device identity, trust state, granted permissions, pairing time, and capabilities required for operation.

## 7. First executable delivery slice

This repository starts with the following production-oriented slice:

- Typed JDP/1.0 request, response, discovery, and pairing contracts.
- FastAPI health, authentication-session, legal-acceptance, device, pairing, command, and AI-routing endpoints.
- Backend-only configuration loading with placeholder `.env.example` values.
- Allowlist evaluation that returns only `AUTHORIZED` or `NOT_AUTHORIZED` to normal callers.
- In-memory repositories behind protocols so a production database can be added without changing API contracts.
- Deterministic offline command engine for status, calculator, and capability checks.
- Local-AI service interfaces enforcing loopback-only binding and llama.cpp manager boundaries.
- Unit tests for security-sensitive policy decisions.
- Setup and platform integration documentation.

The environment used for this initial slice does not include the Flutter/Dart SDK, Android SDK, or Windows GUI build toolchain. Those clients are represented by explicit contracts and integration boundaries rather than falsely reported as compiled or tested. A later machine with those SDKs can implement the client shells against the same contracts.

## 8. Configuration policy

Runtime settings are read from environment variables or a deployment secret store. `.env.example` contains names and non-sensitive placeholders only. Real values must be injected at deployment time. Approved identities are represented as backend configuration, hashed or normalized for lookup where appropriate, and never returned as a list to clients.

## 9. Operational diagnostics

Diagnostics expose component state as `PASS`, `FAIL`, `SKIPPED`, or `UNKNOWN`. A component is marked `PASS` only after a real check succeeds. The initial health endpoint checks process availability and configuration shape; it does not claim that llama.cpp, a model, voice hardware, Bluetooth, or an OS permission is online unless the relevant adapter performs the check.
