import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import DataProductStatus, DataProductType, QualityStatus


class DataProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    type: DataProductType = DataProductType.DATASET
    status: DataProductStatus = DataProductStatus.DRAFT
    quality_status: QualityStatus = QualityStatus.UNKNOWN
    business_domain_id: uuid.UUID | None = None
    business_owner_id: uuid.UUID | None = None
    technical_owner_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    refresh_frequency: str | None = Field(default=None, max_length=100)
    source_systems: str | None = None
    consumers: str | None = None
    documentation_url: str | None = Field(default=None, max_length=2048)


class DataProductCreate(DataProductBase):
    pass


class DataProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    type: DataProductType | None = None
    status: DataProductStatus | None = None
    quality_status: QualityStatus | None = None
    business_domain_id: uuid.UUID | None = None
    business_owner_id: uuid.UUID | None = None
    technical_owner_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    refresh_frequency: str | None = Field(default=None, max_length=100)
    source_systems: str | None = None
    consumers: str | None = None
    documentation_url: str | None = Field(default=None, max_length=2048)


class DataProductRead(DataProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PaginatedDataProductList(BaseModel):
    items: list[DataProductRead]
    page: int
    page_size: int
    total: int
    pages: int
