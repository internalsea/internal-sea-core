from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.health import check_database_connection


def test_check_database_connection_is_importable() -> None:
    assert callable(check_database_connection)


@pytest.mark.asyncio
async def test_check_database_connection_returns_true_on_success() -> None:
    mock_connection = AsyncMock()
    mock_connection.execute = AsyncMock()

    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_connection
    mock_context.__aexit__.return_value = None

    mock_engine = AsyncMock()
    mock_engine.connect.return_value = mock_context

    with patch("app.db.health.get_engine", return_value=mock_engine):
        result = await check_database_connection()

    assert result is True
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_database_connection_returns_false_on_failure() -> None:
    with patch("app.db.health.get_engine", side_effect=RuntimeError("connection failed")):
        result = await check_database_connection()

    assert result is False


def test_db_health_endpoint_returns_ok_when_connected(
    client: TestClient,
    mock_db_available: AsyncMock,
) -> None:
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
    mock_db_available.assert_awaited_once()


def test_db_health_endpoint_returns_503_when_unavailable(
    client: TestClient,
    mock_db_unavailable: AsyncMock,
) -> None:
    response = client.get("/api/v1/health/db")
    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "unavailable"}
    mock_db_unavailable.assert_awaited_once()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_database_connection() -> None:
    result = await check_database_connection()
    assert result is True
