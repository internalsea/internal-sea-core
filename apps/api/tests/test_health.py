from unittest.mock import AsyncMock

from fastapi.testclient import TestClient


def test_root_returns_200(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Internal Sea API"
    assert data["status"] == "running"
    assert data["docs"] == "/docs"


def test_health_returns_200_and_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Internal Sea API"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "local"


def test_live_returns_200_and_live(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_ready_returns_200_when_database_connected(
    client: TestClient,
    mock_db_available: AsyncMock,
) -> None:
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "connected"}
    mock_db_available.assert_awaited_once()


def test_ready_returns_503_when_database_unavailable(
    client: TestClient,
    mock_db_unavailable: AsyncMock,
) -> None:
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "not_ready", "database": "unavailable"}
    mock_db_unavailable.assert_awaited_once()
