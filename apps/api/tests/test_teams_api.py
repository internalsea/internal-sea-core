import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.teams.router import get_team_service
from app.modules.teams.schemas import TeamListItem, TeamListResponse, TeamRead


@pytest.fixture
def mock_team_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_team_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_team_service] = lambda: mock_team_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_team() -> TeamRead:
    now = datetime.now(timezone.utc)
    return TeamRead(
        id=uuid.uuid4(),
        name="Core Platform Team",
        description="Internal Sea product and platform team.",
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_teams_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/teams" in paths
    assert "/api/v1/teams/{team_id}" in paths
    assert "/api/v1/teams/{team_id}/summary" in paths


def test_list_teams(api_client: TestClient, mock_team_service: AsyncMock) -> None:
    team = _sample_team()
    mock_team_service.list_teams.return_value = TeamListResponse(
        items=[TeamListItem.model_validate(team)],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/teams")

    assert response.status_code == 200
    assert response.json()["items"][0]["name"] == "Core Platform Team"


def test_create_team(api_client: TestClient, mock_team_service: AsyncMock) -> None:
    team = _sample_team()
    mock_team_service.create_team.return_value = team

    response = api_client.post(
        "/api/v1/teams",
        json={
            "name": "Core Platform Team",
            "description": "Internal Sea product and platform team.",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Core Platform Team"


def test_get_team(api_client: TestClient, mock_team_service: AsyncMock) -> None:
    team = _sample_team()
    mock_team_service.get_team.return_value = team

    response = api_client.get(f"/api/v1/teams/{team.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(team.id)
