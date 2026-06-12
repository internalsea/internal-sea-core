import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1, max_length=5000)
    author_id: uuid.UUID | None = None

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("body cannot be empty")
        return value


class CommentUpdate(BaseModel):
    body: str = Field(..., min_length=1, max_length=5000)

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("body cannot be empty")
        return value


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    body: str
    author_id: uuid.UUID | None
    data_product_id: uuid.UUID | None
    work_item_id: uuid.UUID | None
    project_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class CommentListResponse(BaseModel):
    items: list[CommentRead]
    total: int
    page: int
    page_size: int
    pages: int
