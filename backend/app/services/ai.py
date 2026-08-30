from __future__ import annotations

import asyncio
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, Protocol

from app.config import Settings
from app.core.contracts import AIRequest, AIResponse


class ProviderUnavailable(RuntimeError):
    pass


class AIProvider(Protocol):
    name: str

    async def complete(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class LocalAIConfig:
    host: str
    port: int
    executable: str | None
    model: str | None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def validate(self) -> None:
        if self.host not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("local AI must bind to loopback by default")
        if not 1024 <= self.port <= 65535:
            raise ValueError("local AI port is outside the user-space range")


class LlamaCppManager:
    def __init__(self, config: LocalAIConfig) -> None:
        config.validate()
        self.config = config

    def detect_executable(self) -> str | None:
        candidate = self.config.executable
        if candidate and Path(candidate).is_file():
            return candidate
        return shutil.which("llama-server") or shutil.which("llama-cli")

    def detect_model(self) -> str | None:
        model = self.config.model
        return model if model and Path(model).is_file() else None

    def status(self) -> dict[str, str | bool | int | None]:
        return {
            "host": self.config.host,
            "port": self.config.port,
            "loopback_only": self.config.host in {"127.0.0.1", "localhost", "::1"},
            "executable_detected": bool(self.detect_executable()),
            "model_detected": bool(self.detect_model()),
            "executable": self.detect_executable(),
            "model": self.detect_model(),
        }

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        """Placeholder for the llama.cpp HTTP streaming adapter.

        The manager exposes the correct boundary without pretending that a
        model is available in this environment. A later adapter can call the
        local llama.cpp server at ``self.config.base_url``.
        """
        raise ProviderUnavailable("llama.cpp local server is not configured or running")
        yield prompt


class OfflineCore:
    async def complete(self, prompt: str) -> str:
        prompt_clean = " ".join(prompt.split())
        if not prompt_clean:
            return "I need a command or question."
        return (
            "I am operating in Offline Core mode. I can still handle configured "
            "system commands, local calculations, and device-status checks, but "
            "I cannot provide general cloud reasoning right now."
        )


class AIOrchestrator:
    def __init__(self, settings: Settings, providers: list[AIProvider] | None = None) -> None:
        self._settings = settings
        self._providers = providers or []
        self._offline = OfflineCore()
        self._local = LlamaCppManager(
            LocalAIConfig(
                host=settings.local_ai_host,
                port=settings.local_ai_port,
                executable=settings.llama_cpp_executable,
                model=settings.llama_cpp_model,
            )
        )

    async def route(self, request: AIRequest) -> AIResponse:
        if request.preferred_route == "DESKTOP_LOCAL":
            try:
                text = await _first(self._local.stream(request.prompt))
                return AIResponse(route="DESKTOP_LOCAL", text=text, degraded=False, reason_code="PREFERRED_ROUTE")
            except ProviderUnavailable:
                pass

        for provider in self._providers:
            try:
                text = await provider.complete(request.prompt)
                return AIResponse(route="CLOUD", text=text, degraded=False, reason_code=f"PROVIDER_{provider.name.upper()}")
            except Exception:
                continue

        local_status = self._local.status()
        if local_status["executable_detected"] and local_status["model_detected"]:
            try:
                text = await _first(self._local.stream(request.prompt))
                return AIResponse(route="DESKTOP_LOCAL", text=text, degraded=True, reason_code="CLOUD_UNAVAILABLE")
            except ProviderUnavailable:
                pass

        text = await self._offline.complete(request.prompt)
        return AIResponse(route="OFFLINE_CORE", text=text, degraded=True, reason_code="NO_PROVIDER_AVAILABLE")


async def _first(stream: AsyncIterator[str]) -> str:
    chunks: list[str] = []
    async for chunk in stream:
        chunks.append(chunk)
    return "".join(chunks)
