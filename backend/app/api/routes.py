from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, WebSocket, WebSocketDisconnect, status

from app.core.contracts import (
    AIRequest,
    AIResponse,
    CommandRequest,
    CommandResponse,
    DeviceRecord,
    DiagnosticsResponse,
    DiagnosticResult,
    Identity,
    JDPMessage,
    LegalAcceptanceRequest,
    OTPRequest,
    OTPRequestResponse,
    OTPVerifyRequest,
    PairingConfirmRequest,
    PairingStartRequest,
    PairingStartResponse,
    SessionResponse,
)
from app.core.security import SecurityError, SessionClaims, utc_now
from app.services.ai import AIOrchestrator
from app.services.auth import AuthService
from app.services.commands import OfflineCommandEngine
from app.services.devices import DeviceService
from app.services.discovery import DiscoveryManager
from app.services.legal import LegalService
from app.services.otp import OTPService


@dataclass
class AuditLog:
    events: list[dict[str, str]] = field(default_factory=list)

    def record(self, event: str, subject: str) -> None:
        self.events.append({"event": event, "subject": subject, "at": utc_now().isoformat()})


@dataclass
class AppContext:
    auth: AuthService
    devices: DeviceService
    legal: LegalService
    commands: OfflineCommandEngine
    ai: AIOrchestrator
    discovery: DiscoveryManager
    audit: AuditLog
    otp: OTPService


def get_context(request: Request) -> AppContext:
    return request.app.state.context


def _claims_from_header(authorization: str | None, context: AppContext) -> SessionClaims:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer session required")
    try:
        return context.auth._sessions.verify(authorization.removeprefix("Bearer ").strip())
    except SecurityError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session") from exc


def require_session(
    context: Annotated[AppContext, Depends(get_context)],
    authorization: Annotated[str | None, Header()] = None,
) -> SessionClaims:
    return _claims_from_header(authorization, context)


def require_admin(claims: Annotated[SessionClaims, Depends(require_session)]) -> SessionClaims:
    if claims.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ADMIN authorization required")
    return claims


router = APIRouter(prefix="/api/v1")


@router.get("/healthz")
def healthz(context: Annotated[AppContext, Depends(get_context)]) -> dict[str, object]:
    return {
        "status": "ok",
        "service": "jarvis-control-plane",
        "time": utc_now().isoformat(),
        "discovery": [capability.__dict__ for capability in context.discovery.capabilities()],
    }


@router.post("/auth/otp/request", response_model=OTPRequestResponse)
def request_otp(payload: OTPRequest, context: Annotated[AppContext, Depends(get_context)]) -> OTPRequestResponse:
    # Return a generic result so this endpoint cannot be used to enumerate users.
    try:
        challenge = context.otp.issue(payload.email)
    except (ValueError, RuntimeError):
        return OTPRequestResponse(
            status="UNAVAILABLE",
            message="If the address can be used, a verification code will be sent.",
        )
    context.audit.record("OTP_REQUESTED", "redacted")
    return OTPRequestResponse(
        status="CHALLENGE_CREATED",
        challenge_id=challenge.challenge_id,
        expires_at=challenge.expires_at,
        message="If the address can be used, a verification code will be sent.",
    )


@router.post("/auth/otp/verify", response_model=SessionResponse)
def verify_otp(payload: OTPVerifyRequest, context: Annotated[AppContext, Depends(get_context)]) -> SessionResponse:
    if not context.otp.verify(payload.challenge_id, payload.email, payload.code):
        context.audit.record("OTP_DENIED", "redacted")
        return SessionResponse(status="NOT_AUTHORIZED")
    identity = Identity(provider="email", subject=payload.email, email=payload.email)
    response = context.auth.authenticate(identity)
    context.audit.record("OTP_AUTHORIZED" if response.status == "AUTHORIZED" else "OTP_NOT_AUTHORIZED", "redacted")
    return response


@router.post("/auth/check", response_model=SessionResponse)
def auth_check(identity: Identity, context: Annotated[AppContext, Depends(get_context)]) -> SessionResponse:
    response = context.auth.authenticate(identity)
    context.audit.record("AUTH_AUTHORIZED" if response.status == "AUTHORIZED" else "AUTH_DENIED", identity.subject)
    return response


