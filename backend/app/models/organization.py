from __future__ import annotations
from typing import List, Optional
from sqlalchemy import Boolean, Integer, String, UniqueConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin, TimestampMixin

class Organization(Base, IDMixin, TimestampMixin):
    """Tenant organization in the platform."""
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    # Relationships
    memberships: Mapped[List["OrganizationMembership"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    teams: Mapped[List["Team"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )


class OrganizationMembership(Base, IDMixin, TimestampMixin):
    """
    Links users <-> organizations with an optional org-level role.
    Enforces one membership per (organization, user).
    """
    __tablename__ = "organization_memberships"
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_membership_org_user"),
        # Helpful composite index for common lookups
        Index("ix_org_memberships_org_user", "organization_id", "user_id"),
        Index("ix_org_memberships_user_default", "user_id", "is_default"),
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"), nullable=True
    )

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="memberships")
    user: Mapped["User"] = relationship(back_populates="memberships")
    role: Mapped[Optional["Role"]] = relationship(back_populates="org_memberships")
