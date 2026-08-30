# J.A.R.V.I.S. Terms & Conditions

**Version:** v1.0  
**Effective date:** 30 August 2026  
**Contact:** jarvissubsystems@gmail.com; princesingh305305@gmail.com

> This draft is for product implementation and review. It is not legal advice and should be reviewed for the target jurisdictions before public release.

## 1. Eligibility and account access

You may use J.A.R.V.I.S. only where you are legally permitted to do so and where you can comply with these Terms. Access may be restricted to identities approved by the J.A.R.V.I.S. backend. A client receives only an authorization result; it must not receive the complete allowlist.

You are responsible for protecting your account, sessions, connected devices, API keys, pairing codes, and local model files. Do not share OTPs, tokens, pairing codes, OAuth secrets, or administrative credentials.

## 2. Authentication

J.A.R.V.I.S. may support email OTP, Google, Microsoft, Yahoo, and GitHub login. Availability depends on configuration. OAuth state, redirect URI, PKCE where supported, server-side token handling, session expiry, and provider requirements apply. An OAuth provider's own terms also apply to the provider interaction.

## 3. AI services

J.A.R.V.I.S. may route requests to configured cloud AI providers, a phone-local model, a paired desktop-local model, or an Offline Core. Cloud providers may process prompts and responses under their own terms. Local and offline routes may have different capabilities, quality, latency, and data-handling behavior. AI output can be inaccurate, incomplete, unsafe, or unsuitable for a particular decision; verify important information with appropriate authoritative sources.

## 4. API keys and credentials

A user may configure provider credentials where the deployment supports it. Credentials must remain in an approved secure store and must not be embedded in an APK, EXE, Flutter bundle, Java source, C++ source, public repository, discovery packet, or log. The project does not promise that a provider connection will remain available.

## 5. Local AI, llama.cpp, and GGUF models

The Windows local-AI service is designed to use llama.cpp and GGUF model files. Model licenses, terms, safety characteristics, and distribution restrictions remain the responsibility of the model author and the user. J.A.R.V.I.S. does not claim ownership of third-party inference software or model files. The local service should bind to loopback by default and should not be exposed publicly without an intentional, secured deployment decision.

## 6. Discovery, pairing, and device control

JARVIS Discovery may use LAN, mDNS/DNS-SD, UDP, Bluetooth, or BLE where supported. Discovery is not trust. Devices must be explicitly paired and authorized, and permissions must be checked for every protected operation. Device control is limited by operating-system permissions, device capabilities, network conditions, third-party APIs, and safety policies. High-impact actions such as shutdown, restart, deletion, or sensitive system operations require explicit confirmation and may remain unsupported.

## 7. Automation and plugins

Automation and plugins may receive capabilities only when the user enables them and the backend permits them. A plugin must not bypass authentication, authorization, permission checks, confirmation requirements, rate limits, or audit logging. Untrusted plugins should be isolated before they are allowed to control devices, access files, or transmit data.

## 8. Acceptable and prohibited use

You must not use J.A.R.V.I.S. to access devices without authorization, evade operating-system security, distribute malware, steal credentials, conduct unlawful surveillance, harm another person, bypass provider limits, or execute destructive operations without the required confirmation and authority. You must comply with applicable law and with the terms of connected third-party services.

## 9. Updates and availability

J.A.R.V.I.S. may change, update, disable, or remove features, models, transports, integrations, and support content. Service availability depends on the backend, cloud providers, Internet access, local hardware, operating-system behavior, and paired devices. No uptime or uninterrupted operation is promised by this draft.

## 10. Disclaimers and liability

J.A.R.V.I.S. is provided subject to applicable law and without promises that AI responses, device commands, discovery results, local inference, or automations will always be accurate, available, secure, or suitable for a specific purpose. To the extent permitted by applicable law, the project owner is not responsible for losses caused by misuse, unsupported devices, incorrect commands, third-party services, unavailable networks, model behavior, or failure to follow warnings and confirmation prompts. These statements must be adapted by legal counsel for the target jurisdiction.

## 11. Suspension and termination

Access may be suspended or terminated for security reasons, unauthorized access, abuse, violation of these Terms, or operational necessity. The user may stop using J.A.R.V.I.S. and remove client applications, local models, paired devices, and credentials. Account and legal-record deletion should follow the applicable Privacy Policy and legitimate record-keeping requirements.

## 12. Changes and contact

A material change should receive a new version number and effective date. When re-acceptance is required, normal protected access may remain locked until the updated document is reviewed and accepted. Questions may be sent to jarvissubsystems@gmail.com or princesingh305305@gmail.com.