@router.post("/legal/accept")
def accept_legal(
    payload: LegalAcceptanceRequest,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> dict[str, object]:
    if claims.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Cannot record acceptance for another user")
    try:
        record = context.legal.accept(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    context.audit.record("LEGAL_ACCEPTED", claims.user_id)
    return {"status": "ACCEPTED", "accepted_at": record.accepted_at, "versions": context.legal.CURRENT_VERSIONS}


@router.get("/legal/history")
def legal_history(context: Annotated[AppContext, Depends(get_context)]) -> dict[str, object]:
    return {"documents": context.legal.history()}


@router.get("/legal/status")
def legal_status(
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> dict[str, object]:
    return {"accepted": context.legal.is_current(claims.user_id), "required_versions": context.legal.CURRENT_VERSIONS}


@router.post("/pairing/start", response_model=PairingStartResponse)
def pairing_start(
    payload: PairingStartRequest,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> PairingStartResponse:
    if not context.legal.is_current(claims.user_id):
        raise HTTPException(status_code=428, detail="Legal acceptance is required before pairing")
    response = context.devices.start_pairing(payload)
    context.audit.record("PAIRING_STARTED", claims.user_id)
    return response


@router.post("/pairing/confirm", response_model=DeviceRecord)
def pairing_confirm(
    payload: PairingConfirmRequest,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> DeviceRecord:
    if not context.legal.is_current(claims.user_id):
        raise HTTPException(status_code=428, detail="Legal acceptance is required before pairing")
    try:
        record = context.devices.confirm_pairing(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    context.audit.record("PAIRING_CONFIRMED", claims.user_id)
    return record


@router.get("/devices", response_model=list[DeviceRecord])
def list_devices(
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> list[DeviceRecord]:
    return context.devices.list_devices()


@router.post("/commands", response_model=CommandResponse)
def command(
    payload: CommandRequest,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> CommandResponse:
    if not context.legal.is_current(claims.user_id):
        raise HTTPException(status_code=428, detail="Legal acceptance is required before commands")
    response = context.commands.execute(payload.device_id, payload.command, payload.confirmation_token)
    context.audit.record(f"COMMAND_{response.status}", claims.user_id)
    return response


@router.post("/ai/route", response_model=AIResponse)
async def ai_route(
    payload: AIRequest,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> AIResponse:
    if not context.legal.is_current(claims.user_id):
        raise HTTPException(status_code=428, detail="Legal acceptance is required before AI use")
    response = await context.ai.route(payload)
    context.audit.record(f"AI_ROUTE_{response.route}", claims.user_id)
    return response


@router.post("/protocol/validate", response_model=JDPMessage)
def validate_protocol(
    payload: JDPMessage,
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> JDPMessage:
    context.audit.record("JDP_VALIDATED", claims.user_id)
    return payload


@router.get("/diagnostics", response_model=DiagnosticsResponse)
def diagnostics(
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_session)],
) -> DiagnosticsResponse:
    local_status = context.ai._local.status()
    checks = [
        DiagnosticResult(component="ACCOUNT", status="PASS", detail="Authenticated session is valid."),
        DiagnosticResult(component="LEGAL", status="PASS" if context.legal.is_current(claims.user_id) else "FAIL", detail="Current agreement versions checked."),
        DiagnosticResult(component="LOCAL_AI", status="PASS" if local_status["loopback_only"] else "FAIL", detail="Loopback binding policy checked."),
        DiagnosticResult(component="LLAMA_CPP", status="PASS" if local_status["executable_detected"] else "UNKNOWN", detail="Executable detection performed."),
        DiagnosticResult(component="MODEL", status="PASS" if local_status["model_detected"] else "UNKNOWN", detail="Configured GGUF model detection performed."),
        DiagnosticResult(component="DISCOVERY", status="UNKNOWN", detail="Platform discovery adapters are not installed in this environment."),
        DiagnosticResult(component="VOICE", status="UNKNOWN", detail="Requires client microphone and speech adapters."),
        DiagnosticResult(component="WAKE_WORD", status="UNKNOWN", detail="Requires a local client wake-word adapter."),
        DiagnosticResult(component="HUD", status="UNKNOWN", detail="Requires the Flutter client shell."),
    ]
    return DiagnosticsResponse(checks=checks)


@router.get("/admin/summary")
def admin_summary(
    context: Annotated[AppContext, Depends(get_context)],
    claims: Annotated[SessionClaims, Depends(require_admin)],
) -> dict[str, object]:
    return {
        "role": claims.role,
        "devices": len(context.devices.list_devices()),
        "audit_events": len(context.audit.events),
        "legal_versions": context.legal.CURRENT_VERSIONS,
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    context: AppContext = websocket.app.state.context
    token = websocket.query_params.get("access_token")
    if not token:
        await websocket.send_json({"type": "ERROR", "detail": "access_token query parameter required"})
        await websocket.close(code=1008)
        return
    try:
        claims = context.auth._sessions.verify(token)
    except SecurityError:
        await websocket.send_json({"type": "ERROR", "detail": "Invalid or expired session"})
        await websocket.close(code=1008)
        return
    await websocket.send_json({"type": "READY", "user_id": claims.user_id})
    try:
        while True:
            message = await websocket.receive_json()
            await websocket.send_json({"type": "ACK", "request_id": message.get("request_id")})
    except WebSocketDisconnect:
        return
