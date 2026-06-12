from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin, WorkspaceScopedMixin
from app.domain.enums import (
    AutomationActionType,
    AutomationRunStatus,
    AutomationStatus,
    AutomationTriggerType,
    ScheduleFrequency,
)

if TYPE_CHECKING:
    from app.models.identity import User


class AutomationSchedule(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "automation_schedules"
    __table_args__ = (
        Index("ix_automation_schedules_name", "name"),
        Index("ix_automation_schedules_frequency", "frequency"),
        Index("ix_automation_schedules_is_active", "is_active"),
        Index("ix_automation_schedules_next_run_at", "next_run_at"),
        Index("ix_automation_schedules_last_run_at", "last_run_at"),
        Index("ix_automation_schedules_created_by_id", "created_by_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    frequency: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ScheduleFrequency.MONTHLY.value,
    )
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True, default="UTC")
    start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cron_expression: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    created_by: Mapped[User | None] = relationship(back_populates="automation_schedules")
    triggers: Mapped[list[AutomationTrigger]] = relationship(
        "AutomationTrigger",
        back_populates="schedule",
    )


class AutomationTrigger(Base, UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin):
    __tablename__ = "automation_triggers"
    __table_args__ = (
        Index("ix_automation_triggers_name", "name"),
        Index("ix_automation_triggers_status", "status"),
        Index("ix_automation_triggers_trigger_type", "trigger_type"),
        Index("ix_automation_triggers_action_type", "action_type"),
        Index("ix_automation_triggers_schedule_id", "schedule_id"),
        Index("ix_automation_triggers_target_type_target_id", "target_type", "target_id"),
        Index("ix_automation_triggers_created_by_id", "created_by_id"),
        Index("ix_automation_triggers_last_run_at", "last_run_at"),
        Index("ix_automation_triggers_next_run_at", "next_run_at"),
        Index("ix_automation_triggers_status_next_run_at", "status", "next_run_at"),
        Index("ix_automation_triggers_lock_expires_at", "lock_expires_at"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=AutomationStatus.DRAFT.value,
    )
    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=AutomationTriggerType.SCHEDULE.value,
    )
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    schedule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("automation_schedules.id"),
        nullable=True,
    )
    target_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    conditions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    action_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    locked_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lock_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    schedule: Mapped[AutomationSchedule | None] = relationship(
        "AutomationSchedule",
        back_populates="triggers",
    )
    created_by: Mapped[User | None] = relationship(back_populates="automation_triggers")
    runs: Mapped[list[AutomationRun]] = relationship(
        "AutomationRun",
        back_populates="trigger",
    )


class AutomationRun(Base, UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin):
    __tablename__ = "automation_runs"
    __table_args__ = (
        Index("ix_automation_runs_trigger_id", "trigger_id"),
        Index("ix_automation_runs_status", "status"),
        Index("ix_automation_runs_started_at", "started_at"),
        Index("ix_automation_runs_finished_at", "finished_at"),
        Index("ix_automation_runs_target_type_target_id", "target_type", "target_id"),
        Index("ix_automation_runs_action_type", "action_type"),
        Index("ix_automation_runs_executed_by_id", "executed_by_id"),
        Index("ix_automation_runs_created_at", "created_at"),
        Index("ix_automation_runs_worker_instance_id", "worker_instance_id"),
    )

    trigger_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("automation_triggers.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=AutomationRunStatus.PENDING.value,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    target_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    worker_instance_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    trigger: Mapped[AutomationTrigger] = relationship("AutomationTrigger", back_populates="runs")
    executed_by: Mapped[User | None] = relationship(back_populates="automation_runs")
