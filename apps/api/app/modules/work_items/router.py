import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.modules.work_items.repository import WorkItemListFilters, WorkItemRepository
from app.modules.work_items.schemas import (
    PaginatedWorkItemList,
    WorkItemBoardResponse,
    WorkItemCreate,
    WorkItemRead,
    WorkItemUpdate,
)
from app.modules.activity.dependencies import build_activity_service
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant
from app.modules.work_items.service import WorkItemService

router = APIRouter(prefix="/work-items", tags=["Work"])


def get_work_item_service(db: AsyncSession = Depends(get_db)) -> WorkItemService:
    return WorkItemService(WorkItemRepository(db), build_activity_service(db))


def _build_filters(
    *,
    search: str | None = None,
    type: WorkItemType | None = None,
    status: WorkItemStatus | None = None,
    priority: WorkItemPriority | None = None,
    assignee_id: uuid.UUID | None = None,
    data_product_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    team_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
    company_id: uuid.UUID | None = None,
) -> WorkItemListFilters:
    return WorkItemListFilters(
        search=search,
        type=type,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        data_product_id=data_product_id,
        capability_id=capability_id,
        team_id=team_id,
        project_id=project_id,
        company_id=company_id,
    )


@router.get("", response_model=PaginatedWorkItemList)
async def list_work_items(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    type: WorkItemType | None = None,
    status: WorkItemStatus | None = None,
    priority: WorkItemPriority | None = None,
    assignee_id: uuid.UUID | None = None,
    data_product_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    team_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: WorkItemService = Depends(get_work_item_service),
) -> PaginatedWorkItemList:
    filters = _build_filters(
        search=search,
        type=type,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        data_product_id=data_product_id,
        capability_id=capability_id,
        team_id=team_id,
        project_id=project_id,
        company_id=tenant.company_id,
    )
    return await service.list_work_items(
        filters=filters,
        page=page,
        page_size=page_size,
    )


@router.get("/board", response_model=WorkItemBoardResponse)
async def get_work_item_board(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    type: WorkItemType | None = None,
    status: WorkItemStatus | None = None,
    priority: WorkItemPriority | None = None,
    assignee_id: uuid.UUID | None = None,
    data_product_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    team_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
    service: WorkItemService = Depends(get_work_item_service),
) -> WorkItemBoardResponse:
    filters = _build_filters(
        search=search,
        type=type,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        data_product_id=data_product_id,
        capability_id=capability_id,
        team_id=team_id,
        project_id=project_id,
        company_id=tenant.company_id,
    )
    return await service.get_work_item_board(filters=filters)


@router.post("", response_model=WorkItemRead, status_code=status.HTTP_201_CREATED)
async def create_work_item(
    payload: WorkItemCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: WorkItemService = Depends(get_work_item_service),
) -> WorkItemRead:
    return await service.create_work_item(
        payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{work_item_id}", response_model=WorkItemRead)
async def get_work_item(
    work_item_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: WorkItemService = Depends(get_work_item_service),
) -> WorkItemRead:
    return await service.get_work_item(work_item_id, company_id=tenant.company_id)


@router.patch("/{work_item_id}", response_model=WorkItemRead)
async def update_work_item(
    work_item_id: uuid.UUID,
    payload: WorkItemUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: WorkItemService = Depends(get_work_item_service),
) -> WorkItemRead:
    return await service.update_work_item(work_item_id, payload, company_id=tenant.company_id)


@router.delete("/{work_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_item(
    work_item_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: WorkItemService = Depends(get_work_item_service),
) -> None:
    await service.delete_work_item(work_item_id, company_id=tenant.company_id)
