from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin, WorkspaceScopedMixin

if TYPE_CHECKING:
    from app.models.identity import User


class EntityLink(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "entity_links"
    __table_args__ = (
        UniqueConstraint(
            "source_type",
            "source_id",
            "target_type",
            "target_id",
            "link_type",
            name="uq_entity_links_source_target_type",
        ),
        CheckConstraint(
            "NOT (source_type = target_type AND source_id = target_id)",
            name="ck_entity_links_no_self_link",
        ),
        Index("ix_entity_links_source_type_source_id", "source_type", "source_id"),
        Index("ix_entity_links_target_type_target_id", "target_type", "target_id"),
        Index(
            "ix_entity_links_source_target",
            "source_type",
            "source_id",
            "target_type",
            "target_id",
        ),
        Index("ix_entity_links_link_type", "link_type"),
        Index("ix_entity_links_created_by_id", "created_by_id"),
        Index("ix_entity_links_created_at", "created_at"),
    )

    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    link_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    created_by: Mapped[User | None] = relationship(back_populates="entity_links")
