import logging
from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.config import get_settings
from app.core.errors import (
    AppError,
    ConflictError,
    NotFoundError,
    ValidationError,
    build_error_response,
)
from app.core.request_id import get_request_id
from app.modules.auth.errors import (
    AuthError,
    DuplicateUserEmailError,
    InactiveUserError,
    InsufficientPermissionsError,
    InvalidCredentialsError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)


def _json_safe_validation_errors(
    errors: Sequence[Mapping[str, Any]],
) -> list[dict[str, object]]:
    sanitized: list[dict[str, object]] = []
    for error in errors:
        item = dict(error)
        ctx = item.get("ctx")
        if isinstance(ctx, dict):
            item["ctx"] = {key: str(value) for key, value in ctx.items()}
        sanitized.append(item)
    return sanitized


def _error_response(
    request: Request,
    *,
    status_code: int,
    error: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=build_error_response(
            error=error,
            message=message,
            details=details,
            request_id=get_request_id(request),
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, dict):
            message = str(detail.get("message") or detail.get("detail") or "Request failed")
            error = str(detail.get("code") or detail.get("error") or "http_error")
            details = detail
        elif isinstance(detail, list):
            message = "Request failed"
            error = "http_error"
            details = detail
        else:
            message = str(detail)
            error = {
                status.HTTP_401_UNAUTHORIZED: "unauthorized",
                status.HTTP_403_FORBIDDEN: "forbidden",
                status.HTTP_404_NOT_FOUND: "not_found",
            }.get(exc.status_code, "http_error")
        return _error_response(
            request,
            status_code=exc.status_code,
            error=error,
            message=message,
            details=details if isinstance(detail, dict | list) else None,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error="validation_error",
            message="Request validation failed",
            details=_json_safe_validation_errors(exc.errors()),
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
        if get_settings().debug:
            logger.warning("Database integrity error", exc_info=exc)
        else:
            logger.warning("Database integrity error: %s", exc)
        return _error_response(
            request,
            status_code=status.HTTP_409_CONFLICT,
            error="conflict",
            message="Database constraint violation",
            details=None,
        )

    @app.exception_handler(NotFoundError)
    async def handle_not_found(request: Request, exc: NotFoundError) -> JSONResponse:
        return _error_response(request, status_code=404, error=exc.code, message=exc.message)

    @app.exception_handler(ConflictError)
    async def handle_conflict(request: Request, exc: ConflictError) -> JSONResponse:
        return _error_response(request, status_code=409, error=exc.code, message=exc.message)

    @app.exception_handler(ValidationError)
    async def handle_validation(request: Request, exc: ValidationError) -> JSONResponse:
        return _error_response(request, status_code=400, error=exc.code, message=exc.message)

    @app.exception_handler(InvalidCredentialsError)
    async def handle_invalid_credentials(
        request: Request,
        exc: InvalidCredentialsError,
    ) -> JSONResponse:
        return _error_response(request, status_code=401, error=exc.code, message=exc.message)

    @app.exception_handler(InactiveUserError)
    async def handle_inactive_user(request: Request, exc: InactiveUserError) -> JSONResponse:
        return _error_response(request, status_code=401, error=exc.code, message=exc.message)

    @app.exception_handler(UserNotFoundError)
    async def handle_user_not_found(request: Request, exc: UserNotFoundError) -> JSONResponse:
        return _error_response(request, status_code=404, error=exc.code, message=exc.message)

    @app.exception_handler(DuplicateUserEmailError)
    async def handle_duplicate_user(
        request: Request,
        exc: DuplicateUserEmailError,
    ) -> JSONResponse:
        return _error_response(request, status_code=409, error=exc.code, message=exc.message)

    @app.exception_handler(InsufficientPermissionsError)
    async def handle_insufficient_permissions(
        request: Request,
        exc: InsufficientPermissionsError,
    ) -> JSONResponse:
        return _error_response(request, status_code=403, error=exc.code, message=exc.message)

    @app.exception_handler(AuthError)
    async def handle_auth_error(request: Request, exc: AuthError) -> JSONResponse:
        return _error_response(request, status_code=401, error=exc.code, message=exc.message)

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return _error_response(request, status_code=400, error=exc.code, message=exc.message)

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        settings = get_settings()
        logger.exception(
            "Unhandled exception request_id=%s",
            get_request_id(request),
            exc_info=exc,
        )
        message = str(exc) if settings.debug else "Internal server error"
        details = {"type": exc.__class__.__name__} if settings.debug else None
        return _error_response(
            request,
            status_code=500,
            error="internal_error",
            message=message,
            details=details,
        )
