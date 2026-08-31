from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from typing import Literal

from app.core.security import utc_now

OAuthProvider = Literal["google", "microsoft", "yahoo", "github"]


@dataclass
class _OAuthState:
    provider: OAuthProvider
    redirect_uri: str
    code_challenge: str | None
    expires_at: datetime
    used: bool = False


class OAuthStateService:
    """Server-side OAuth state and redirect validation boundary."""

    def __init__(self, allowed_redirect_uris: set[str], ttl_seconds: int = 600) -> None:
        self._allowed_redirect_uris = frozenset(allowed_redirect_uris)
        self._ttl_seconds = ttl_seconds
        self._states: dict[str, _OAuthState] = {}
        self._lock = Lock()

    def create(self, provider: OAuthProvider, redirect_uri: str, code_challenge: str | None = None) -> str:
        if redirect_uri not in self._allowed_redirect_uris:
            raise ValueError("redirect URI is not allowlisted")
        state = secrets.token_urlsafe(32)
        with self._lock:
            self._states[state] = _OAuthState(
                provider=provider,
                redirect_uri=redirect_uri,
                code_challenge=code_challenge,
                expires_at=utc_now() + timedelta(seconds=self._ttl_seconds),
            )
        return state

    def consume(
        self,
        state: str,
        provider: OAuthProvider,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> str | None:
        with self._lock:
            record = self._states.get(state)
            if record is None or record.used or utc_now() >= record.expires_at:
                self._states.pop(state, None)
                return None
            if record.provider != provider or record.redirect_uri != redirect_uri:
                return None
            if record.code_challenge is not None and not code_verifier:
                return None
            record.used = True
            self._states.pop(state, None)
            return record.code_challenge
