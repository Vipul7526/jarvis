from __future__ import annotations

from app.services.otp import DevelopmentEmailSender, OTPService


def test_otp_is_one_time_and_sender_does_not_retain_code() -> None:
    sender = DevelopmentEmailSender()
    service = OTPService(sender, resend_cooldown_seconds=0)
    challenge = service.issue("Prince@example.com")
    assert sender.sent[0][0] == "prince@example.com"
    assert service.verify(challenge.challenge_id, "PRINCE@example.com", "000000") is False
    assert service.verify(challenge.challenge_id, "prince@example.com", "000000") is False
    assert all(len(item) == 2 for item in sender.sent)


def test_otp_cooldown_blocks_resend() -> None:
    sender = DevelopmentEmailSender()
    service = OTPService(sender, resend_cooldown_seconds=60)
    service.issue("user@example.com")
    try:
        service.issue("USER@example.com")
    except ValueError as exc:
        assert "cooldown" in str(exc)
    else:
        raise AssertionError("expected resend cooldown")
