import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.models.work import WorkItem


@dataclass
class WorkItemListFilters:
    search: str | None = None
    type: WorkItemType | None = None
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    assignee_id: uuid.UUID | None = None
    data_product_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None


class WorkItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query, filters: WorkItemListFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    WorkItem.title.ilike(pattern),
                    WorkItem.description.ilike(pattern),
                )
            )
        if filters.type is not None:
            query = query.where(WorkItem.type == filters.type)
        if filters.status is not None:
            query = query.where(WorkItem.status == filters.status)
        if filters.priority is not None:
            query = query.where(WorkItem.priority == filters.priority)
        if filters.assignee_id is not None:
            query = query.where(WorkItem.assignee_id == filters.assignee_id)
        if filters.data_product_id is not None:
            query = query.where(WorkItem.data_product_id == filters.data_product_id)
        if filters.capability_id is not None:
            query = query.where(WorkItem.capability_id == filters.capability_id)
        if filters.team_id is not None:
            query = query.where(WorkItem.team_id == filters.team_id)
        if filters.project_id is not None:
            query = query.where(WorkItem.project_id == filters.project_id)
        if filters.company_id is not None:
            query = query.where(WorkItem.company_id == filters.company_id)
        return query

    async def list(
        self,
        *,
        filters: WorkItemListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[WorkItem], int]:
        base_query = select(WorkItem)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(WorkItem.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(WorkItem.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def list_for_board(
        self,
        *,
        filters: WorkItemListFilters,
        board_statuses: list[WorkItemStatus],
    ) -> list[WorkItem]:
        board_filters = WorkItemListFilters(
            search=filters.search,
            type=filters.type,
            status=filters.status,
            priority=filters.priority,
            assignee_id=filters.assignee_id,
            data_product_id=filters.data_product_id,
            capability_id=filters.capability_id,
            team_id=filters.team_id,
            project_id=filters.project_id,
            company_id=filters.company_id,
        )
        query = self._apply_filters(select(WorkItem), board_filters)
        query = query.where(WorkItem.status.in_(board_statuses))
        result = await self._session.scalars(
            query.order_by(WorkItem.updated_at.desc())
        )
        return list(result.all())

    async def get_by_id(self, work_item_id: uuid.UUID) -> WorkItem | None:
        return await self._session.get(WorkItem, work_item_id)

    async def create(self, data: dict[str, object]) -> WorkItem:
        work_item = WorkItem(**data)
        self._session.add(work_item)
        await self._session.commit()
        await self._session.refresh(work_item)
        return work_item

    async def update(self, work_item: WorkItem, data: dict[str, object]) -> WorkItem:
        for field, value in data.items():
            setattr(work_item, field, value)
        await self._session.commit()
        await self._session.refresh(work_item)
        return work_item

    async def delete(self, work_item: WorkItem) -> None:
        await self._session.delete(work_item)
        await self._session.commit()
