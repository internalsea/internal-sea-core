import uuid

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.domain.enums import UserRole
from app.main import create_app
from app.models.identity import User
from app.modules.auth.dependencies import require_admin, require_viewer


def test_openapi_contains_auth_endpoints(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/auth/me" in paths
    assert "/api/v1/auth/users" in paths


def test_login_validation_error(client: TestClient) -> None:
    response = client.post("/api/v1/auth/login", json={"email": "bad", "password": ""})
    assert response.status_code == 422


def test_register_validation_error(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "bad", "full_name": "", "password": "short"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_admin_dependency_allows_admin() -> None:
    admin = User(
        email="admin@example.com",
        full_name="Admin",
        role=UserRole.ADMIN,
        is_active=True,
    )
    result = await require_admin(admin)
    assert result.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_viewer_rejected_by_admin_dependency() -> None:
    from fastapi import HTTPException

    viewer = User(
        email="viewer@example.com",
        full_name="Viewer",
        role=UserRole.VIEWER,
        is_active=True,
    )
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(viewer)
    assert exc_info.value.status_code == 403


def test_inactive_user_rejected_when_auth_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTH_ENABLED", "true")
    get_settings.cache_clear()

    inactive = User(
        id=uuid.uuid4(),
        email="inactive@example.com",
        full_name="Inactive",
        role=UserRole.VIEWER,
        is_active=False,
    )

    app = create_app()

    async def override_viewer() -> User:
        return inactive

    app.dependency_overrides[require_viewer] = override_viewer
    with TestClient(app) as client:
        response = client.get("/api/v1/data-products")
        assert response.status_code == 403

    get_settings.cache_clear()
