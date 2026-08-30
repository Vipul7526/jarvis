from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from threading import Lock

from app.core.contracts import LegalAcceptanceRequest
from app.core.security import utc_now


@dataclass(frozen=True)
class LegalAcceptance:
    user_id: str
    agreement_version: str
    privacy_policy_version: str
    terms_version: str
    license_version: str
    accepted_at: datetime
    application_version: str


class LegalService:
    CURRENT_VERSIONS = {
        "agreement": "v1.0",
        "privacy_policy": "v1.0",
        "terms": "v1.0",
        "license": "v1.0",
    }

    def __init__(self) -> None:
        self._records: dict[str, LegalAcceptance] = {}
        self._lock = Lock()

    def accept(self, request: LegalAcceptanceRequest) -> LegalAcceptance:
        if not request.accepted:
            raise ValueError("explicit acceptance is required")
        expected = self.CURRENT_VERSIONS
        supplied = {
            "agreement": request.agreement_version,
            "privacy_policy": request.privacy_policy_version,
            "terms": request.terms_version,
            "license": request.license_version,
        }
        if supplied != expected:
            raise ValueError("one or more legal documents require review")
        record = LegalAcceptance(
            user_id=request.user_id,
            agreement_version=request.agreement_version,
            privacy_policy_version=request.privacy_policy_version,
            terms_version=request.terms_version,
            license_version=request.license_version,
            accepted_at=utc_now(),
            application_version=request.application_version,
        )
        with self._lock:
            self._records[request.user_id] = record
        return record

    def is_current(self, user_id: str) -> bool:
        with self._lock:
            record = self._records.get(user_id)
        if record is None:
            return False
        return (
            record.agreement_version == self.CURRENT_VERSIONS["agreement"]
            and record.privacy_policy_version == self.CURRENT_VERSIONS["privacy_policy"]
            and record.terms_version == self.CURRENT_VERSIONS["terms"]
            and record.license_version == self.CURRENT_VERSIONS["license"]
        )

    def history(self) -> list[dict[str, str]]:
        return [
            {
                "document": "Privacy Policy",
                "version": self.CURRENT_VERSIONS["privacy_policy"],
                "status": "Current",
            },
            {
                "document": "Terms & Conditions",
                "version": self.CURRENT_VERSIONS["terms"],
                "status": "Current",
            },
            {
                "document": "User Agreement",
                "version": self.CURRENT_VERSIONS["agreement"],
                "status": "Current",
            },
            {
                "document": "Software License",
                "version": self.CURRENT_VERSIONS["license"],
                "status": "Current",
            },
        ]
