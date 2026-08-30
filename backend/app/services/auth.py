from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.config import Settings
from app.core.contracts import Identity, SessionResponse
from app.core.security import SessionManager, utc_now


@dataclass(frozen=True)
class AuthorizationDecision:
    authorized: bool
    role: str | None


class AllowlistService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def decide(self, identity: Identity) -> AuthorizationDecision:
        subject = identity.subject.casefold().strip()
        email = (identity.email or "").casefold().strip()
        username = (identity.username or "").casefold().strip()

        authorized = False
        if email and email in self._settings.approved_emails:
            authorized = True
        elif identity.provider == "github" and username in self._settings.approved_github_users:
            authorized = True
        elif identity.provider == "microsoft" and email in self._settings.approved_microsoft_emails:
            authorized = True
        elif identity.provider == "yahoo" and email in self._settings.approved_yahoo_emails:
            authorized = True
        elif subject in self._settings.approved_emails:
            authorized = True

        if not authorized:
            return AuthorizationDecision(False, None)

        admin_keys = {item.casefold().strip() for item in self._settings.admin_identities}
        is_admin = subject in admin_keys or email in admin_keys or username in admin_keys
        return AuthorizationDecision(True, "ADMIN" if is_admin else "APPROVED_USER")


class AuthService:
    def __init__(self, allowlist: AllowlistService, sessions: SessionManager) -> None:
        self._allowlist = allowlist
        self._sessions = sessions

    def authenticate(self, identity: Identity) -> SessionResponse:
        decision = self._allowlist.decide(identity)
        if not decision.authorized or decision.role is None:
            return SessionResponse(status="NOT_AUTHORIZED")
        token, expires_at_epoch = self._sessions.issue(identity.subject, decision.role)
        expires_at = datetime.fromtimestamp(expires_at_epoch, tz=timezone.utc)
        return SessionResponse(
            status="AUTHORIZED",
            access_token=token,
            expires_at=expires_at,
            role=decision.role,
        )
