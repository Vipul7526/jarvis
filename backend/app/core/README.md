# Core Layer

The `core/` folder defines the shared rules that should remain stable across clients and services. `contracts.py` contains strict JDP, identity, session, pairing, command, AI, and diagnostic schemas. `security.py` contains signed session tokens, expiry validation, replay protection, and secret-digest utilities.

## Guide

Changes to these contracts affect Android, Windows, desktop AI, and backend integrations. Add compatibility notes and tests whenever a field or security rule changes. Never use natural-language text as an authorization decision, and never place secrets in contract payloads.
