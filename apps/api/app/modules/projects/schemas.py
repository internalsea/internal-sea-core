import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.enums import ProjectStatus, ProjectType


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_type: ProjectType = ProjectType.CLIENT_PROJECT
    status: ProjectStatus = ProjectStatus.IDEA
    client_name: str | None = Field(default=None, max_length=255)
    account_name: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    actual_end_date: date | None = None
    budget_amount: Decimal | None = Field(default=None, ge=0)
    budget_currency: str | None = Field(default="EUR", max_length=10)
    priority: str | None = Field(default=None, max_length=50)
    health_status: str | None = Field(default=None, max_length=50)
    delivery_notes: str | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if (
            self.start_date is not None
            and self.target_end_date is not None
            and self.target_end_date < self.start_date
        ):
            raise ValueError("target_end_date cannot be before start_date")
        if (
            self.start_date is not None
            and self.actual_end_date is not None
            and self.actual_end_date < self.start_date
        ):
            raise ValueError("actual_end_date cannot be before start_date")
        return self


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    project_type: ProjectType | None = None
    status: ProjectStatus | None = None
    client_name: str | None = Field(default=None, max_length=255)
    account_name: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    actual_end_date: date | None = None
    budget_amount: Decimal | None = Field(default=None, ge=0)
    budget_currency: str | None = Field(default=None, max_length=10)
    priority: str | None = Field(default=None, max_length=50)
    health_status: str | None = Field(default=None, max_length=50)
    delivery_notes: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if (
            self.start_date is not None
            and self.target_end_date is not None
            and self.target_end_date < self.start_date
        ):
            raise ValueError("target_end_date cannot be before start_date")
        if (
            self.start_date is not None
            and self.actual_end_date is not None
            and self.actual_end_date < self.start_date
        ):
            raise ValueError("actual_end_date cannot be before start_date")
        return self


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProjectListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    project_type: ProjectType
    status: ProjectStatus
    client_name: str | None
    owner_id: uuid.UUID | None
    team_id: uuid.UUID | None
    capability_id: uuid.UUID | None
    start_date: date | None
    target_end_date: date | None
    health_status: str | None
    updated_at: datetime


class ProjectListResponse(BaseModel):
    items: list[ProjectListItem]
    total: int
    page: int
    page_size: int
    pages: int


class ProjectSummary(BaseModel):
    project: ProjectRead
    open_work_items: int
    completed_work_items: int
    total_work_items: int
    overdue_work_items: int
