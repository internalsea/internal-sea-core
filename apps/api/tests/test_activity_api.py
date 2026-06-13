import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import ActivityAction, ActivityEntityType
from app.main import create_app
from app.modules.activity.dependencies import get_activity_service
from app.modules.activity.schemas import ActivityEventListResponse, ActivityEventRead
from fastapi.testclient import TestClient


@pytest.fixture
def mock_activity_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_activity_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_activity_service] = lambda: mock_activity_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_openapi_includes_activity_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/activity" in paths
    assert "/api/v1/activity/{entity_type}/{entity_id}" in paths


def test_list_entity_activity(api_client: TestClient, mock_activity_service: AsyncMock) -> None:
    entity_id = uuid.uuid4()
    now = datetime.now(UTC)
    mock_activity_service.list_entity_activity.return_value = ActivityEventListResponse(
        items=[
            ActivityEventRead(
                id=uuid.uuid4(),
                entity_type=ActivityEntityType.DATA_PRODUCT,
                entity_id=entity_id,
                action=ActivityAction.CREATED,
                actor_id=None,
                title="Data product created",
                description=None,
                details=None,
                created_at=now,
            )
        ],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )
    response = api_client.get(f"/api/v1/activity/data_product/{entity_id}")
    assert response.status_code == 200
    assert response.json()["total"] == 1
