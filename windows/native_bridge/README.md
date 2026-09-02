# Windows Native Bridge

This folder contains the C++ boundary for Windows-specific capability reporting and future local-service integration. It deliberately reports local AI and device control as unavailable until real health checks and pairing authorization succeed.

## Setup

Use Visual Studio or CMake on Windows to compile the bridge. Do not ship it as an EXE by itself; it must be integrated with the Flutter desktop client and tested with the backend control plane.
