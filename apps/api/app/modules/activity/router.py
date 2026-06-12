import uuid

from fastapi import APIRouter, Depends, Query

from app.api.auth_deps import ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.domain.enums import ActivityAction, ActivityEntityType
from app.modules.activity.dependencies import get_activity_service
from app.modules.activity.schemas import ActivityEventFilters, ActivityEventListResponse
from app.modules.activity.service import ActivityService

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.get("", response_model=ActivityEventListResponse)
async def list_activity(
    _user: ViewerUser,
    entity_type: ActivityEntityType | None = None,
    entity_id: uuid.UUID | None = None,
    action: ActivityAction | None = None,
    actor_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ActivityService = Depends(get_activity_service),
) -> ActivityEventListResponse:
    filters = ActivityEventFilters(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_id=actor_id,
    )
    return await service.list_activity(filters=filters, page=page, page_size=page_size)


@router.get("/{entity_type}/{entity_id}", response_model=ActivityEventListResponse)
async def list_entity_activity(
    entity_type: ActivityEntityType,
    entity_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ActivityService = Depends(get_activity_service),
) -> ActivityEventListResponse:
    return await service.list_entity_activity(
        entity_type,
        entity_id,
        page=page,
        page_size=page_size,
    )
