from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import AppContext, AuditLog, router
from app.config import get_settings
from app.core.security import ReplayProtector, SessionManager
from app.services.ai import AIOrchestrator
from app.services.auth import AllowlistService, AuthService
from app.services.commands import OfflineCommandEngine
from app.services.devices import DeviceService
from app.services.discovery import DiscoveryManager
from app.services.email import GmailSMTPEmailSender
from app.services.legal import LegalService
from app.services.otp import OTPService


def create_app() -> FastAPI:
    settings = get_settings()
    session_manager = SessionManager(settings.session_secret, settings.session_ttl_seconds)
    context = AppContext(
        auth=AuthService(AllowlistService(settings), session_manager),
        devices=DeviceService(settings.pairing_ttl_seconds),
        legal=LegalService(),
        commands=None,  # type: ignore[arg-type]
        ai=AIOrchestrator(settings),
        discovery=DiscoveryManager(),
        audit=AuditLog(),
        otp=OTPService(GmailSMTPEmailSender()),
    )
    context.commands = OfflineCommandEngine(context.devices)

    app = FastAPI(
        title="J.A.R.V.I.S. Control Plane",
        version="0.1.0",
        description="Secure control-plane foundation for the J.A.R.V.I.S. ecosystem.",
    )
    app.state.context = context
    app.state.replay_protector = ReplayProtector(settings.replay_window_seconds)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(router)
    return app


app = create_app()
