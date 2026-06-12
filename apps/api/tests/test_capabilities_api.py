import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.capabilities.router import get_capability_service
from app.modules.capabilities.schemas import CapabilityListItem, CapabilityListResponse, CapabilityRead


@pytest.fixture
def mock_capability_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_capability_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_capability_service] = lambda: mock_capability_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_capability() -> CapabilityRead:
    now = datetime.now(timezone.utc)
    return CapabilityRead(
        id=uuid.uuid4(),
        name="Data Engineering",
        description="Builds and operates data pipelines, data products and platform integrations.",
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_capabilities_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/capabilities" in paths
    assert "/api/v1/capabilities/{capability_id}" in paths
    assert "/api/v1/capabilities/{capability_id}/summary" in paths


def test_list_capabilities(api_client: TestClient, mock_capability_service: AsyncMock) -> None:
    capability = _sample_capability()
    mock_capability_service.list_capabilities.return_value = CapabilityListResponse(
        items=[CapabilityListItem.model_validate(capability)],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/capabilities")

    assert response.status_code == 200
    assert response.json()["items"][0]["name"] == "Data Engineering"


def test_create_capability(api_client: TestClient, mock_capability_service: AsyncMock) -> None:
    capability = _sample_capability()
    mock_capability_service.create_capability.return_value = capability

    response = api_client.post(
        "/api/v1/capabilities",
        json={
            "name": "Data Engineering",
            "description": "Builds and operates data pipelines, data products and platform integrations.",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Data Engineering"


def test_get_capability(api_client: TestClient, mock_capability_service: AsyncMock) -> None:
    capability = _sample_capability()
    mock_capability_service.get_capability.return_value = capability

    response = api_client.get(f"/api/v1/capabilities/{capability.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(capability.id)
