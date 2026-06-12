from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin, WorkspaceScopedMixin
from app.domain.enums import ProjectStatus, ProjectType

if TYPE_CHECKING:
    from app.models.people import Capability, Person, Team
    from app.models.work import Comment, WorkItem


class Project(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "projects"
    __table_args__ = (
        Index("ix_projects_name", "name"),
        Index("ix_projects_project_type", "project_type"),
        Index("ix_projects_status", "status"),
        Index("ix_projects_client_name", "client_name"),
        Index("ix_projects_owner_id", "owner_id"),
        Index("ix_projects_team_id", "team_id"),
        Index("ix_projects_capability_id", "capability_id"),
        Index("ix_projects_start_date", "start_date"),
        Index("ix_projects_target_end_date", "target_end_date"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_type: Mapped[ProjectType] = mapped_column(
        Enum(ProjectType, native_enum=False, length=50),
        default=ProjectType.CLIENT_PROJECT,
        nullable=False,
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, native_enum=False, length=50),
        default=ProjectStatus.IDEA,
        nullable=False,
    )
    client_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    account_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
        nullable=True,
    )
    capability_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("capabilities.id"),
        nullable=True,
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    actual_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    budget_currency: Mapped[str | None] = mapped_column(String(10), default="EUR", nullable=True)
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    health_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    delivery_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    owner: Mapped[Person | None] = relationship(back_populates="owned_projects")
    team: Mapped[Team | None] = relationship(back_populates="projects")
    capability: Mapped[Capability | None] = relationship(back_populates="projects")
    work_items: Mapped[list[WorkItem]] = relationship(back_populates="project")
    comments: Mapped[list[Comment]] = relationship(back_populates="project")
