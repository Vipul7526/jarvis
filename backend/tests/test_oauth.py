from __future__ import annotations

import pytest

from app.services.oauth import OAuthStateService


def test_oauth_state_requires_allowlisted_redirect_and_is_one_time() -> None:
    service = OAuthStateService({"https://example.com/callback"})
    with pytest.raises(ValueError):
        service.create("google", "https://attacker.example/callback")
    state = service.create("google", "https://example.com/callback", code_challenge="challenge")
    assert service.consume(state, "google", "https://example.com/callback") is None
    assert service.consume(state, "google", "https://example.com/callback", code_verifier="verifier") == "challenge"
    assert service.consume(state, "google", "https://example.com/callback", code_verifier="verifier") is None


def test_oauth_state_cannot_be_consumed_for_another_provider() -> None:
    service = OAuthStateService({"https://example.com/callback"})
    state = service.create("github", "https://example.com/callback")
    assert service.consume(state, "google", "https://example.com/callback") is None
    assert service.consume(state, "github", "https://example.com/callback") is None
