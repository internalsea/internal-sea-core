import uuid

from fastapi import HTTPException, status

from app.modules.search.errors import SearchEntityNotFoundError
from app.modules.search.ranking import sort_search_results
from app.modules.search.repository import SearchRepository
from app.modules.search.schemas import (
    DEFAULT_SEARCH_LIMIT,
    EntityLookupResult,
    MAX_SEARCH_LIMIT,
    MIN_SEARCH_QUERY_LENGTH,
    SearchFilters,
    SearchResponse,
    SearchResultType,
)


def normalize_search_limit(limit: int) -> int:
    if limit < 1:
        return DEFAULT_SEARCH_LIMIT
    return min(limit, MAX_SEARCH_LIMIT)


class SearchService:
    def __init__(self, repository: SearchRepository) -> None:
        self._repository = repository

    async def search(
        self,
        *,
        query: str,
        types: list[SearchResultType] | None = None,
        limit: int = DEFAULT_SEARCH_LIMIT,
        company_id: uuid.UUID | None = None,
    ) -> SearchResponse:
        stripped_query = query.strip()
        if not stripped_query:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query must not be empty",
            )
        if len(stripped_query) < MIN_SEARCH_QUERY_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query must be at least 2 characters",
            )

        normalized_limit = normalize_search_limit(limit)
        filters = SearchFilters(q=stripped_query, types=types, limit=normalized_limit)

        results = await self._repository.search(
            query=filters.q,
            types=filters.types,
            company_id=company_id,
        )
        ranked_results = sort_search_results(filters.q, results)
        limited_results = ranked_results[: filters.limit]

        return SearchResponse(
            query=filters.q,
            total=len(limited_results),
            items=limited_results,
        )

    async def lookup_entity(
        self,
        entity_type: SearchResultType,
        entity_id: uuid.UUID,
    ) -> EntityLookupResult:
        result = await self._repository.lookup_entity(entity_type, entity_id)
        if result is None:
            raise SearchEntityNotFoundError(entity_type, entity_id)
        return result
