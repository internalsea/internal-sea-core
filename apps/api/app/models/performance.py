"""Performance metrics models."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import (
    CompanyScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    WorkspaceScopedMixin,
)
from app.domain.enums import MetricDirection, MetricStatus, MetricValueStatus, MetricValueType

if TYPE_CHECKING:
    from app.models.identity import User
    from app.models.people import Person


class PerformanceMetricDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "performance_metric_definitions"
    __table_args__ = (
        Index("ix_performance_metric_definitions_name", "name"),
        Index("ix_performance_metric_definitions_code", "code"),
        Index("ix_performance_metric_definitions_subject_type", "subject_type"),
        Index("ix_performance_metric_definitions_value_type", "value_type"),
        Index("ix_performance_metric_definitions_direction", "direction"),
        Index("ix_performance_metric_definitions_status", "status"),
        Index("ix_performance_metric_definitions_owner_id", "owner_id"),
        UniqueConstraint("code", name="uq_performance_metric_definitions_code"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    subject_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=MetricValueType.NUMBER.value,
    )
    direction: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=MetricDirection.NEUTRAL.value,
    )
    frequency: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=MetricStatus.ACTIVE.value,
    )
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    warning_threshold: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    critical_threshold: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )

    owner: Mapped[Person | None] = relationship("Person")
    values: Mapped[list[PerformanceMetricValue]] = relationship(
        "PerformanceMetricValue",
        back_populates="metric_definition",
        cascade="all, delete-orphan",
    )


class PerformanceMetricValue(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "performance_metric_values"
    __table_args__ = (
        Index("ix_performance_metric_values_metric_definition_id", "metric_definition_id"),
        Index("ix_performance_metric_values_subject", "subject_type", "subject_id"),
        Index("ix_performance_metric_values_period_start", "period_start"),
        Index("ix_performance_metric_values_period_end", "period_end"),
        Index("ix_performance_metric_values_status", "status"),
        Index("ix_performance_metric_values_submitted_by_id", "submitted_by_id"),
        Index("ix_performance_metric_values_approved_by_id", "approved_by_id"),
        Index("ix_performance_metric_values_created_at", "created_at"),
        UniqueConstraint(
            "metric_definition_id",
            "subject_type",
            "subject_id",
            "period_start",
            "period_end",
            name="uq_performance_metric_values_period",
        ),
    )

    metric_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("performance_metric_definitions.id"),
        nullable=False,
    )
    subject_type: Mapped[str] = mapped_column(String(50), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    value_numeric: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    value_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    value_bool: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=MetricValueStatus.SUBMITTED.value,
    )
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    metric_definition: Mapped[PerformanceMetricDefinition] = relationship(
        "PerformanceMetricDefinition",
        back_populates="values",
    )
    submitted_by: Mapped[User | None] = relationship("User", foreign_keys=[submitted_by_id])
    approved_by: Mapped[User | None] = relationship("User", foreign_keys=[approved_by_id])
