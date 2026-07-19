from __future__ import annotations

from typing import Any


class EnvironmentError(Exception):
    code = "EnvironmentError"

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class PolicyViolation(EnvironmentError):
    code = "PolicyViolation"


class LockMismatch(EnvironmentError):
    code = "LockMismatch"


class ProfileUnsupported(EnvironmentError):
    code = "ProfileUnsupported"


class PreflightFailure(EnvironmentError):
    code = "PreflightFailure"


def to_error_payload(error: EnvironmentError) -> dict[str, Any]:
    return {
        "ok": False,
        "error": error.__class__.__name__,
        "message": str(error),
        "code": error.code,
        **error.details,
    }
