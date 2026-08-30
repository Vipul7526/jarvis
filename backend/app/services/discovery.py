from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Iterable, Protocol

from app.core.contracts import JDPMessage


class JARVISTransport(Protocol):
    name: str

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]: ...

    async def send(self, message: JDPMessage, address: str) -> None: ...


@dataclass(frozen=True)
class TransportCapability:
    name: str
    available: bool
    detail: str


class LANDiscovery:
    name = "lan"

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        return []

    async def send(self, message: JDPMessage, address: str) -> None:
        _validate_private_or_loopback(address)
        raise NotImplementedError("LAN transport adapter is platform-specific")


class MDNSDiscovery:
    name = "mdns"

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        return []

    async def send(self, message: JDPMessage, address: str) -> None:
        raise NotImplementedError("mDNS transport adapter requires a platform implementation")


class UDPDiscovery:
    name = "udp"

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        return []

    async def send(self, message: JDPMessage, address: str) -> None:
        _validate_private_or_loopback(address)
        raise NotImplementedError("UDP transport adapter is platform-specific")


class BluetoothDiscovery:
    name = "bluetooth"

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        return []

    async def send(self, message: JDPMessage, address: str) -> None:
        raise NotImplementedError("Bluetooth transport adapter requires a platform implementation")


class BLEDiscovery:
    name = "ble"

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        return []

    async def send(self, message: JDPMessage, address: str) -> None:
        raise NotImplementedError("BLE transport adapter requires a platform implementation")


class DiscoveryManager:
    def __init__(self, transports: Iterable[JARVISTransport] | None = None) -> None:
        self.transports = list(
            transports
            or [LANDiscovery(), MDNSDiscovery(), UDPDiscovery(), BluetoothDiscovery(), BLEDiscovery()]
        )

    def capabilities(self) -> list[TransportCapability]:
        return [
            TransportCapability(
                name=transport.name,
                available=False,
                detail="Platform adapter required; no false-positive availability reported.",
            )
            for transport in self.transports
        ]

    async def discover(self, timeout_seconds: float = 1.0) -> list[JDPMessage]:
        messages: list[JDPMessage] = []
        for transport in self.transports:
            try:
                messages.extend(await transport.discover(timeout_seconds))
            except (OSError, NotImplementedError):
                continue
        return messages


def _validate_private_or_loopback(address: str) -> None:
    host, _, _port = address.partition(":")
    try:
        parsed = ipaddress.ip_address(host)
    except ValueError:
        parsed = socket.gethostbyname(host)
        parsed = ipaddress.ip_address(parsed)
    if not (parsed.is_private or parsed.is_loopback or parsed.is_link_local):
        raise ValueError("discovery transport refuses public destination by default")
