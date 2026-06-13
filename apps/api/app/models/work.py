from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import (
    CompanyScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    WorkspaceScopedMixin,
)
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType

if TYPE_CHECKING:
    from app.models.catalog import DataProduct
    from app.models.identity import User
    from app.models.people import Capability, Person, Team
    from app.models.projects import Project


class WorkItem(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "work_items"
    __table_args__ = (
        Index("ix_work_items_title", "title"),
        Index("ix_work_items_type", "type"),
        Index("ix_work_items_status", "status"),
        Index("ix_work_items_priority", "priority"),
        Index("ix_work_items_assignee_id", "assignee_id"),
        Index("ix_work_items_data_product_id", "data_product_id"),
        Index("ix_work_items_capability_id", "capability_id"),
        Index("ix_work_items_team_id", "team_id"),
        Index("ix_work_items_due_date", "due_date"),
        Index("ix_work_items_project_id", "project_id"),
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[WorkItemType] = mapped_column(
        Enum(WorkItemType, native_enum=False, length=50),
        default=WorkItemType.TASK,
        nullable=False,
    )
    status: Mapped[WorkItemStatus] = mapped_column(
        Enum(WorkItemStatus, native_enum=False, length=50),
        default=WorkItemStatus.BACKLOG,
        nullable=False,
    )
    priority: Mapped[WorkItemPriority] = mapped_column(
        Enum(WorkItemPriority, native_enum=False, length=50),
        default=WorkItemPriority.MEDIUM,
        nullable=False,
    )
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    reporter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    data_product_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("data_products.id"),
        nullable=True,
    )
    capability_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("capabilities.id"),
        nullable=True,
    )
    team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
        nullable=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=True,
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimate_points: Mapped[int | None] = mapped_column(Integer, nullable=True)

    assignee: Mapped[Person | None] = relationship(back_populates="assigned_work_items")
    reporter: Mapped[User | None] = relationship(back_populates="reported_work_items")
    data_product: Mapped[DataProduct | None] = relationship(back_populates="work_items")
    capability: Mapped[Capability | None] = relationship(back_populates="work_items")
    team: Mapped[Team | None] = relationship(back_populates="work_items")
    project: Mapped[Project | None] = relationship(back_populates="work_items")
    comments: Mapped[list[Comment]] = relationship(back_populates="work_item")


class Comment(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "comments"
    __table_args__ = (
        CheckConstraint(
            "data_product_id IS NOT NULL OR work_item_id IS NOT NULL OR project_id IS NOT NULL",
            name="ck_comments_target_required",
        ),
    )

    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    data_product_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("data_products.id"),
        nullable=True,
    )
    work_item_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("work_items.id"),
        nullable=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=True,
    )

    author: Mapped[User | None] = relationship(back_populates="comments")
    data_product: Mapped[DataProduct | None] = relationship(back_populates="comments")
    work_item: Mapped[WorkItem | None] = relationship(back_populates="comments")
    project: Mapped[Project | None] = relationship(back_populates="comments")
