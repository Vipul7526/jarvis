# JARVIS Discovery Protocol — JDP/1.0

## Purpose

JDP/1.0 is the structured protocol used for discovery, capability exchange, pairing, local-AI requests, and device acknowledgements across Android, Windows, and other authorized clients. Messages are data contracts, not natural-language instructions.

## Envelope

Every message uses this envelope:

```json
{
  "protocol": "JDP",
  "version": "1.0",
  "type": "LOCAL_AI_REQUEST",
  "request_id": "uuid",
  "device_id": "device identifier",
  "device_type": "android",
  "capability": "text_generation",
  "timestamp": "2026-08-30T00:00:00Z",
  "payload": {}
}
```

| Field | Requirement |
|---|---|
| `protocol` | Must equal `JDP`. |
| `version` | Must equal `1.0` for this contract. |
| `type` | Structured message type such as `DISCOVER`, `CAPABILITIES`, `PAIR_REQUEST`, `LOCAL_AI_REQUEST`, or `LOCAL_AI_RESPONSE`. |
| `request_id` | Unique identifier used for correlation and replay protection. |
| `device_id` | Stable device identifier; never a secret. |
| `device_type` | One of the registered platform categories. |
| `capability` | Requested or advertised capability. |
| `timestamp` | Timezone-aware UTC timestamp inside the configured replay window. |
| `payload` | Type-specific fields validated by the receiver. |

## Trust rules

A receiver must reject malformed messages, unsupported versions, stale timestamps, duplicate request IDs, unknown device IDs, revoked devices, and capabilities that are not granted to the paired device. LAN presence, mDNS visibility, Bluetooth visibility, or a valid-looking natural-language message is never sufficient for authorization.

## Pairing

Pairing starts with a `PAIR_REQUEST` that creates a short-lived server-side session. The user confirms the displayed numeric code or QR payload on both devices. On success, the backend records the device identity, trust state, permissions, pairing timestamp, and capabilities. The code is never logged and is deleted after successful confirmation or expiry.

## Phone-to-desktop local AI

The phone sends a `LOCAL_AI_REQUEST` to the paired desktop transport. The desktop validates the authenticated transport and capability, then invokes its local service on loopback. The phone does not connect to the desktop's `127.0.0.1` address directly.

```text
Android client
  -> authenticated JDP transport
  -> paired Windows JARVIS
  -> localhost-only local-AI service
  -> llama.cpp
  -> GGUF model
  -> authenticated JDP response
```

## Example local-AI request

```json
{
  "protocol": "JDP",
  "version": "1.0",
  "type": "LOCAL_AI_REQUEST",
  "request_id": "0d80f431-3b29-4b3b-95d0-820d50a671b0",
  "device_id": "android-01",
  "device_type": "android",
  "capability": "text_generation",
  "timestamp": "2026-08-30T00:00:00Z",
  "payload": {
    "prompt": "Summarize my local notes.",
    "stream": true,
    "max_tokens": 512
  }
}
```

## Response types

Responses must contain the original `request_id`, a structured status, and a non-sensitive error code when unsuccessful. Raw provider secrets, OAuth tokens, OTP values, filesystem paths containing secrets, and complete allowlists are never returned in JDP payloads.
