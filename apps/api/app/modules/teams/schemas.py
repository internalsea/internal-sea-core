import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeamBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value


class TeamRead(TeamBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TeamListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    updated_at: datetime


class TeamListResponse(BaseModel):
    items: list[TeamListItem]
    total: int
    page: int
    page_size: int
    pages: int


class TeamSummary(BaseModel):
    team: TeamRead
    people_count: int
    active_people_count: int
    data_products_count: int
    open_work_items_count: int
    projects_count: int
    internal_projects_count: int
