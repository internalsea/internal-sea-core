import uuid
from datetime import UTC, datetime

import pytest
from app.modules.search.schemas import (
    MAX_SEARCH_LIMIT,
    EntityLookupResult,
    SearchFilters,
    SearchResponse,
    SearchResult,
    SearchResultType,
)
from pydantic import ValidationError


def test_search_result_schema_for_each_type() -> None:
    now = datetime.now(UTC)
    base = {
        "id": uuid.uuid4(),
        "title": "Example",
        "url": "/example",
        "updated_at": now,
    }

    for result_type in SearchResultType:
        result = SearchResult(
            **base,
            type=result_type,
            description="Description",
            status="active",
            secondary_status="good",
            matched_field="name",
        )
        assert result.type == result_type


def test_search_response_schema() -> None:
    response = SearchResponse(query="sales", total=1, items=[])
    assert response.query == "sales"
    assert response.total == 1


def test_search_filters_rejects_short_query() -> None:
    with pytest.raises(ValidationError):
        SearchFilters(q="a")


def test_search_filters_strips_query() -> None:
    filters = SearchFilters(q="  sales  ")
    assert filters.q == "sales"


def test_search_filters_limit_max() -> None:
    with pytest.raises(ValidationError):
        SearchFilters(q="sales", limit=MAX_SEARCH_LIMIT + 1)


def test_file_result_type_is_accepted() -> None:
    result = SearchResult(
        id=uuid.uuid4(),
        type=SearchResultType.FILE,
        title="Spec document",
        url="/files/example",
    )
    assert result.type == SearchResultType.FILE


def test_policy_result_type_is_accepted() -> None:
    result = SearchResult(
        id=uuid.uuid4(),
        type=SearchResultType.POLICY,
        title="Governance Policy",
        url="/compliance/policies/example",
    )
    assert result.type == SearchResultType.POLICY


def test_compliance_check_result_type_is_accepted() -> None:
    result = SearchResult(
        id=uuid.uuid4(),
        type=SearchResultType.COMPLIANCE_CHECK,
        title="Ownership check",
        url="/compliance/checks/example",
    )
    assert result.type == SearchResultType.COMPLIANCE_CHECK


def test_entity_lookup_schema_works() -> None:
    entity_id = uuid.uuid4()
    lookup = EntityLookupResult(
        id=entity_id,
        type=SearchResultType.PERSON,
        title="Nikita Rogachev",
        description="Engineering lead",
        status="active",
        secondary_status="senior",
        url=f"/people/{entity_id}",
    )
    assert lookup.type == SearchResultType.PERSON
    assert lookup.title == "Nikita Rogachev"
