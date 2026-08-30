from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.config import Settings
from app.core.contracts import AIRequest, Identity, PairingConfirmRequest, PairingStartRequest
from app.core.security import ReplayProtector, SecurityError, SessionManager
from app.services.ai import AIOrchestrator
from app.services.auth import AllowlistService
from app.services.commands import OfflineCommandEngine
from app.services.devices import DeviceService


def settings() -> Settings:
    return Settings(
        app_name="test",
        app_env="test",
        host="127.0.0.1",
        port=8000,
        session_secret="test-secret-with-at-least-24-chars",
        session_ttl_seconds=60,
        pairing_ttl_seconds=300,
        replay_window_seconds=120,
        approved_emails=frozenset({"allowed@example.com"}),
        approved_github_users=frozenset({"approved-user"}),
        approved_microsoft_emails=frozenset(),
        approved_yahoo_emails=frozenset(),
        admin_identities=frozenset({"admin@example.com"}),
        local_ai_host="127.0.0.1",
        local_ai_port=11435,
        llama_cpp_executable=None,
        llama_cpp_model=None,
    )


def test_session_token_is_signed_and_expires() -> None:
    manager = SessionManager(settings().session_secret, ttl_seconds=10)
    token, expires = manager.issue("user-1", "APPROVED_USER", now=100)
    claims = manager.verify(token, now=105)
    assert claims.user_id == "user-1"
    assert expires == 110
    with pytest.raises(SecurityError):
        manager.verify(token + "x", now=105)
    with pytest.raises(SecurityError):
        manager.verify(token, now=110)


def test_allowlist_returns_only_a_decision() -> None:
    service = AllowlistService(settings())
    allowed = service.decide(Identity(provider="email", subject="allowed@example.com", email="allowed@example.com"))
    denied = service.decide(Identity(provider="email", subject="unknown@example.com", email="unknown@example.com"))
    assert allowed.authorized is True
    assert denied.authorized is False
    assert denied.role is None


def test_replay_protector_accepts_once() -> None:
    protector = ReplayProtector(120)
    request_id = "request-1"
    timestamp = datetime.fromtimestamp(1000, tz=timezone.utc)
    assert protector.accept(request_id, timestamp, now=1000)
    assert not protector.accept(request_id, timestamp, now=1000)
    assert not protector.accept("request-2", timestamp, now=1000 + 121)


def test_pairing_requires_the_exact_code_and_authorizes_device() -> None:
    devices = DeviceService(300)
    started = devices.start_pairing(
        PairingStartRequest(device_id="desktop-1", device_type="windows", capabilities=["text_generation"])
    )
    record = devices.confirm_pairing(
        PairingConfirmRequest(pairing_id=started.pairing_id, numeric_code=started.numeric_code, permissions=["text_generation"])
    )
    assert record.trust_state == "AUTHORIZED"
    assert devices.is_authorized("desktop-1", "text_generation")


def test_high_risk_command_requires_confirmation() -> None:
    devices = DeviceService(300)
    started = devices.start_pairing(PairingStartRequest(device_id="desktop-1", device_type="windows"))
    devices.confirm_pairing(PairingConfirmRequest(pairing_id=started.pairing_id, numeric_code=started.numeric_code))
    engine = OfflineCommandEngine(devices)
    response = engine.execute("desktop-1", "shutdown PC")
    assert response.status == "CONFIRMATION_REQUIRED"
    assert response.risk.value == "HIGH"


@pytest.mark.asyncio
async def test_orchestrator_degrades_to_offline_core() -> None:
    orchestrator = AIOrchestrator(settings())
    response = await orchestrator.route(AIRequest(prompt="hello"))
    assert response.route == "OFFLINE_CORE"
    assert response.degraded is True
