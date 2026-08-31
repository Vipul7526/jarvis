from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_does_not_claim_unavailable_transports() -> None:
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert all(item["available"] is False for item in body["discovery"])


def test_otp_request_is_generic_when_gmail_is_not_configured() -> None:
    response = client.post("/api/v1/auth/otp/request", json={"email": "user@example.com"})
    assert response.status_code == 200
    assert response.json()["status"] == "UNAVAILABLE"
    assert "verification code" in response.json()["message"]
    assert "GMAIL_APP_PASSWORD" not in response.text


def test_unconfigured_identity_is_denied_without_allowlist_disclosure() -> None:
    response = client.post(
        "/api/v1/auth/check",
        json={
            "provider": "email",
            "subject": "unknown@example.com",
            "email": "unknown@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "NOT_AUTHORIZED", "access_token": None, "expires_at": None, "role": None}
    assert "allowlist" not in response.text.casefold()
