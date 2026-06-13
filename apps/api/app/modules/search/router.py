import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import ViewerUser
from app.dependencies import get_db
from app.modules.search.errors import SearchEntityNotFoundError
from app.modules.search.repository import SearchRepository
from app.modules.search.schemas import (
    DEFAULT_SEARCH_LIMIT,
    MAX_SEARCH_LIMIT,
    EntityLookupResult,
    SearchResponse,
    SearchResultType,
)
from app.modules.search.service import SearchService
from app.modules.tenancy.dependencies import get_current_company_id

router = APIRouter(prefix="/search", tags=["Search"])


def get_search_service(db: AsyncSession = Depends(get_db)) -> SearchService:
    return SearchService(SearchRepository(db))


@router.get("", response_model=SearchResponse)
async def global_search(
    _user: ViewerUser,
    company_id: uuid.UUID = Depends(get_current_company_id),
    q: str = Query(..., description="Search query (minimum 2 characters)"),
    types: list[SearchResultType] | None = Query(None, description="Optional entity type filters"),
    limit: int = Query(DEFAULT_SEARCH_LIMIT, ge=1, le=MAX_SEARCH_LIMIT),
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    return await service.search(query=q, types=types, limit=limit, company_id=company_id)


@router.get("/entity/{entity_type}/{entity_id}", response_model=EntityLookupResult)
async def lookup_entity(
    _user: ViewerUser,
    entity_type: SearchResultType,
    entity_id: uuid.UUID,
    service: SearchService = Depends(get_search_service),
) -> EntityLookupResult:
    try:
        return await service.lookup_entity(entity_type, entity_id)
    except SearchEntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
