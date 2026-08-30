from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JDPMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocol: Literal["JDP"] = "JDP"
    version: Literal["1.0"] = "1.0"
    type: str = Field(min_length=1, max_length=80)
    request_id: UUID = Field(default_factory=uuid4)
    device_id: str = Field(min_length=1, max_length=128)
    device_type: Literal["android", "windows", "tablet", "tv", "iot", "unknown"]
    capability: str = Field(min_length=1, max_length=120)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must include timezone information")
        return value


class Identity(BaseModel):
    provider: Literal["email", "google", "microsoft", "yahoo", "github"]
    subject: str = Field(min_length=1, max_length=320)
    email: str | None = Field(default=None, max_length=320)
    username: str | None = Field(default=None, max_length=100)


class SessionResponse(BaseModel):
    status: Literal["AUTHORIZED", "NOT_AUTHORIZED"]
    access_token: str | None = None
    expires_at: datetime | None = None
    role: Literal["ADMIN", "APPROVED_USER"] | None = None


class LegalAcceptanceRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    agreement_version: str = Field(min_length=1, max_length=32)
    privacy_policy_version: str = Field(min_length=1, max_length=32)
    terms_version: str = Field(min_length=1, max_length=32)
    license_version: str = Field(min_length=1, max_length=32)
    application_version: str = Field(min_length=1, max_length=64)
    accepted: bool


class PairingStartRequest(BaseModel):
    device_id: str = Field(min_length=1, max_length=128)
    device_type: Literal["android", "windows", "tablet", "tv", "iot", "unknown"]
    capabilities: list[str] = Field(default_factory=list, max_length=50)


class PairingStartResponse(BaseModel):
    pairing_id: UUID
    device_id: str
    expires_at: datetime
    numeric_code: str


class PairingConfirmRequest(BaseModel):
    pairing_id: UUID
    numeric_code: str = Field(pattern=r"^\d{3} \d{3}$")
    permissions: list[str] = Field(default_factory=list, max_length=50)


class DeviceRecord(BaseModel):
    device_id: str
    device_type: str
    trust_state: Literal["PENDING", "AUTHORIZED", "REVOKED", "DISABLED"]
    permissions: list[str]
    capabilities: list[str]
    paired_at: datetime | None


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CommandRequest(BaseModel):
    device_id: str = Field(min_length=1, max_length=128)
    command: str = Field(min_length=1, max_length=500)
    confirmation_token: str | None = None


class CommandResponse(BaseModel):
    status: Literal["EXECUTED", "CONFIRMATION_REQUIRED", "DENIED", "UNSUPPORTED"]
    risk: RiskLevel
    message: str
    request_id: UUID = Field(default_factory=uuid4)


class AIRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)
    preferred_route: str | None = Field(default=None, max_length=50)
    device_id: str | None = Field(default=None, max_length=128)


class AIResponse(BaseModel):
    route: Literal["CLOUD", "PHONE_LOCAL", "DESKTOP_LOCAL", "OFFLINE_CORE"]
    text: str
    degraded: bool
    reason_code: str


class DiagnosticResult(BaseModel):
    component: str
    status: Literal["PASS", "FAIL", "SKIPPED", "UNKNOWN"]
    detail: str


class DiagnosticsResponse(BaseModel):
    checks: list[DiagnosticResult]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
