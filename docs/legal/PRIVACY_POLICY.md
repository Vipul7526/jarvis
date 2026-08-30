# J.A.R.V.I.S. Privacy Policy

**Version:** v1.0  
**Effective date:** 30 August 2026  
**Contact:** jarvissubsystems@gmail.com; princesingh305305@gmail.com

> This draft is a product document, not legal advice. Before public release, the project owner should have the policy reviewed for the countries and platforms in which J.A.R.V.I.S. will be offered.

## 1. Scope

This Privacy Policy explains how J.A.R.V.I.S. handles information when a person uses the J.A.R.V.I.S. Android application, Windows application, backend services, setup wizard, local-AI service, discovery features, device gateway, help center, or administrative surface.

No company, corporation, registered office, or legal entity is identified in this document because none has been supplied by the project owner. The contacts above are the supplied J.A.R.V.I.S. support and legal contacts.

## 2. Information that may be handled

Depending on the features enabled, J.A.R.V.I.S. may handle account identifiers, email addresses, OAuth provider subject identifiers, usernames, device identifiers, device types, capabilities, pairing state, granted permissions, pairing timestamps, application versions, configuration status, security events, diagnostic results, support messages, and legal acceptance records. The backend should collect only what is required for the selected feature.

Voice input, speech-recognition output, wake-word signals, AI prompts, AI responses, local automation details, and device-control requests may be processed when the user enables those features. Sensitive content should not be placed in logs by default.

## 3. Processing modes

| Mode | What happens |
|---|---|
| **Cloud processing** | A configured cloud provider may receive the prompt or other request needed to produce a response. The applicable provider's terms and privacy policy also apply. API credentials are handled by the configured backend or local secure store and are not placed in discovery packets or logs. |
| **Phone local processing** | If a local model and platform adapter are installed, the phone may process supported requests on the device. Model behavior and storage are controlled by the phone configuration. |
| **Desktop local processing** | A paired Windows desktop may process a request using a local GGUF model through llama.cpp. The desktop local-AI service should bind to loopback and the phone should communicate through authenticated J.A.R.V.I.S. transport rather than directly using the desktop's localhost address. |
| **Offline processing** | The Offline Core may handle predefined commands, calculations, cached information, and supported status checks without sending the request to a cloud provider. |

## 4. Discovery, Bluetooth, and LAN

JARVIS Discovery may inspect local network, mDNS/DNS-SD, UDP, Bluetooth, and BLE availability where the operating system and enabled feature permit it. Discovery results may contain device IDs, capability metadata, transport addresses, and protocol versions. Visibility on the same network or through Bluetooth does not itself create trust. Pairing and authorization are required before protected device operations.

## 5. Device pairing and control

Pairing records may include a device ID, trust state, granted permissions, pairing timestamp, device capabilities, and security events. Device-control commands are sent only to devices that are supported, paired, enabled, and authorized for the requested capability. High-impact operations should require explicit confirmation.

## 6. Authentication and legal records

The service may process email OTP data and OAuth identity data to authenticate an account. OTP values must be short-lived, one-time, rate-limited, attempt-limited, and never logged. OAuth state, redirect URIs, PKCE where supported, and secure sessions must be validated server-side. The backend may store the versions of the Privacy Policy, Terms & Conditions, User Agreement, and license accepted by a user, together with the acceptance time and application version.

## 7. Diagnostics, logs, and analytics

Security, pairing, authentication, command status, routing, and operational events may be recorded for security and reliability. Logs should use identifiers and reason codes rather than prompt contents, OTPs, access tokens, API keys, OAuth secrets, or the complete allowlist. Analytics are optional and must remain separate from required functional consent. If analytics are implemented, the privacy center should explain the exact data collected and provide an enable/disable choice.

## 8. Third-party services

Enabled OAuth providers, email delivery systems, cloud AI providers, model distributors, font providers, crash-reporting tools, hosting providers, and device integrations may process information under their own terms. The application should present the providers that are actually enabled rather than claiming that every integration is active.

## 9. Retention and deletion

Retention periods should be configured by the deployed service based on operational need, security requirements, legal obligations, and the user's request. A deletion workflow should remove or anonymize account records, sessions, legal acceptance records where retention is not required, paired-device records, diagnostic data, and support data where applicable. Deleting local models, logs, cached prompts, and client configuration may require separate device actions.

## 10. Security

J.A.R.V.I.S. is designed to use expiring sessions, authorization checks, secure pairing, replay protection, timestamps, request IDs, rate limits, audit events, secure credential storage, loopback-only local AI defaults, and explicit confirmation for high-impact commands. No security measure guarantees absolute security. Users should keep devices, operating systems, credentials, and model files protected.

## 11. Children and minors

J.A.R.V.I.S. is not represented as a service for children. The project owner should determine the age and consent requirements for each target market before public release. If the service becomes aware that information was collected in a manner that violates applicable requirements, it should follow an appropriate review and deletion process.

## 12. User rights and contact

Depending on applicable law, a user may have rights relating to access, correction, deletion, restriction, objection, portability, or withdrawal of optional consent. Requests should be sent to jarvissubsystems@gmail.com or princesingh305305@gmail.com with enough information to identify the request, without sending passwords, OTPs, or API keys.

## 13. Changes

A materially changed version should be published with a new version number and effective date. Where re-acceptance is required, J.A.R.V.I.S. should lock the relevant protected access until the user reviews and accepts the updated version.
