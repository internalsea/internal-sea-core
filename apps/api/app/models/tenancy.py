"""SaaS tenant models: Company, Workspace and CompanyMember."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.domain.enums import CompanyMemberRole, CompanyMemberStatus, CompanyStatus, WorkspaceStatus

if TYPE_CHECKING:
    from app.models.identity import User
    from app.models.people import Person


class Company(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "companies"
    __table_args__ = (
        Index("ix_companies_name", "name"),
        Index("ix_companies_slug", "slug"),
        Index("ix_companies_status", "status"),
        Index("ix_companies_industry", "industry"),
        Index("ix_companies_country", "country"),
        UniqueConstraint("slug", name="uq_companies_slug"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    industry: Mapped[str | None] = mapped_column(String(50), nullable=True)
    company_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=CompanyStatus.TRIAL.value,
    )

    workspaces: Mapped[list[Workspace]] = relationship(back_populates="company")
    members: Mapped[list[CompanyMember]] = relationship(back_populates="company")


class Workspace(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "workspaces"
    __table_args__ = (
        Index("ix_workspaces_company_id", "company_id"),
        Index("ix_workspaces_slug", "slug"),
        Index("ix_workspaces_status", "status"),
        UniqueConstraint("company_id", "slug", name="uq_workspaces_company_slug"),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_timezone: Mapped[str | None] = mapped_column(String(100), nullable=True, default="UTC")
    default_currency: Mapped[str | None] = mapped_column(String(10), nullable=True, default="EUR")
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=WorkspaceStatus.ACTIVE.value,
    )

    company: Mapped[Company] = relationship(back_populates="workspaces")


class CompanyMember(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "company_members"
    __table_args__ = (
        Index("ix_company_members_company_id", "company_id"),
        Index("ix_company_members_user_id", "user_id"),
        Index("ix_company_members_person_id", "person_id"),
        Index("ix_company_members_role", "role"),
        Index("ix_company_members_status", "status"),
        UniqueConstraint("company_id", "user_id", name="uq_company_members_company_user"),
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    person_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=CompanyMemberRole.VIEWER.value,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=CompanyMemberStatus.ACTIVE.value,
    )
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    company: Mapped[Company] = relationship(back_populates="members")
    user: Mapped[User] = relationship(back_populates="company_memberships")
    person: Mapped[Person | None] = relationship(back_populates="company_memberships")
