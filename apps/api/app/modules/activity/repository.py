import uuid
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import ActivityAction, ActivityEntityType
from app.models.activity import ActivityEvent
from app.modules.activity.schemas import ActivityEventCreateInternal


@dataclass
class ActivityEventListFilters:
    entity_type: ActivityEntityType | None = None
    entity_id: uuid.UUID | None = None
    action: ActivityAction | None = None
    actor_id: uuid.UUID | None = None


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query, filters: ActivityEventListFilters):
        if filters.entity_type is not None:
            query = query.where(ActivityEvent.entity_type == filters.entity_type.value)
        if filters.entity_id is not None:
            query = query.where(ActivityEvent.entity_id == filters.entity_id)
        if filters.action is not None:
            query = query.where(ActivityEvent.action == filters.action.value)
        if filters.actor_id is not None:
            query = query.where(ActivityEvent.actor_id == filters.actor_id)
        return query

    async def create(self, data: ActivityEventCreateInternal) -> ActivityEvent:
        event = ActivityEvent(
            entity_type=data.entity_type.value,
            entity_id=data.entity_id,
            action=data.action.value,
            actor_id=data.actor_id,
            title=data.title,
            description=data.description,
            details=data.details,
        )
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def list_for_entity(
        self,
        *,
        entity_type: ActivityEntityType,
        entity_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[ActivityEvent], int]:
        filters = ActivityEventListFilters(entity_type=entity_type, entity_id=entity_id)
        return await self.list(filters=filters, offset=offset, limit=limit)

    async def list(
        self,
        *,
        filters: ActivityEventListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[ActivityEvent], int]:
        base_query = select(ActivityEvent)
        base_query = self._apply_filters(base_query, filters)

        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self._session.scalar(count_query) or 0

        items_query = (
            base_query.order_by(ActivityEvent.created_at.desc()).offset(offset).limit(limit)
        )
        result = await self._session.execute(items_query)
        return list(result.scalars().all()), total
