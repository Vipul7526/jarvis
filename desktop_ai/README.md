# Desktop AI

The `desktop_ai/` folder contains the Python local-AI service boundary for Windows J.A.R.V.I.S. It manages llama.cpp, GGUF model detection, localhost health, process lifecycle, and local chat requests.

## Setup

Install a compatible llama.cpp build and obtain a legally usable GGUF model. Configure `LOCAL_AI_HOST=127.0.0.1`, `LOCAL_AI_PORT=11435`, `LLAMA_CPP_EXECUTABLE`, and `LLAMA_CPP_MODEL` through the environment. Run the service with `python -m uvicorn main:app --host 127.0.0.1 --port 11435` after resolving the final manager/server port arrangement.

## Guide

The service reports executable detection, model detection, process state, HTTP health, and inference readiness separately. It must not claim `MODEL READY` until an actual inference test succeeds. Non-loopback binding is rejected by default, and model licenses remain separate from the J.A.R.V.I.S. software license.
