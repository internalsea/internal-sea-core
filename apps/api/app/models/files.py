"""File metadata and attachment models."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import (
    CompanyScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    WorkspaceScopedMixin,
)
from app.domain.enums import (
    FileAssetType,
    FileSensitivity,
    FileStatus,
    FileStorageType,
)

if TYPE_CHECKING:
    from app.models.identity import User
    from app.models.people import Person


class FileStorage(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "file_storages"
    __table_args__ = (
        Index("ix_file_storages_name", "name"),
        Index("ix_file_storages_storage_type", "storage_type"),
        Index("ix_file_storages_is_active", "is_active"),
        UniqueConstraint("name", name="uq_file_storages_name"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=FileStorageType.EXTERNAL_URL.value,
    )
    base_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    assets: Mapped[list[FileAsset]] = relationship(
        "FileAsset",
        back_populates="storage",
    )


class FileAsset(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "file_assets"
    __table_args__ = (
        Index("ix_file_assets_name", "name"),
        Index("ix_file_assets_file_type", "file_type"),
        Index("ix_file_assets_status", "status"),
        Index("ix_file_assets_sensitivity", "sensitivity"),
        Index("ix_file_assets_storage_id", "storage_id"),
        Index("ix_file_assets_owner_id", "owner_id"),
        Index("ix_file_assets_uploaded_by_id", "uploaded_by_id"),
        Index("ix_file_assets_created_at", "created_at"),
        Index("ix_file_assets_updated_at", "updated_at"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=FileAssetType.DOCUMENT.value,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=FileStatus.ACTIVE.value,
    )
    sensitivity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=FileSensitivity.INTERNAL.value,
    )
    storage_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_storages.id"),
        nullable=True,
    )
    original_filename: Mapped[str | None] = mapped_column(String(512), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    external_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    storage_path: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    uploaded_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    storage: Mapped[FileStorage | None] = relationship("FileStorage", back_populates="assets")
    owner: Mapped[Person | None] = relationship("Person")
    uploaded_by: Mapped[User | None] = relationship("User")
    attachments: Mapped[list[FileAttachment]] = relationship(
        "FileAttachment",
        back_populates="file",
        cascade="all, delete-orphan",
    )


class FileAttachment(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "file_attachments"
    __table_args__ = (
        Index("ix_file_attachments_file_id", "file_id"),
        Index(
            "ix_file_attachments_entity_type_entity_id",
            "entity_type",
            "entity_id",
        ),
        Index(
            "ix_file_attachments_entity_evidence",
            "entity_type",
            "entity_id",
            "is_evidence",
        ),
        Index("ix_file_attachments_is_evidence", "is_evidence"),
        Index("ix_file_attachments_evidence_type", "evidence_type"),
        Index("ix_file_attachments_attached_by_id", "attached_by_id"),
        Index("ix_file_attachments_created_at", "created_at"),
        UniqueConstraint(
            "file_id",
            "entity_type",
            "entity_id",
            "purpose",
            name="uq_file_attachments_file_entity_purpose",
        ),
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_assets.id"),
        nullable=False,
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    purpose: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_evidence: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    evidence_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attached_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    file: Mapped[FileAsset] = relationship("FileAsset", back_populates="attachments")
    attached_by: Mapped[User | None] = relationship("User")
