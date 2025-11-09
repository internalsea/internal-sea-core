from __future__ import annotations
from typing import List, Optional
from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin, TimestampMixin

class Team(Base, IDMixin, TimestampMixin):
    """Team inside an organization (name unique within org)."""
    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("organization_id", "name", name="uq_team_org_name"),
        Index("ix_teams_org_id", "organization_id"),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="teams")
    user_roles: Mapped[List["TeamUserRole"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )

class TeamUserRole(Base, IDMixin, TimestampMixin):
    """Assigns a team-scoped role to a user."""
    __tablename__ = "team_user_roles"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", "role_id", name="uq_team_user_role"),
        Index("ix_tur_team_user", "team_id", "user_id"),
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="user_roles")
    user: Mapped["User"] = relationship(back_populates="team_roles")
    role: Mapped["Role"] = relationship(back_populates="team_user_roles")
