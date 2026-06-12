import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.modules.search.schemas import SearchResult, SearchResultType
from app.modules.search.service import SearchService, normalize_search_limit
from app.modules.search.errors import SearchEntityNotFoundError
from app.modules.search.schemas import EntityLookupResult
from app.modules.search.urls import (
    build_compliance_check_url,
    build_data_product_url,
    build_file_url,
    build_policy_url,
    build_project_url,
    project_search_result_type,
)
from app.domain.enums import ProjectType


def test_normalize_search_limit() -> None:
    assert normalize_search_limit(100) == 50
    assert normalize_search_limit(10) == 10
    assert normalize_search_limit(0) == 20


def test_build_data_product_url() -> None:
    entity_id = uuid.uuid4()
    assert build_data_product_url(entity_id) == f"/data-products/{entity_id}"


def test_build_project_url_internal() -> None:
    entity_id = uuid.uuid4()
    assert build_project_url(entity_id, ProjectType.INTERNAL_PROJECT) == (
        f"/internal-projects/{entity_id}"
    )


def test_build_file_url() -> None:
    entity_id = uuid.uuid4()
    assert build_file_url(entity_id) == f"/files/{entity_id}"


def test_build_policy_url() -> None:
    entity_id = uuid.uuid4()
    assert build_policy_url(entity_id) == f"/compliance/policies/{entity_id}"


def test_build_compliance_check_url() -> None:
    entity_id = uuid.uuid4()
    assert build_compliance_check_url(entity_id) == f"/compliance/checks/{entity_id}"


def test_project_search_result_type_mapping() -> None:
    assert project_search_result_type(ProjectType.INTERNAL_PROJECT) == (
        SearchResultType.INTERNAL_PROJECT
    )
    assert project_search_result_type(ProjectType.CLIENT_PROJECT) == SearchResultType.PROJECT


@pytest.mark.asyncio
async def test_service_rejects_short_query() -> None:
    service = SearchService(AsyncMock())

    with pytest.raises(HTTPException) as exc_info:
        await service.search(query="a")

    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_service_calls_repository_with_normalized_query() -> None:
    now = datetime.now(timezone.utc)
    entity_id = uuid.uuid4()
    repository = AsyncMock()
    repository.search.return_value = [
        SearchResult(
            id=entity_id,
            type=SearchResultType.DATA_PRODUCT,
            title="Executive Sales Dashboard",
            description="Sales dashboard",
            status="active",
            secondary_status="good",
            url=build_data_product_url(entity_id),
            updated_at=now,
        )
    ]
    service = SearchService(repository)

    response = await service.search(query="  sales  ", limit=10)

    repository.search.assert_awaited_once_with(query="sales", types=None)
    assert response.query == "sales"
    assert response.total == 1
    assert response.items[0].title == "Executive Sales Dashboard"


@pytest.mark.asyncio
async def test_service_lookup_entity_returns_result() -> None:
    entity_id = uuid.uuid4()
    repository = AsyncMock()
    repository.lookup_entity.return_value = EntityLookupResult(
        id=entity_id,
        type=SearchResultType.PERSON,
        title="Nikita Rogachev",
        description="Engineering lead",
        status="active",
        secondary_status=None,
        url=build_data_product_url(entity_id),
    )
    service = SearchService(repository)

    result = await service.lookup_entity(SearchResultType.PERSON, entity_id)

    repository.lookup_entity.assert_awaited_once_with(SearchResultType.PERSON, entity_id)
    assert result.title == "Nikita Rogachev"


@pytest.mark.asyncio
async def test_service_lookup_entity_not_found() -> None:
    entity_id = uuid.uuid4()
    repository = AsyncMock()
    repository.lookup_entity.return_value = None
    service = SearchService(repository)

    with pytest.raises(SearchEntityNotFoundError):
        await service.lookup_entity(SearchResultType.TEAM, entity_id)
