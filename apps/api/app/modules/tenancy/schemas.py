"""Pydantic schemas for SaaS tenancy."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.enums import (
    CompanyMemberRole,
    CompanyMemberStatus,
    CompanySize,
    CompanyStatus,
    Industry,
    WorkspaceStatus,
)
from app.modules.auth.schemas import CurrentUser


class CompanyBase(BaseModel):
    name: str
    slug: str | None = None
    description: str | None = None
    industry: Industry | None = None
    company_size: CompanySize | None = None
    country: str | None = None
    website: str | None = None
    status: CompanyStatus = CompanyStatus.TRIAL

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Company name is required")
        return value.strip()


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    industry: Industry | None = None
    company_size: CompanySize | None = None
    country: str | None = None
    website: str | None = None
    status: CompanyStatus | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Company name cannot be empty")
        return value.strip() if value else value


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    industry: str | None
    company_size: str | None
    country: str | None
    website: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class WorkspaceBase(BaseModel):
    company_id: uuid.UUID
    name: str
    slug: str | None = None
    description: str | None = None
    default_timezone: str = "UTC"
    default_currency: str = "EUR"
    status: WorkspaceStatus = WorkspaceStatus.ACTIVE

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Workspace name is required")
        return value.strip()


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    default_timezone: str | None = None
    default_currency: str | None = None
    status: WorkspaceStatus | None = None


class WorkspaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    slug: str
    description: str | None
    default_timezone: str | None
    default_currency: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class CompanyMemberBase(BaseModel):
    company_id: uuid.UUID
    user_id: uuid.UUID
    person_id: uuid.UUID | None = None
    role: CompanyMemberRole = CompanyMemberRole.VIEWER
    status: CompanyMemberStatus = CompanyMemberStatus.ACTIVE


class CompanyMemberCreate(CompanyMemberBase):
    pass


class CompanyMemberUpdate(BaseModel):
    person_id: uuid.UUID | None = None
    role: CompanyMemberRole | None = None
    status: CompanyMemberStatus | None = None


class CompanyMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    user_id: uuid.UUID
    person_id: uuid.UUID | None
    role: str
    status: str
    joined_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CurrentTenantContext(BaseModel):
    company: CompanyRead
    workspace: WorkspaceRead
    member: CompanyMemberRead


class FirstUserOnboardingRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    company_name: str
    company_size: CompanySize | None = None
    industry: Industry | None = None
    country: str | None = None
    team_name: str | None = None
    main_capability_name: str | None = None

    @field_validator("full_name", "company_name")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field is required")
        return value.strip()


class FirstUserOnboardingResponse(BaseModel):
    user: CurrentUser
    company: CompanyRead
    workspace: WorkspaceRead
    member: CompanyMemberRead
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class CompanyListResponse(BaseModel):
    items: list[CompanyRead]
    total: int
    page: int
    page_size: int
    pages: int


class WorkspaceListResponse(BaseModel):
    items: list[WorkspaceRead]
    total: int
    page: int
    page_size: int
    pages: int


class CompanyMemberListResponse(BaseModel):
    items: list[CompanyMemberRead]
    total: int
    page: int
    page_size: int
    pages: int
