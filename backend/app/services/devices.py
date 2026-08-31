from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from uuid import UUID, uuid4

from app.core.contracts import DeviceRecord, PairingConfirmRequest, PairingStartRequest, PairingStartResponse
from app.core.security import secret_digest, utc_now


@dataclass
class PairingSession:
    pairing_id: UUID
    device_id: str
    device_type: str
    capabilities: list[str]
    numeric_digest: str
    numeric_salt: bytes
    expires_at: datetime


class DeviceService:
    def __init__(self, pairing_ttl_seconds: int) -> None:
        self._pairings: dict[UUID, PairingSession] = {}
        self._devices: dict[str, DeviceRecord] = {}
        self._lock = Lock()
        self._pairing_ttl_seconds = pairing_ttl_seconds

    @staticmethod
    def _new_code() -> str:
        digits = f"{secrets.randbelow(1_000_000):06d}"
        return f"{digits[:3]} {digits[3:]}"

    def start_pairing(self, request: PairingStartRequest) -> PairingStartResponse:
        code = self._new_code()
        digest, salt_text = secret_digest(code)
        expires_at = utc_now() + timedelta(seconds=self._pairing_ttl_seconds)
        pairing_id = uuid4()
        session = PairingSession(
            pairing_id=pairing_id,
            device_id=request.device_id,
            device_type=request.device_type,
            capabilities=list(request.capabilities),
            numeric_digest=digest,
            numeric_salt=__import__("base64").urlsafe_b64decode(salt_text),
            expires_at=expires_at,
        )
        with self._lock:
            self._pairings[pairing_id] = session
            self._devices[request.device_id] = DeviceRecord(
                device_id=request.device_id,
                device_type=request.device_type,
                trust_state="PENDING",
                permissions=[],
                capabilities=list(request.capabilities),
                paired_at=None,
            )
        return PairingStartResponse(
            pairing_id=pairing_id,
            device_id=request.device_id,
            expires_at=expires_at,
            numeric_code=code,
        )

    def confirm_pairing(self, request: PairingConfirmRequest) -> DeviceRecord:
        with self._lock:
            session = self._pairings.get(request.pairing_id)
        if session is None or utc_now() >= session.expires_at:
            raise ValueError("pairing session expired or not found")
        digest, _ = secret_digest(request.numeric_code, session.numeric_salt)
        if not secrets.compare_digest(digest, session.numeric_digest):
            raise ValueError("invalid pairing code")
        record = DeviceRecord(
            device_id=session.device_id,
            device_type=session.device_type,
            trust_state="AUTHORIZED",
            permissions=list(request.permissions),
            capabilities=list(session.capabilities),
            paired_at=utc_now(),
        )
        with self._lock:
            self._devices[session.device_id] = record
            self._pairings.pop(request.pairing_id, None)
        return record

    def get(self, device_id: str) -> DeviceRecord | None:
        with self._lock:
            return self._devices.get(device_id)

    def list_devices(self) -> list[DeviceRecord]:
        with self._lock:
            return list(self._devices.values())

    def revoke(self, device_id: str) -> DeviceRecord:
        with self._lock:
            existing = self._devices.get(device_id)
            if existing is None:
                raise ValueError("device not found")
            revoked = existing.model_copy(update={"trust_state": "REVOKED", "permissions": []})
            self._devices[device_id] = revoked
            return revoked

    def is_authorized(self, device_id: str, permission: str | None = None) -> bool:
        record = self.get(device_id)
        if record is None or record.trust_state != "AUTHORIZED":
            return False
        return permission is None or permission in record.permissions
