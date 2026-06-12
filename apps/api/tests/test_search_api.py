import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.search.router import get_search_service
from app.modules.search.schemas import (
    EntityLookupResult,
    SearchResponse,
    SearchResult,
    SearchResultType,
)


@pytest.fixture
def mock_search_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_search_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_search_service] = lambda: mock_search_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_openapi_includes_search_path(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/search" in paths
    assert "/api/v1/search/entity/{entity_type}/{entity_id}" in paths


def test_search_rejects_short_query(api_client: TestClient, mock_search_service: AsyncMock) -> None:
    from fastapi import HTTPException

    mock_search_service.search.side_effect = HTTPException(
        status_code=422,
        detail="Query must be at least 2 characters",
    )

    response = api_client.get("/api/v1/search?q=a")

    assert response.status_code == 422


def test_search_returns_results(api_client: TestClient, mock_search_service: AsyncMock) -> None:
    now = datetime.now(timezone.utc)
    entity_id = uuid.uuid4()
    mock_search_service.search.return_value = SearchResponse(
        query="sales",
        total=1,
        items=[
            SearchResult(
                id=entity_id,
                type=SearchResultType.DATA_PRODUCT,
                title="Executive Sales Dashboard",
                description="Sales reporting",
                status="active",
                secondary_status="good",
                url=f"/data-products/{entity_id}",
                updated_at=now,
            )
        ],
    )

    response = api_client.get("/api/v1/search?q=sales&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "sales"
    assert data["items"][0]["type"] == "data_product"
    mock_search_service.search.assert_awaited_once()


def test_search_with_types_filter(api_client: TestClient, mock_search_service: AsyncMock) -> None:
    mock_search_service.search.return_value = SearchResponse(query="nikita", total=0, items=[])

    response = api_client.get("/api/v1/search?q=nikita&types=person&types=team&limit=10")

    assert response.status_code == 200
    mock_search_service.search.assert_awaited_once()
    call_kwargs = mock_search_service.search.await_args.kwargs
    assert call_kwargs["types"] == [SearchResultType.PERSON, SearchResultType.TEAM]
    assert call_kwargs["limit"] == 10


def test_search_limit_max_enforced(api_client: TestClient) -> None:
    response = api_client.get("/api/v1/search?q=sales&limit=100")

    assert response.status_code == 422


def test_entity_lookup_returns_result(api_client: TestClient, mock_search_service: AsyncMock) -> None:
    entity_id = uuid.uuid4()
    mock_search_service.lookup_entity.return_value = EntityLookupResult(
        id=entity_id,
        type=SearchResultType.PERSON,
        title="Nikita Rogachev",
        description="Engineering lead",
        status="active",
        secondary_status=None,
        url=f"/people/{entity_id}",
    )

    response = api_client.get(f"/api/v1/search/entity/person/{entity_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "person"
    assert data["title"] == "Nikita Rogachev"


def test_entity_lookup_not_found(api_client: TestClient, mock_search_service: AsyncMock) -> None:
    from app.modules.search.errors import SearchEntityNotFoundError

    entity_id = uuid.uuid4()
    mock_search_service.lookup_entity.side_effect = SearchEntityNotFoundError(
        SearchResultType.PERSON,
        entity_id,
    )

    response = api_client.get(f"/api/v1/search/entity/person/{entity_id}")

    assert response.status_code == 404
