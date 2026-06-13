from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.dependencies import get_db
from app.domain.enums import UserRole
from app.models.identity import User
from app.modules.auth.permissions import can_admin, can_read, can_write
from app.modules.auth.repository import AuthRepository
from app.modules.auth.security import decode_access_token

_bearer_scheme = HTTPBearer(auto_error=False)

DEV_BYPASS_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def _dev_bypass_user() -> User:
    return User(
        id=DEV_BYPASS_USER_ID,
        email="dev@local",
        full_name="Dev Bypass",
        hashed_password=None,
        role=UserRole.ADMIN,
        is_active=True,
        is_superuser=True,
    )


async def get_optional_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User | None:
    settings = get_settings()
    if not settings.auth_enabled:
        return _dev_bypass_user()
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = uuid.UUID(str(payload["sub"]))
    except (jwt.PyJWTError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc

    repository = AuthRepository(db)
    user = await repository.get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user


async def get_current_user(
    user: Annotated[User | None, Depends(get_optional_current_user)],
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


async def require_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
        )
    return user


def require_role(*roles: UserRole) -> Callable[..., Awaitable[User]]:
    async def _dependency(user: Annotated[User, Depends(require_active_user)]) -> User:
        if user.is_superuser:
            return user
        if user.role in roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return _dependency


async def require_viewer(user: Annotated[User, Depends(require_active_user)]) -> User:
    if not can_read(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user


async def require_editor(user: Annotated[User, Depends(require_active_user)]) -> User:
    if not can_write(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user


async def require_admin(user: Annotated[User, Depends(require_active_user)]) -> User:
    if not can_admin(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user
