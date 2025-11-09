from __future__ import annotations
from typing import List, Optional
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin, TimestampMixin

class User(Base, IDMixin, TimestampMixin):
    """Global user (email unique across all orgs)."""
    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # Relationships
    memberships: Mapped[List["OrganizationMembership"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    team_roles: Mapped[List["TeamUserRole"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Role(Base, IDMixin, TimestampMixin):
    """Reusable role definitions used at org and team level."""
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Backrefs
    org_memberships: Mapped[List["OrganizationMembership"]] = relationship(back_populates="role")
    team_user_roles: Mapped[List["TeamUserRole"]] = relationship(back_populates="role")
