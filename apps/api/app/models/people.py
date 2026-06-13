from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import (
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    WorkspaceScopedMixin,
)
from app.domain.enums import SeniorityLevel

if TYPE_CHECKING:
    from app.models.catalog import BusinessDomain, DataProduct
    from app.models.identity import User
    from app.models.projects import Project
    from app.models.tenancy import CompanyMember
    from app.models.work import WorkItem


class Team(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    people: Mapped[list[Person]] = relationship(back_populates="team")
    data_products: Mapped[list[DataProduct]] = relationship(back_populates="team")
    work_items: Mapped[list[WorkItem]] = relationship(back_populates="team")
    projects: Mapped[list[Project]] = relationship(back_populates="team")


class Capability(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "capabilities"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    people: Mapped[list[Person]] = relationship(back_populates="capability")
    data_products: Mapped[list[DataProduct]] = relationship(back_populates="capability")
    work_items: Mapped[list[WorkItem]] = relationship(back_populates="capability")
    projects: Mapped[list[Project]] = relationship(back_populates="capability")


class Person(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "people"
    __table_args__ = (
        CheckConstraint(
            "availability_percent IS NULL OR "
            "(availability_percent >= 0 AND availability_percent <= 100)",
            name="ck_people_availability_percent_range",
        ),
        Index("ix_people_email", "email"),
    )

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    role_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    seniority_level: Mapped[SeniorityLevel | None] = mapped_column(
        Enum(SeniorityLevel, native_enum=False, length=50),
        nullable=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
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
    availability_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="person_profile")
    team: Mapped[Team | None] = relationship(back_populates="people")
    capability: Mapped[Capability | None] = relationship(back_populates="people")
    owned_business_domains: Mapped[list[BusinessDomain]] = relationship(
        back_populates="owner",
    )
    owned_business_data_products: Mapped[list[DataProduct]] = relationship(
        back_populates="business_owner",
        foreign_keys="DataProduct.business_owner_id",
    )
    owned_technical_data_products: Mapped[list[DataProduct]] = relationship(
        back_populates="technical_owner",
        foreign_keys="DataProduct.technical_owner_id",
    )
    assigned_work_items: Mapped[list[WorkItem]] = relationship(
        back_populates="assignee",
    )
    owned_projects: Mapped[list[Project]] = relationship(back_populates="owner")
    company_memberships: Mapped[list[CompanyMember]] = relationship(
        back_populates="person",
    )
