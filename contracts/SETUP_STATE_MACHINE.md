# J.A.R.V.I.S. Setup State Machine

The setup flow is sequential, resumable, and explicit. Legal acceptance is a gate, not the end of setup. A client must not jump to the HUD because a previous UI screen was displayed; each state is backed by stored evidence or a real platform check.

## States

| State | Completion evidence |
|---|---|
| `LEGAL_ACCEPTANCE` | Explicit checkbox selection and current document versions stored for the authenticated user. |
| `PERMISSION_CENTER` | Each required permission is checked through its platform API; optional permissions may be `SKIPPED`. |
| `ACCOUNT_CONFIGURATION` | The account session is valid and the user is authorized. |
| `AI_PROVIDER_CONFIGURATION` | Each enabled provider has a backend-safe configuration status and a real connection test or an explicit disabled state. |
| `LOCAL_AI_CONFIGURATION` | Host, port, executable, model path, and resource metadata have been checked. |
| `LLAMA_CPP_CONFIGURATION` | llama.cpp executable is detected and launch/configuration validation succeeds. |
| `MODEL_CONFIGURATION` | A GGUF model is detected, selected, and passes an inference test. |
| `VOICE_CONFIGURATION` | Microphone/STT/TTS checks pass or the feature is explicitly disabled. |
| `WAKE_WORD_CONFIGURATION` | Local wake-word adapter passes a real test or the feature is explicitly disabled. |
| `DISCOVERY` | Available transports are detected without claiming unsupported transports are online. |
| `DEVICE_PAIRING` | At least one requested device is explicitly paired, or the user intentionally continues without one. |
| `THEME` | A valid theme token is stored. |
| `FONTS` | Online or bundled fallback fonts are available and loaded. |
| `HUD` | The client HUD route is available and can render its baseline state. |
| `DIAGNOSTICS` | All required checks are `PASS`, or the user has accepted clearly identified optional `SKIPPED` checks. |
| `INITIALIZATION` | The client assembles the selected services and reports their actual state. |
| `READY` | Main J.A.R.V.I.S. HUD may open. |

## Transition rule

```text
LEGAL_ACCEPTANCE -> PERMISSION_CENTER -> ACCOUNT_CONFIGURATION
-> AI_PROVIDER_CONFIGURATION -> LOCAL_AI_CONFIGURATION
-> LLAMA_CPP_CONFIGURATION -> MODEL_CONFIGURATION
-> VOICE_CONFIGURATION -> WAKE_WORD_CONFIGURATION
-> DISCOVERY -> DEVICE_PAIRING -> THEME -> FONTS -> HUD
-> DIAGNOSTICS -> INITIALIZATION -> READY
```

A failed required state remains visible with a remediation action. An unavailable platform feature is not converted into `PASS`; it is recorded as `UNKNOWN`, `FAIL`, or `SKIPPED` according to the reason and the user's choice.

## Legal acceptance behavior

The acceptance checkbox is initially false. `ACCEPT & CONTINUE` is disabled until the user selects it. On decline, normal J.A.R.V.I.S. access remains locked and the user is offered review or exit. If any legal document version changes materially, the user must review and accept the updated versions before protected access resumes.

## Diagnostic statuses

- `PASS`: a real check executed and succeeded.
- `FAIL`: a real check executed and failed.
- `SKIPPED`: an optional feature was intentionally disabled or skipped.
- `UNKNOWN`: the owning platform adapter is unavailable, so no claim is made.
