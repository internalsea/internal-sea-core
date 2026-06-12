import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.domain.enums import (
    FileAssetType,
    FileEntityType,
    FileSensitivity,
    FileStatus,
    FileStorageType,
)


class FileStorageBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    storage_type: FileStorageType = FileStorageType.EXTERNAL_URL
    base_url: str | None = None
    description: str | None = None
    is_active: bool = True


class FileStorageCreate(FileStorageBase):
    pass


class FileStorageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    storage_type: FileStorageType | None = None
    base_url: str | None = None
    description: str | None = None
    is_active: bool | None = None


class FileStorageRead(FileStorageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FileStorageListResponse(BaseModel):
    items: list[FileStorageRead]
    page: int
    page_size: int
    total: int
    pages: int


class FileAssetBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    file_type: FileAssetType = FileAssetType.DOCUMENT
    status: FileStatus = FileStatus.ACTIVE
    sensitivity: FileSensitivity = FileSensitivity.INTERNAL
    storage_id: uuid.UUID | None = None
    original_filename: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    external_url: str | None = None
    storage_path: str | None = None
    checksum: str | None = None
    version: str | None = None
    owner_id: uuid.UUID | None = None
    uploaded_by_id: uuid.UUID | None = None

    @field_validator("file_size_bytes")
    @classmethod
    def validate_file_size(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("file_size_bytes must be >= 0")
        return value

    @field_validator("external_url")
    @classmethod
    def validate_external_url(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        HttpUrl(value)
        return value


class FileAssetCreate(FileAssetBase):
    pass


class FileAssetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    file_type: FileAssetType | None = None
    status: FileStatus | None = None
    sensitivity: FileSensitivity | None = None
    storage_id: uuid.UUID | None = None
    original_filename: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    external_url: str | None = None
    storage_path: str | None = None
    checksum: str | None = None
    version: str | None = None
    owner_id: uuid.UUID | None = None
    uploaded_by_id: uuid.UUID | None = None

    @field_validator("file_size_bytes")
    @classmethod
    def validate_file_size(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("file_size_bytes must be >= 0")
        return value

    @field_validator("external_url")
    @classmethod
    def validate_external_url(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        HttpUrl(value)
        return value


class FileAssetRead(FileAssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FileAssetListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    file_type: FileAssetType
    status: FileStatus
    sensitivity: FileSensitivity
    storage_id: uuid.UUID | None
    external_url: str | None
    owner_id: uuid.UUID | None
    version: str | None
    updated_at: datetime


class FileAssetListResponse(BaseModel):
    items: list[FileAssetListItem]
    total: int
    page: int
    page_size: int
    pages: int


class FileAssetFilters(BaseModel):
    search: str | None = None
    file_type: FileAssetType | None = None
    status: FileStatus | None = None
    sensitivity: FileSensitivity | None = None
    storage_id: uuid.UUID | None = None
    owner_id: uuid.UUID | None = None
    is_evidence: bool | None = None


class FileAttachmentCreate(BaseModel):
    file_id: uuid.UUID
    entity_type: FileEntityType
    entity_id: uuid.UUID
    purpose: str | None = Field(default=None, max_length=255)
    is_evidence: bool = False
    evidence_type: str | None = Field(default=None, max_length=255)
    attached_by_id: uuid.UUID | None = None


class FileAttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    file_id: uuid.UUID
    entity_type: FileEntityType
    entity_id: uuid.UUID
    purpose: str | None
    is_evidence: bool
    evidence_type: str | None
    attached_by_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    file: FileAssetListItem | None = None


class FileAttachmentListResponse(BaseModel):
    items: list[FileAttachmentRead]
    total: int
    page: int
    page_size: int
    pages: int


class EntityFilesResponse(BaseModel):
    entity_type: FileEntityType
    entity_id: uuid.UUID
    files: list[FileAttachmentRead]
    total: int
