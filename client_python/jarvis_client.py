"""Small Python client boundary for J.A.R.V.I.S. control-plane calls.

This module intentionally does not store credentials. Callers supply an already
secured transport/session implementation and can use the same envelope shape as
Dart, Java, C++, and Swift clients.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol
from uuid import uuid4


class Transport(Protocol):
    def request(self, method: str, path: str, payload: Mapping[str, Any] | None = None) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class JdpEnvelope:
    message_type: str
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    target: str | None = None
    requires_confirmation: bool = False
    protocol: str = "JDP/1.0"
    message_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "protocol": self.protocol,
            "message_id": self.message_id,
            "message_type": self.message_type,
            "created_at": self.created_at,
            "source": self.source,
            "requires_confirmation": self.requires_confirmation,
            "payload": dict(self.payload),
        }
        if self.target:
            value["target"] = self.target
        return value


class JarvisClient:
    def __init__(self, transport: Transport, source: str) -> None:
        self.transport = transport
        self.source = source

    def health(self) -> Mapping[str, Any]:
        return self.transport.request("GET", "/health")

    def command(self, text: str, device_id: str, *, confirmation: bool = False) -> Mapping[str, Any]:
        envelope = JdpEnvelope(
            message_type="command",
            source=self.source,
            target=device_id,
            requires_confirmation=confirmation,
            payload={"command": text, "device_id": device_id},
        )
        return self.transport.request("POST", "/commands", envelope.as_dict())
