# Python Client

This package contains a typed Python client boundary for JDP/1.0 envelopes, backend health checks, and command submission. It does not read or store API keys. Production callers must provide a secured transport with session headers, timestamps, TLS validation, and device authorization.

Run a syntax check with `python3 -m py_compile jarvis_client.py`.
