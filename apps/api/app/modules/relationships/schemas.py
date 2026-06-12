import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import EntityLinkType, EntityType


class EntityRef(BaseModel):
    entity_type: EntityType
    entity_id: uuid.UUID


class EntityLinkCreate(BaseModel):
    source_type: EntityType
    source_id: uuid.UUID
    target_type: EntityType
    target_id: uuid.UUID
    link_type: EntityLinkType
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    created_by_id: uuid.UUID | None = None

    @model_validator(mode="after")
    def validate_not_self_link(self) -> "EntityLinkCreate":
        if (
            self.source_type == self.target_type
            and self.source_id == self.target_id
        ):
            raise ValueError("source and target cannot be the same object")
        return self


class EntityLinkUpdate(BaseModel):
    link_type: EntityLinkType | None = None
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None


class EntityLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_type: EntityType
    source_id: uuid.UUID
    target_type: EntityType
    target_id: uuid.UUID
    link_type: EntityLinkType
    title: str | None
    description: str | None
    created_by_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class EntityLinkListResponse(BaseModel):
    items: list[EntityLinkRead]
    total: int
    page: int
    page_size: int
    pages: int


class EntityLinkFilters(BaseModel):
    entity_type: EntityType | None = None
    entity_id: uuid.UUID | None = None
    source_type: EntityType | None = None
    source_id: uuid.UUID | None = None
    target_type: EntityType | None = None
    target_id: uuid.UUID | None = None
    link_type: EntityLinkType | None = None
    include_reverse: bool = True


class EntityRelationshipView(BaseModel):
    entity_type: EntityType
    entity_id: uuid.UUID
    outgoing: list[EntityLinkRead]
    incoming: list[EntityLinkRead]
    total: int
