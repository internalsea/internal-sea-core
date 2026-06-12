import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


class WorkItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    type: WorkItemType = WorkItemType.TASK
    status: WorkItemStatus = WorkItemStatus.BACKLOG
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    assignee_id: uuid.UUID | None = None
    reporter_id: uuid.UUID | None = None
    data_product_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    due_date: date | None = None
    estimate_points: int | None = Field(default=None, ge=0)


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    type: WorkItemType | None = None
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    assignee_id: uuid.UUID | None = None
    reporter_id: uuid.UUID | None = None
    data_product_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    due_date: date | None = None
    estimate_points: int | None = Field(default=None, ge=0)


class WorkItemRead(WorkItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PaginatedWorkItemList(BaseModel):
    items: list[WorkItemRead]
    page: int
    page_size: int
    total: int
    pages: int


class WorkItemBoardColumn(BaseModel):
    status: WorkItemStatus
    title: str
    items: list[WorkItemRead]
    count: int


class WorkItemBoardResponse(BaseModel):
    columns: list[WorkItemBoardColumn]
