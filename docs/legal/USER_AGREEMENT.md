# J.A.R.V.I.S. User Agreement

**Version:** v1.0  
**Effective date:** 30 August 2026  
**Contact:** jarvissubsystems@gmail.com; princesingh305305@gmail.com

> This product-language draft is not legal advice. It should be reviewed before public release.

## 1. Agreement to the legal documents

By using J.A.R.V.I.S., you agree to the applicable J.A.R.V.I.S. User Agreement, Terms & Conditions, Privacy Policy, Software License, Third-Party Licenses, AI Disclaimer, and Device Control Disclaimer. You must review the current versions shown by the application and explicitly select the acceptance checkbox. The checkbox must not be selected automatically, and the application must not continue to normal protected functionality after a decline.

## 2. Software and account access

J.A.R.V.I.S. includes Android and Windows clients, a backend, a setup wizard, local-AI services, discovery, device gateway, administrative functions, and documentation. Access may be restricted to backend-approved identities. You are responsible for your account, authentication methods, sessions, API keys, paired devices, local models, and actions performed from your authorized clients.

## 3. Authentication, OAuth, and email OTP

Supported login methods may include email OTP, Google, Microsoft, Yahoo, and GitHub. Provider availability depends on configuration. Do not share OTPs or tokens. OTPs are intended to be short-lived and one-time. OAuth uses server-side validation and may use PKCE where supported; OAuth provider terms remain applicable.

## 4. Cloud, local, and offline AI

J.A.R.V.I.S. may use configured cloud providers, phone-local models, desktop-local llama.cpp models, or Offline Core functionality. Cloud requests may be processed by third-party providers. Local processing may stay on the phone or paired desktop, subject to the selected model and system configuration. Offline Core supports only the commands and information implemented locally. AI output requires verification and must not be treated as guaranteed fact.

## 5. llama.cpp and GGUF

The Windows local-AI route is designed around llama.cpp and GGUF model files. You are responsible for obtaining models from legitimate sources and complying with their licenses. Model behavior may vary by quantization, context, hardware, and configuration. The local-AI service should remain loopback-only unless you intentionally configure a secured transport.

## 6. Voice and wake word

Voice features may use microphone input, speech-to-text, text-to-speech, voice activity detection, and local wake-word processing. These features are optional where the platform permits. The permission center must explain the reason for each permission, the data involved, how to disable it, and any operating-system limitation.

## 7. Discovery, pairing, and devices

JARVIS Discovery can identify available LAN, mDNS/DNS-SD, UDP, Bluetooth, and BLE transports where supported. Visibility is not authorization. A device must be paired, trusted, enabled, and permitted for a requested capability. The phone communicates with a desktop through an authenticated JARVIS transport; it does not treat the desktop's localhost address as its own.

## 8. Commands, automation, and plugins

Commands are classified as low, medium, or high risk. Destructive or sensitive actions require explicit confirmation and may be denied. Automation and plugins must operate within granted capabilities and must not bypass security checks. You must review commands before confirming them.

## 9. Data handling and privacy

The Privacy Policy describes account, device, voice, AI, discovery, pairing, logging, diagnostic, analytics, third-party, retention, deletion, and security handling. Required functional consent must remain separate from optional analytics or personalization consent. You may keep optional analytics disabled where the application provides that choice.

## 10. Changes, suspension, and support

Features, legal documents, integrations, models, and policies may change. A materially changed legal document requires review and re-acceptance where applicable. Access may be suspended for security, unauthorized access, abuse, or violation of the applicable documents. Support and legal questions may be sent to jarvissubsystems@gmail.com or princesingh305305@gmail.com.

## First-run acceptance screen

```text
JARVIS USER AGREEMENT

Before continuing, please review:
[ VIEW PRIVACY POLICY ]
[ VIEW TERMS & CONDITIONS ]
[ VIEW USER AGREEMENT ]
[ VIEW SOFTWARE LICENSE ]
[ VIEW THIRD-PARTY LICENSES ]
[ VIEW AI DISCLAIMER ]
[ VIEW DEVICE CONTROL DISCLAIMER ]

[ ] I have read and agree to the JARVIS User Agreement,
    Terms & Conditions, Privacy Policy, and applicable licenses.

[ ACCEPT & CONTINUE ]
```

`ACCEPT & CONTINUE` remains disabled until the user selects the checkbox. If the user declines, show: “J.A.R.V.I.S. requires acceptance of the applicable agreements before the application can be used.” Offer `EXIT JARVIS` and, where appropriate, `REVIEW DOCUMENTS`.
