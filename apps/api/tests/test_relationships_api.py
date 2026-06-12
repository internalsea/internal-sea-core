import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.enums import EntityLinkType, EntityType
from app.main import create_app
from app.modules.relationships.router import get_relationship_service
from app.modules.relationships.schemas import EntityLinkListResponse, EntityLinkRead, EntityRelationshipView


@pytest.fixture
def mock_relationship_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_relationship_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_relationship_service] = lambda: mock_relationship_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_link() -> EntityLinkRead:
    now = datetime.now(timezone.utc)
    return EntityLinkRead(
        id=uuid.uuid4(),
        source_type=EntityType.DATA_PRODUCT,
        source_id=uuid.uuid4(),
        target_type=EntityType.WORK_ITEM,
        target_id=uuid.uuid4(),
        link_type=EntityLinkType.IMPROVES,
        title="Improves documentation",
        description=None,
        created_by_id=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_relationships_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/relationships" in paths
    assert "/api/v1/relationships/{link_id}" in paths
    assert "/api/v1/relationships/entity/{entity_type}/{entity_id}" in paths


def test_get_entity_relationships(api_client: TestClient, mock_relationship_service: AsyncMock) -> None:
    entity_id = uuid.uuid4()
    link = _sample_link()
    mock_relationship_service.get_relationship_view.return_value = EntityRelationshipView(
        entity_type=EntityType.DATA_PRODUCT,
        entity_id=entity_id,
        outgoing=[link],
        incoming=[],
        total=1,
    )
    response = api_client.get(f"/api/v1/relationships/entity/data_product/{entity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["outgoing"]) == 1


def test_list_relationships(api_client: TestClient, mock_relationship_service: AsyncMock) -> None:
    link = _sample_link()
    mock_relationship_service.list_links.return_value = EntityLinkListResponse(
        items=[link],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )
    response = api_client.get("/api/v1/relationships")
    assert response.status_code == 200
    assert response.json()["total"] == 1
