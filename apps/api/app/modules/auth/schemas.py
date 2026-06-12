from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.enums import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class CurrentUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool
    is_superuser: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: CurrentUser


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str = Field(min_length=8)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: str | None = Field(default=None, min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool
    is_superuser: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class UserListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool
    is_superuser: bool
    last_login_at: datetime | None
    updated_at: datetime


class UserListResponse(BaseModel):
    items: list[UserListItem]
    total: int
    page: int
    page_size: int
    pages: int


class UserFilters(BaseModel):
    search: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class MessageResponse(BaseModel):
    message: str


class UserCreateInternal(BaseModel):
    email: str
    full_name: str | None
    hashed_password: str
    role: UserRole
    is_active: bool
    is_superuser: bool


class UserUpdateInternal(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    hashed_password: str | None = None
