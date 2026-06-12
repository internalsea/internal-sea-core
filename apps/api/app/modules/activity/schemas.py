import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import ActivityAction, ActivityEntityType


class ActivityEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    entity_type: ActivityEntityType
    entity_id: uuid.UUID
    action: ActivityAction
    actor_id: uuid.UUID | None
    title: str
    description: str | None
    details: dict[str, Any] | None
    created_at: datetime


class ActivityEventCreateInternal(BaseModel):
    entity_type: ActivityEntityType
    entity_id: uuid.UUID
    action: ActivityAction
    actor_id: uuid.UUID | None = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    details: dict[str, Any] | None = None


class ActivityEventListResponse(BaseModel):
    items: list[ActivityEventRead]
    total: int
    page: int
    page_size: int
    pages: int


class ActivityEventFilters(BaseModel):
    entity_type: ActivityEntityType | None = None
    entity_id: uuid.UUID | None = None
    action: ActivityAction | None = None
    actor_id: uuid.UUID | None = None
