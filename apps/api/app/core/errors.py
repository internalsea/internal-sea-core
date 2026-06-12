from typing import Any

from pydantic import BaseModel


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, *, code: str = "app_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, code="not_found")


class ValidationError(AppError):
    """Raised when business validation fails."""

    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message, code="validation_error")


class ConflictError(AppError):
    """Raised when an operation conflicts with existing data."""

    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, code="conflict")


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: str
    message: str
    details: Any | None = None
    request_id: str | None = None


def build_error_response(
    *,
    error: str,
    message: str,
    details: Any | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build error JSON with standard and legacy fields for clients."""
    body = ErrorResponse(
        error=error,
        message=message,
        details=details,
        request_id=request_id,
    ).model_dump()
    # Legacy fields kept for backward compatibility during client migration.
    body["detail"] = message
    body["code"] = error
    return body
