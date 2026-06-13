from unittest.mock import AsyncMock, MagicMock
import uuid

import pytest

from app.domain.enums import UserRole
from app.models.identity import User
from app.modules.auth.errors import InvalidCredentialsError
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.auth.security import hash_password
from app.modules.auth.service import AuthService


@pytest.mark.asyncio
async def test_authenticate_user_rejects_invalid_password() -> None:
    user = User(
        email="user@example.com",
        full_name="User",
        hashed_password=hash_password("correct12345"),
        role=UserRole.EDITOR,
        is_active=True,
    )
    repository = AsyncMock()
    repository.get_user_by_email.return_value = user
    service = AuthService(repository, AsyncMock())

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate_user("user@example.com", "wrong12345")


@pytest.mark.asyncio
async def test_login_returns_token_response() -> None:
    user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        full_name="Admin",
        hashed_password=hash_password("admin12345"),
        role=UserRole.ADMIN,
        is_active=True,
        is_superuser=True,
    )
    repository = AsyncMock()
    repository.get_user_by_email.return_value = user
    repository.update_last_login.return_value = user
    session = AsyncMock()
    service = AuthService(repository, session)

    response = await service.login(LoginRequest(email="admin@example.com", password="admin12345"))
    assert response.access_token
    assert response.token_type == "bearer"
    assert response.user.email == "admin@example.com"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_returns_token_response() -> None:
    user = User(
        id=uuid.uuid4(),
        email="new@example.com",
        full_name="New User",
        hashed_password=hash_password("secret12345"),
        role=UserRole.VIEWER,
        is_active=True,
        is_superuser=False,
    )
    repository = AsyncMock()
    repository.get_user_by_email.return_value = None
    repository.create_user.return_value = user
    session = AsyncMock()
    service = AuthService(repository, session)

    response = await service.register(
        RegisterRequest(email="new@example.com", full_name="New User", password="secret12345")
    )
    assert response.access_token
    assert response.user.email == "new@example.com"
    assert response.user.role == UserRole.VIEWER
    session.commit.assert_awaited_once()
