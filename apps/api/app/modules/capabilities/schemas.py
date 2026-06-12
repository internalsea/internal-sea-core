import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CapabilityBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class CapabilityCreate(CapabilityBase):
    pass


class CapabilityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value


class CapabilityRead(CapabilityBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CapabilityListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    updated_at: datetime


class CapabilityListResponse(BaseModel):
    items: list[CapabilityListItem]
    total: int
    page: int
    page_size: int
    pages: int


class CapabilitySummary(BaseModel):
    capability: CapabilityRead
    people_count: int
    active_people_count: int
    data_products_count: int
    open_work_items_count: int
    projects_count: int
    internal_projects_count: int
