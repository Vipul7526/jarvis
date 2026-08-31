from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from datetime import datetime


class GmailSMTPEmailSender:
    """Backend-only Gmail SMTP sender for authentication messages."""

    def __init__(self) -> None:
        self._username = os.getenv("GMAIL_USER", "").strip()
        self._app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
        self._host = os.getenv("GMAIL_SMTP_HOST", "smtp.gmail.com")
        self._port = int(os.getenv("GMAIL_SMTP_PORT", "465"))

    @property
    def configured(self) -> bool:
        return bool(self._username and self._app_password)

    def send_login_otp(self, email: str, code: str, expires_at: datetime) -> None:
        if not self.configured:
            raise RuntimeError("Gmail SMTP is not configured")
        message = EmailMessage()
        message["Subject"] = "Your J.A.R.V.I.S. verification code"
        message["From"] = self._username
        message["To"] = email
        message.set_content(
            "Your J.A.R.V.I.S. verification code is: "
            f"{code}\n\nThis code expires at {expires_at.isoformat()} UTC and can be used only once."
        )
        with smtplib.SMTP_SSL(self._host, self._port, timeout=15) as smtp:
            smtp.login(self._username, self._app_password)
            smtp.send_message(message)
