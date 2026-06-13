from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.domain.enums import UserRole

if TYPE_CHECKING:
    from app.models.activity import ActivityEvent
    from app.models.automation import AutomationRun, AutomationSchedule, AutomationTrigger
    from app.models.people import Person
    from app.models.relationships import EntityLink
    from app.models.tenancy import CompanyMember
    from app.models.work import Comment, WorkItem


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, length=50),
        default=UserRole.VIEWER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    person_profile: Mapped[Person | None] = relationship(
        back_populates="user",
        uselist=False,
    )
    reported_work_items: Mapped[list[WorkItem]] = relationship(
        back_populates="reporter",
    )
    comments: Mapped[list[Comment]] = relationship(
        back_populates="author",
    )
    activity_events: Mapped[list[ActivityEvent]] = relationship(
        back_populates="actor",
    )
    entity_links: Mapped[list[EntityLink]] = relationship(
        back_populates="created_by",
    )
    automation_schedules: Mapped[list[AutomationSchedule]] = relationship(
        back_populates="created_by",
    )
    automation_triggers: Mapped[list[AutomationTrigger]] = relationship(
        back_populates="created_by",
    )
    automation_runs: Mapped[list[AutomationRun]] = relationship(
        back_populates="executed_by",
    )
    company_memberships: Mapped[list[CompanyMember]] = relationship(
        back_populates="user",
    )
