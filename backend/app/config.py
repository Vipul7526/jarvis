from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def _csv(name: str) -> frozenset[str]:
    raw = os.getenv(name, "")
    return frozenset(item.strip().casefold() for item in raw.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    host: str
    port: int
    session_secret: str
    session_ttl_seconds: int
    pairing_ttl_seconds: int
    replay_window_seconds: int
    approved_emails: frozenset[str]
    approved_github_users: frozenset[str]
    approved_microsoft_emails: frozenset[str]
    approved_yahoo_emails: frozenset[str]
    admin_identities: frozenset[str]
    local_ai_host: str
    local_ai_port: int
    llama_cpp_executable: str | None
    llama_cpp_model: str | None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "JARVIS Backend"),
        app_env=os.getenv("APP_ENV", "development"),
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        session_secret=os.getenv("SESSION_SECRET", "development-only-change-me"),
        session_ttl_seconds=int(os.getenv("SESSION_TTL_SECONDS", "1800")),
        pairing_ttl_seconds=int(os.getenv("PAIRING_TTL_SECONDS", "300")),
        replay_window_seconds=int(os.getenv("REPLAY_WINDOW_SECONDS", "120")),
        approved_emails=_csv("APPROVED_EMAILS"),
        approved_github_users=_csv("APPROVED_GITHUB_USERS"),
        approved_microsoft_emails=_csv("APPROVED_MICROSOFT_EMAILS"),
        approved_yahoo_emails=_csv("APPROVED_YAHOO_EMAILS"),
        admin_identities=_csv("ADMIN_IDENTITIES"),
        local_ai_host=os.getenv("LOCAL_AI_HOST", "127.0.0.1"),
        local_ai_port=int(os.getenv("LOCAL_AI_PORT", "11435")),
        llama_cpp_executable=os.getenv("LLAMA_CPP_EXECUTABLE") or None,
        llama_cpp_model=os.getenv("LLAMA_CPP_MODEL") or None,
    )
