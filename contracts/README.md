# Shared Contracts

The `contracts/` folder contains specifications shared by Android, Windows, backend, discovery, and local-AI components.

`JDP-1.0.md` defines structured discovery and device messages. `SETUP_STATE_MACHINE.md` defines the sequential setup flow from legal acceptance to the ready HUD state.

## Setup guide

Read and implement these contracts before building a client adapter. Preserve version compatibility, request IDs, timestamps, replay protection, pairing rules, and explicit permission gates. Protocol changes require coordinated client and backend tests.
