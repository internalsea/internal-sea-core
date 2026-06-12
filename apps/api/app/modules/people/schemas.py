import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.enums import SeniorityLevel


class PersonBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    role_title: str | None = Field(default=None, max_length=255)
    seniority_level: SeniorityLevel | None = None
    user_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    availability_percent: int | None = Field(default=None, ge=0, le=100)
    location: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    role_title: str | None = Field(default=None, max_length=255)
    seniority_level: SeniorityLevel | None = None
    user_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    availability_percent: int | None = Field(default=None, ge=0, le=100)
    location: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("full_name cannot be empty")
        return value


class PersonRead(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PersonListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str | None
    role_title: str | None
    seniority_level: SeniorityLevel | None
    team_id: uuid.UUID | None
    capability_id: uuid.UUID | None
    availability_percent: int | None
    location: str | None
    is_active: bool
    updated_at: datetime


class PersonListResponse(BaseModel):
    items: list[PersonListItem]
    total: int
    page: int
    page_size: int
    pages: int


class PersonSummary(BaseModel):
    person: PersonRead
    assigned_work_items: int
    owned_data_products_business: int
    owned_data_products_technical: int
    owned_projects: int
