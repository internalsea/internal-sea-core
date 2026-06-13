from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
from app.config import get_settings
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def disable_auth_for_unit_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Existing API tests assume open access unless auth is explicitly enabled."""
    monkeypatch.setenv("AUTH_ENABLED", "false")
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def mock_database_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default tests assume database is reachable without a live Postgres instance."""

    async def _connected() -> bool:
        return True

    monkeypatch.setattr(
        "app.api.v1.endpoints.health.check_database_connection",
        _connected,
    )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_db_unavailable(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock(return_value=False)
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", mock)
    return mock


@pytest.fixture
def mock_db_available(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", mock)
    return mock
