from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class LocalAISettings:
    host: str = os.getenv("LOCAL_AI_HOST", "127.0.0.1")
    port: int = int(os.getenv("LOCAL_AI_PORT", "11435"))
    executable: str | None = os.getenv("LLAMA_CPP_EXECUTABLE") or None
    model: str | None = os.getenv("LLAMA_CPP_MODEL") or None
    context: int = int(os.getenv("LLAMA_CPP_CONTEXT", "4096"))
    threads: int = int(os.getenv("LLAMA_CPP_THREADS", "0"))
    gpu_layers: int = int(os.getenv("LLAMA_CPP_GPU_LAYERS", "0"))

    def validate(self) -> None:
        if self.host not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("LOCAL_AI_HOST must remain loopback-only by default")
        if not 1024 <= self.port <= 65535:
            raise ValueError("LOCAL_AI_PORT must use a user-space port")
        if self.context < 256:
            raise ValueError("LLAMA_CPP_CONTEXT is too small")


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)
    max_tokens: int = Field(default=512, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0, le=2)


class ChatResponse(BaseModel):
    text: str
    model: str
    local: bool = True


class LlamaCppManager:
    def __init__(self, settings: LocalAISettings) -> None:
        settings.validate()
        self.settings = settings
        self.process: subprocess.Popen[bytes] | None = None
        self._lock = asyncio.Lock()

    def executable_path(self) -> str | None:
        if self.settings.executable and Path(self.settings.executable).is_file():
            return self.settings.executable
        return shutil.which("llama-server")

    def model_path(self) -> str | None:
        if self.settings.model and Path(self.settings.model).is_file():
            return self.settings.model
        return None

    def status(self) -> dict[str, Any]:
        process_running = self.process is not None and self.process.poll() is None
        return {
            "host": self.settings.host,
            "port": self.settings.port,
            "loopback_only": self.settings.host in {"127.0.0.1", "localhost", "::1"},
            "executable": self.executable_path(),
            "model": self.model_path(),
            "process_running": process_running,
        }

    async def start(self) -> dict[str, Any]:
        async with self._lock:
            if self.process is not None and self.process.poll() is None:
                return self.status()
            executable = self.executable_path()
            model = self.model_path()
            if not executable:
                raise RuntimeError("llama-server executable was not detected")
            if not model:
                raise RuntimeError("GGUF model was not detected")
            command = [
                executable,
                "-m",
                model,
                "--host",
                self.settings.host,
                "--port",
                str(self.settings.port),
                "-c",
                str(self.settings.context),
            ]
            if self.settings.threads > 0:
                command.extend(["-t", str(self.settings.threads)])
            command.extend(["-ngl", str(self.settings.gpu_layers)])
            self.process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return self.status()

    async def stop(self) -> None:
        async with self._lock:
            if self.process is None:
                return
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    await asyncio.to_thread(self.process.wait, 5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    await asyncio.to_thread(self.process.wait)
            self.process = None

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                response = await client.get(f"http://{self.settings.host}:{self.settings.port}/health")
                return response.is_success
        except httpx.HTTPError:
            return False

    async def complete(self, request: ChatRequest) -> str:
        if not await self.health():
            raise RuntimeError("llama.cpp server is not healthy")
        payload = {
            "messages": [{"role": "user", "content": request.prompt}],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"http://{self.settings.host}:{self.settings.port}/v1/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("llama.cpp returned an unexpected response") from exc


settings = LocalAISettings()
manager = LlamaCppManager(settings)
app = FastAPI(title="J.A.R.V.I.S. Desktop Local AI", version="0.1.0")


@app.get("/healthz")
async def healthz() -> dict[str, Any]:
    status = manager.status()
    status["server_healthy"] = await manager.health()
    return status


@app.post("/manager/start")
async def start_manager() -> dict[str, Any]:
    try:
        return await manager.start()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/manager/stop", status_code=204)
async def stop_manager() -> None:
    await manager.stop()


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        text = await manager.complete(request)
    except (RuntimeError, httpx.HTTPError) as exc:
        raise HTTPException(status_code=503, detail="Local llama.cpp service is unavailable") from exc
    return ChatResponse(text=text, model=manager.model_path() or "unknown")
