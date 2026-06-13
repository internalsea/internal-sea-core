import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, WorkItemStatus
from app.modules.activity.helpers import get_updated_fields
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields
from app.modules.work_items.errors import WorkItemNotFoundError
from app.modules.work_items.repository import WorkItemListFilters, WorkItemRepository
from app.modules.work_items.schemas import (
    PaginatedWorkItemList,
    WorkItemBoardColumn,
    WorkItemBoardResponse,
    WorkItemCreate,
    WorkItemRead,
    WorkItemUpdate,
)

BOARD_STATUSES = [
    WorkItemStatus.BACKLOG,
    WorkItemStatus.READY,
    WorkItemStatus.IN_PROGRESS,
    WorkItemStatus.REVIEW,
    WorkItemStatus.DONE,
]

BOARD_STATUS_TITLES: dict[WorkItemStatus, str] = {
    WorkItemStatus.BACKLOG: "Backlog",
    WorkItemStatus.READY: "Ready",
    WorkItemStatus.IN_PROGRESS: "In Progress",
    WorkItemStatus.REVIEW: "Review",
    WorkItemStatus.DONE: "Done",
}


class WorkItemService:
    def __init__(self, repository: WorkItemRepository, activity_service: ActivityService) -> None:
        self._repository = repository
        self._activity = activity_service

    async def list_work_items(
        self,
        *,
        filters: WorkItemListFilters,
        page: int,
        page_size: int,
    ) -> PaginatedWorkItemList:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_paginated(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return PaginatedWorkItemList(
            items=[WorkItemRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_work_item_board(
        self,
        *,
        filters: WorkItemListFilters,
    ) -> WorkItemBoardResponse:
        items = await self._repository.list_for_board(
            filters=filters,
            board_statuses=BOARD_STATUSES,
        )
        grouped: dict[WorkItemStatus, list[WorkItemRead]] = {
            status: [] for status in BOARD_STATUSES
        }
        for item in items:
            grouped[item.status].append(WorkItemRead.model_validate(item))

        columns = [
            WorkItemBoardColumn(
                status=status,
                title=BOARD_STATUS_TITLES[status],
                items=grouped[status],
                count=len(grouped[status]),
            )
            for status in BOARD_STATUSES
        ]
        return WorkItemBoardResponse(columns=columns)

    async def get_work_item(
        self, work_item_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> WorkItemRead:
        work_item = await self._repository.get_by_id(work_item_id)
        if work_item is None:
            raise WorkItemNotFoundError(work_item_id)
        if company_id is not None:
            ensure_company_access(work_item, company_id, label="Work item")
        return WorkItemRead.model_validate(work_item)

    async def create_work_item(
        self,
        payload: WorkItemCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> WorkItemRead:
        data = merge_tenant_fields(
            payload.model_dump(), company_id=company_id, workspace_id=workspace_id
        )
        work_item = await self._repository.create(data)
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=ActivityEntityType.WORK_ITEM,
                entity_id=work_item.id,
                action=ActivityAction.CREATED,
                title="Work item created",
            )
        )
        return WorkItemRead.model_validate(work_item)

    async def update_work_item(
        self,
        work_item_id: uuid.UUID,
        payload: WorkItemUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> WorkItemRead:
        work_item = await self._repository.get_by_id(work_item_id)
        if work_item is None:
            raise WorkItemNotFoundError(work_item_id)
        if company_id is not None:
            ensure_company_access(work_item, company_id, label="Work item")
        update_data = payload.model_dump(exclude_unset=True)
        previous_status = work_item.status
        updated = await self._repository.update(work_item, update_data)
        if update_data:
            await self._activity.record_event(
                ActivityEventCreateInternal(
                    entity_type=ActivityEntityType.WORK_ITEM,
                    entity_id=work_item_id,
                    action=ActivityAction.UPDATED,
                    title="Work item updated",
                    details={"updated_fields": get_updated_fields(update_data)},
                )
            )
            if "status" in update_data and update_data["status"] != previous_status:
                await self._activity.record_event(
                    ActivityEventCreateInternal(
                        entity_type=ActivityEntityType.WORK_ITEM,
                        entity_id=work_item_id,
                        action=ActivityAction.STATUS_CHANGED,
                        title="Work item status changed",
                        details={
                            "from_status": previous_status.value,
                            "to_status": update_data["status"].value
                            if hasattr(update_data["status"], "value")
                            else str(update_data["status"]),
                        },
                    )
                )
        return WorkItemRead.model_validate(updated)

    async def delete_work_item(
        self, work_item_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> None:
        work_item = await self._repository.get_by_id(work_item_id)
        if work_item is None:
            raise WorkItemNotFoundError(work_item_id)
        if company_id is not None:
            ensure_company_access(work_item, company_id, label="Work item")
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=ActivityEntityType.WORK_ITEM,
                entity_id=work_item_id,
                action=ActivityAction.DELETED,
                title="Work item deleted",
            )
        )
        await self._repository.delete(work_item)
