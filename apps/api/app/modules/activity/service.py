import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityEntityType
from app.modules.activity.repository import ActivityEventListFilters, ActivityRepository
from app.modules.activity.schemas import (
    ActivityEventCreateInternal,
    ActivityEventFilters,
    ActivityEventListResponse,
    ActivityEventRead,
)


class ActivityService:
    def __init__(self, repository: ActivityRepository) -> None:
        self._repository = repository

    async def record_event(self, data: ActivityEventCreateInternal) -> ActivityEventRead:
        event = await self._repository.create(data)
        return ActivityEventRead.model_validate(event)

    async def list_activity(
        self,
        *,
        filters: ActivityEventFilters,
        page: int,
        page_size: int,
    ) -> ActivityEventListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        repo_filters = ActivityEventListFilters(
            entity_type=filters.entity_type,
            entity_id=filters.entity_id,
            action=filters.action,
            actor_id=filters.actor_id,
        )
        items, total = await self._repository.list(
            filters=repo_filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return ActivityEventListResponse(
            items=[ActivityEventRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def list_entity_activity(
        self,
        entity_type: ActivityEntityType,
        entity_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> ActivityEventListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_for_entity(
            entity_type=entity_type,
            entity_id=entity_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return ActivityEventListResponse(
            items=[ActivityEventRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )
