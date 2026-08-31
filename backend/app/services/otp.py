from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Protocol
from uuid import UUID, uuid4

from app.core.security import utc_now


class EmailSender(Protocol):
    def send_login_otp(self, email: str, code: str, expires_at: datetime) -> None: ...


@dataclass(frozen=True)
class OTPChallenge:
    challenge_id: UUID
    email: str
    expires_at: datetime
    attempts_remaining: int


@dataclass
class _StoredChallenge:
    email: str
    digest: str
    salt: bytes
    expires_at: datetime
    attempts_remaining: int
    used: bool = False


class OTPService:
    """One-time email OTP workflow with no plaintext OTP persistence."""

    def __init__(
        self,
        sender: EmailSender,
        ttl_seconds: int = 600,
        max_attempts: int = 5,
        resend_cooldown_seconds: int = 60,
    ) -> None:
        self._sender = sender
        self._ttl_seconds = ttl_seconds
        self._max_attempts = max_attempts
        self._resend_cooldown_seconds = resend_cooldown_seconds
        self._challenges: dict[UUID, _StoredChallenge] = {}
        self._last_issued: dict[str, datetime] = {}
        self._lock = Lock()

    def issue(self, email: str) -> OTPChallenge:
        normalized = email.strip().casefold()
        if "@" not in normalized or len(normalized) > 320:
            raise ValueError("a valid email address is required")
        now = utc_now()
        with self._lock:
            last = self._last_issued.get(normalized)
            if last and (now - last).total_seconds() < self._resend_cooldown_seconds:
                raise ValueError("resend cooldown is active")
        code = f"{secrets.randbelow(1_000_000):06d}"
        salt = secrets.token_bytes(16)
        digest = hashlib.scrypt(code.encode(), salt=salt, n=2**14, r=8, p=1).hex()
        challenge_id = uuid4()
        expires_at = now + timedelta(seconds=self._ttl_seconds)
        stored = _StoredChallenge(
            email=normalized,
            digest=digest,
            salt=salt,
            expires_at=expires_at,
            attempts_remaining=self._max_attempts,
        )
        with self._lock:
            self._challenges[challenge_id] = stored
            self._last_issued[normalized] = now
        try:
            self._sender.send_login_otp(normalized, code, expires_at)
        except Exception:
            with self._lock:
                self._challenges.pop(challenge_id, None)
            raise
        return OTPChallenge(challenge_id, normalized, expires_at, self._max_attempts)

    def verify(self, challenge_id: UUID, email: str, code: str) -> bool:
        normalized = email.strip().casefold()
        if len(code) != 6 or not code.isdecimal():
            return False
        with self._lock:
            challenge = self._challenges.get(challenge_id)
            if challenge is None or challenge.used or challenge.email != normalized:
                return False
            if utc_now() >= challenge.expires_at or challenge.attempts_remaining <= 0:
                self._challenges.pop(challenge_id, None)
                return False
            challenge.attempts_remaining -= 1
            digest = hashlib.scrypt(code.encode(), salt=challenge.salt, n=2**14, r=8, p=1).hex()
            valid = secrets.compare_digest(digest, challenge.digest)
            if valid:
                challenge.used = True
                self._challenges.pop(challenge_id, None)
            elif challenge.attempts_remaining <= 0:
                self._challenges.pop(challenge_id, None)
            return valid


class DevelopmentEmailSender:
    """Development-only sender hook; never expose captured codes in an API response."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, datetime]] = []

    def send_login_otp(self, email: str, code: str, expires_at: datetime) -> None:
        self.sent.append((email, expires_at))
        # Production must replace this with Gmail SMTP or another mail provider.
        # The code is intentionally not retained or logged here.
