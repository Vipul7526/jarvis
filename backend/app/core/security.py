from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from uuid import UUID


class SecurityError(ValueError):
    pass


@dataclass(frozen=True)
class SessionClaims:
    user_id: str
    role: str
    issued_at: int
    expires_at: int
    token_id: str


class SessionManager:
    """Small signed-token manager for the first slice.

    The interface is intentionally storage-agnostic. A deployed system should
    back revocation and session metadata with a shared datastore.
    """

    def __init__(self, secret: str, ttl_seconds: int) -> None:
        if len(secret) < 24:
            raise ValueError("SESSION_SECRET must be at least 24 characters")
        self._secret = secret.encode("utf-8")
        self._ttl_seconds = ttl_seconds
        self._revoked: set[str] = set()
        self._lock = Lock()

    @staticmethod
    def _encode(payload: bytes) -> str:
        return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")

    @staticmethod
    def _decode(value: str) -> bytes:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

    def issue(self, user_id: str, role: str, now: int | None = None) -> tuple[str, int]:
        issued_at = int(time.time() if now is None else now)
        expires_at = issued_at + self._ttl_seconds
        payload = {
            "sub": user_id,
            "role": role,
            "iat": issued_at,
            "exp": expires_at,
            "jti": secrets.token_urlsafe(18),
        }
        encoded_payload = self._encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
        signature = hmac.new(self._secret, encoded_payload.encode(), hashlib.sha256).digest()
        return f"{encoded_payload}.{self._encode(signature)}", expires_at

    def verify(self, token: str, now: int | None = None) -> SessionClaims:
        try:
            encoded_payload, encoded_signature = token.split(".", 1)
            expected = hmac.new(self._secret, encoded_payload.encode(), hashlib.sha256).digest()
            received = self._decode(encoded_signature)
            if not hmac.compare_digest(expected, received):
                raise SecurityError("invalid session signature")
            payload = json.loads(self._decode(encoded_payload))
            current = int(time.time() if now is None else now)
            if current >= int(payload["exp"]):
                raise SecurityError("session expired")
            token_id = str(payload["jti"])
            with self._lock:
                if token_id in self._revoked:
                    raise SecurityError("session revoked")
            return SessionClaims(
                user_id=str(payload["sub"]),
                role=str(payload["role"]),
                issued_at=int(payload["iat"]),
                expires_at=int(payload["exp"]),
                token_id=token_id,
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise SecurityError("malformed session token") from exc

    def revoke(self, token: str) -> None:
        claims = self.verify(token)
        with self._lock:
            self._revoked.add(claims.token_id)


class ReplayProtector:
    def __init__(self, window_seconds: int) -> None:
        self._window_seconds = window_seconds
        self._seen: dict[str, int] = {}
        self._lock = Lock()

    def accept(self, request_id: UUID | str, timestamp: datetime, now: int | None = None) -> bool:
        if timestamp.tzinfo is None:
            return False
        current = int(time.time() if now is None else now)
        event_time = int(timestamp.timestamp())
        if abs(current - event_time) > self._window_seconds:
            return False
        key = str(request_id)
        with self._lock:
            expired = [item for item, seen_at in self._seen.items() if current - seen_at > self._window_seconds]
            for item in expired:
                del self._seen[item]
            if key in self._seen:
                return False
            self._seen[key] = current
            return True


def secret_digest(value: str, salt: bytes | None = None) -> tuple[str, str]:
    salt_bytes = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(value.encode(), salt=salt_bytes, n=2**14, r=8, p=1).hex()
    return digest, base64.urlsafe_b64encode(salt_bytes).decode("ascii")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
