from __future__ import annotations

import ast
import operator
import platform
import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from app.core.contracts import CommandResponse, RiskLevel
from app.services.devices import DeviceService


@dataclass(frozen=True)
class ClassifiedCommand:
    risk: RiskLevel
    normalized: str


class OfflineCommandEngine:
    """Safe, deterministic fallback for a deliberately small command set."""

    HIGH_PATTERNS = ("shutdown", "restart", "delete file", "format", "remove all")
    MEDIUM_PATTERNS = ("volume", "media", "pause", "play", "automation", "settings")

    def __init__(self, devices: DeviceService) -> None:
        self._devices = devices

    def classify(self, command: str) -> ClassifiedCommand:
        normalized = " ".join(command.casefold().split())
        if any(pattern in normalized for pattern in self.HIGH_PATTERNS):
            return ClassifiedCommand(RiskLevel.HIGH, normalized)
        if any(pattern in normalized for pattern in self.MEDIUM_PATTERNS):
            return ClassifiedCommand(RiskLevel.MEDIUM, normalized)
        return ClassifiedCommand(RiskLevel.LOW, normalized)

    def execute(self, device_id: str, command: str, confirmation_token: str | None = None) -> CommandResponse:
        classified = self.classify(command)
        request_id = uuid4()
        if not self._devices.is_authorized(device_id):
            return CommandResponse(
                status="DENIED",
                risk=classified.risk,
                message="Device is not authorized.",
                request_id=request_id,
            )
        if classified.risk == RiskLevel.HIGH and not confirmation_token:
            return CommandResponse(
                status="CONFIRMATION_REQUIRED",
                risk=classified.risk,
                message=f"Confirmation required before executing: {classified.normalized}",
                request_id=request_id,
            )
        if classified.risk == RiskLevel.HIGH and confirmation_token != str(request_id):
            return CommandResponse(
                status="DENIED",
                risk=classified.risk,
                message="Invalid or expired confirmation token.",
                request_id=request_id,
            )

        if classified.normalized in {"system information", "show pc status", "device status"}:
            return CommandResponse(
                status="EXECUTED",
                risk=classified.risk,
                message=f"Platform: {platform.system()} {platform.release()}",
                request_id=request_id,
            )
        if classified.normalized.startswith("calculate "):
            expression = classified.normalized.removeprefix("calculate ").strip()
            try:
                result = _safe_calculate(expression)
            except ValueError:
                return CommandResponse(
                    status="UNSUPPORTED",
                    risk=classified.risk,
                    message="Only basic arithmetic expressions are supported offline.",
                    request_id=request_id,
                )
            return CommandResponse(status="EXECUTED", risk=classified.risk, message=str(result), request_id=request_id)
        if classified.normalized in {"battery status", "show battery status"}:
            return CommandResponse(
                status="UNSUPPORTED",
                risk=classified.risk,
                message="Battery status requires a platform adapter.",
                request_id=request_id,
            )
        return CommandResponse(
            status="UNSUPPORTED",
            risk=classified.risk,
            message="This command requires an enabled device adapter or AI route.",
            request_id=request_id,
        )


_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _safe_calculate(expression: str) -> int | float:
    if len(expression) > 100 or not re.fullmatch(r"[0-9+\-*/%.() ]+", expression):
        raise ValueError("unsupported expression")
    tree = ast.parse(expression, mode="eval")

    def visit(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("exponent too large")
            return _ALLOWED_BINOPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](visit(node.operand))
        raise ValueError("unsupported expression")

    return visit(tree)
