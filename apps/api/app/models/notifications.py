"""Notification channel, template, preference, message and delivery models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import (
    CompanyScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    WorkspaceScopedMixin,
)

if TYPE_CHECKING:
    from app.models.automation import AutomationRun
    from app.models.identity import User
    from app.models.people import Person


class NotificationChannel(UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin, Base):
    """Outbound notification channel configuration.

    ``provider_config`` must not store secrets in plain text; use environment
    variables or a future secret manager for credentials.
    """

    __tablename__ = "notification_channels"
    __table_args__ = (
        UniqueConstraint("name", name="uq_notification_channels_name"),
        Index("ix_notification_channels_name", "name"),
        Index("ix_notification_channels_channel_type", "channel_type"),
        Index("ix_notification_channels_status", "status"),
        Index("ix_notification_channels_created_by_id", "created_by_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    endpoint_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    default_recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    created_by: Mapped[User | None] = relationship("User", foreign_keys=[created_by_id])
    messages: Mapped[list[NotificationMessage]] = relationship(
        "NotificationMessage",
        back_populates="channel",
    )


class NotificationTemplate(UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin, Base):
    __tablename__ = "notification_templates"
    __table_args__ = (
        UniqueConstraint("name", name="uq_notification_templates_name"),
        Index("ix_notification_templates_name", "name"),
        Index("ix_notification_templates_status", "status"),
        Index("ix_notification_templates_event_type", "event_type"),
        Index("ix_notification_templates_created_by_id", "created_by_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    event_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subject_template: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    created_by: Mapped[User | None] = relationship("User", foreign_keys=[created_by_id])
    messages: Mapped[list[NotificationMessage]] = relationship(
        "NotificationMessage",
        back_populates="template",
    )


class NotificationPreference(UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin, Base):
    __tablename__ = "notification_preferences"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "person_id",
            "channel_type",
            "event_type",
            name="uq_notification_preferences_user_person_channel_event",
        ),
        Index("ix_notification_preferences_user_id", "user_id"),
        Index("ix_notification_preferences_person_id", "person_id"),
        Index("ix_notification_preferences_channel_type", "channel_type"),
        Index("ix_notification_preferences_event_type", "event_type"),
        Index("ix_notification_preferences_is_enabled", "is_enabled"),
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    person_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
    )
    channel_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped[User | None] = relationship("User", foreign_keys=[user_id])
    person: Mapped[Person | None] = relationship("Person", foreign_keys=[person_id])


class NotificationMessage(UUIDPrimaryKeyMixin, TimestampMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "notification_messages"
    __table_args__ = (
        Index("ix_notification_messages_channel_id", "channel_id"),
        Index("ix_notification_messages_template_id", "template_id"),
        Index("ix_notification_messages_status", "status"),
        Index("ix_notification_messages_priority", "priority"),
        Index("ix_notification_messages_event_type", "event_type"),
        Index(
            "ix_notification_messages_recipient_type_value",
            "recipient_type",
            "recipient_value",
        ),
        Index("ix_notification_messages_entity_type_id", "entity_type", "entity_id"),
        Index("ix_notification_messages_automation_run_id", "automation_run_id"),
        Index("ix_notification_messages_created_by_id", "created_by_id"),
        Index("ix_notification_messages_scheduled_at", "scheduled_at"),
        Index("ix_notification_messages_sent_at", "sent_at"),
        Index("ix_notification_messages_simulated_at", "simulated_at"),
        Index("ix_notification_messages_created_at", "created_at"),
        Index("ix_notification_messages_status_scheduled_at", "status", "scheduled_at"),
        Index("ix_notification_messages_lock_expires_at", "lock_expires_at"),
    )

    channel_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notification_channels.id"),
        nullable=True,
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notification_templates.id"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="normal")
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recipient_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    automation_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("automation_runs.id"),
        nullable=True,
    )
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    simulated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_metadata: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    locked_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lock_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    channel: Mapped[NotificationChannel | None] = relationship(
        "NotificationChannel",
        back_populates="messages",
    )
    template: Mapped[NotificationTemplate | None] = relationship(
        "NotificationTemplate",
        back_populates="messages",
    )
    automation_run: Mapped[AutomationRun | None] = relationship(
        "AutomationRun",
        foreign_keys=[automation_run_id],
    )
    created_by: Mapped[User | None] = relationship("User", foreign_keys=[created_by_id])
    delivery_attempts: Mapped[list[NotificationDeliveryAttempt]] = relationship(
        "NotificationDeliveryAttempt",
        back_populates="message",
    )


class NotificationDeliveryAttempt(UUIDPrimaryKeyMixin, TimestampMixin, CompanyScopedMixin, Base):
    __tablename__ = "notification_delivery_attempts"
    __table_args__ = (
        Index("ix_notification_delivery_attempts_message_id", "message_id"),
        Index("ix_notification_delivery_attempts_status", "status"),
        Index("ix_notification_delivery_attempts_provider", "provider"),
        Index("ix_notification_delivery_attempts_attempt_number", "attempt_number"),
        Index("ix_notification_delivery_attempts_started_at", "started_at"),
        Index("ix_notification_delivery_attempts_finished_at", "finished_at"),
        Index("ix_notification_delivery_attempts_created_at", "created_at"),
        Index("ix_notification_delivery_attempts_worker_instance_id", "worker_instance_id"),
    )

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notification_messages.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    provider: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provider_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    request_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    worker_instance_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    message: Mapped[NotificationMessage] = relationship(
        "NotificationMessage",
        back_populates="delivery_attempts",
    )
