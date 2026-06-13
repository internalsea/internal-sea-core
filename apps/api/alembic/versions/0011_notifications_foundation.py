"""notifications foundation

Revision ID: 0011
Revises: 0010
Create Date: 2026-06-12

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0011"
down_revision: str | None = "0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TIMESTAMP_COLUMNS = (
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
)


def upgrade() -> None:
    op.create_table(
        "notification_channels",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("channel_type", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("endpoint_url", sa.String(length=2048), nullable=True),
        sa.Column("default_recipient", sa.String(length=255), nullable=True),
        sa.Column("provider_config", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_notification_channels_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_channels")),
        sa.UniqueConstraint("name", name="uq_notification_channels_name"),
    )
    op.create_index(
        "ix_notification_channels_name",
        "notification_channels",
        ["name"],
    )
    op.create_index(
        "ix_notification_channels_channel_type",
        "notification_channels",
        ["channel_type"],
    )
    op.create_index(
        "ix_notification_channels_status",
        "notification_channels",
        ["status"],
    )
    op.create_index(
        "ix_notification_channels_created_by_id",
        "notification_channels",
        ["created_by_id"],
    )

    op.create_table(
        "notification_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("event_type", sa.String(length=50), nullable=True),
        sa.Column("subject_template", sa.String(length=500), nullable=True),
        sa.Column("body_template", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_notification_templates_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_templates")),
        sa.UniqueConstraint("name", name="uq_notification_templates_name"),
    )
    op.create_index(
        "ix_notification_templates_name",
        "notification_templates",
        ["name"],
    )
    op.create_index(
        "ix_notification_templates_status",
        "notification_templates",
        ["status"],
    )
    op.create_index(
        "ix_notification_templates_event_type",
        "notification_templates",
        ["event_type"],
    )
    op.create_index(
        "ix_notification_templates_created_by_id",
        "notification_templates",
        ["created_by_id"],
    )

    op.create_table(
        "notification_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("channel_type", sa.String(length=50), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["people.id"],
            name=op.f("fk_notification_preferences_person_id_people"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_notification_preferences_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_preferences")),
        sa.UniqueConstraint(
            "user_id",
            "person_id",
            "channel_type",
            "event_type",
            name="uq_notification_preferences_user_person_channel_event",
        ),
    )
    op.create_index(
        "ix_notification_preferences_user_id",
        "notification_preferences",
        ["user_id"],
    )
    op.create_index(
        "ix_notification_preferences_person_id",
        "notification_preferences",
        ["person_id"],
    )
    op.create_index(
        "ix_notification_preferences_channel_type",
        "notification_preferences",
        ["channel_type"],
    )
    op.create_index(
        "ix_notification_preferences_event_type",
        "notification_preferences",
        ["event_type"],
    )
    op.create_index(
        "ix_notification_preferences_is_enabled",
        "notification_preferences",
        ["is_enabled"],
    )

    op.create_table(
        "notification_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column(
            "priority",
            sa.String(length=50),
            nullable=False,
            server_default="normal",
        ),
        sa.Column(
            "event_type",
            sa.String(length=50),
            nullable=False,
            server_default="manual",
        ),
        sa.Column("subject", sa.String(length=500), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("recipient_type", sa.String(length=50), nullable=True),
        sa.Column("recipient_value", sa.String(length=255), nullable=True),
        sa.Column("entity_type", sa.String(length=50), nullable=True),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("automation_run_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("simulated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["automation_run_id"],
            ["automation_runs.id"],
            name=op.f("fk_notification_messages_automation_run_id_automation_runs"),
        ),
        sa.ForeignKeyConstraint(
            ["channel_id"],
            ["notification_channels.id"],
            name=op.f("fk_notification_messages_channel_id_notification_channels"),
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_notification_messages_created_by_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["template_id"],
            ["notification_templates.id"],
            name=op.f("fk_notification_messages_template_id_notification_templates"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_messages")),
    )
    op.create_index(
        "ix_notification_messages_channel_id",
        "notification_messages",
        ["channel_id"],
    )
    op.create_index(
        "ix_notification_messages_template_id",
        "notification_messages",
        ["template_id"],
    )
    op.create_index(
        "ix_notification_messages_status",
        "notification_messages",
        ["status"],
    )
    op.create_index(
        "ix_notification_messages_priority",
        "notification_messages",
        ["priority"],
    )
    op.create_index(
        "ix_notification_messages_event_type",
        "notification_messages",
        ["event_type"],
    )
    op.create_index(
        "ix_notification_messages_recipient_type_value",
        "notification_messages",
        ["recipient_type", "recipient_value"],
    )
    op.create_index(
        "ix_notification_messages_entity_type_id",
        "notification_messages",
        ["entity_type", "entity_id"],
    )
    op.create_index(
        "ix_notification_messages_automation_run_id",
        "notification_messages",
        ["automation_run_id"],
    )
    op.create_index(
        "ix_notification_messages_created_by_id",
        "notification_messages",
        ["created_by_id"],
    )
    op.create_index(
        "ix_notification_messages_scheduled_at",
        "notification_messages",
        ["scheduled_at"],
    )
    op.create_index(
        "ix_notification_messages_sent_at",
        "notification_messages",
        ["sent_at"],
    )
    op.create_index(
        "ix_notification_messages_simulated_at",
        "notification_messages",
        ["simulated_at"],
    )
    op.create_index(
        "ix_notification_messages_created_at",
        "notification_messages",
        ["created_at"],
    )

    op.create_table(
        "notification_delivery_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("provider", sa.String(length=100), nullable=True),
        sa.Column("provider_message_id", sa.String(length=255), nullable=True),
        sa.Column("request_payload", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("response_payload", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["notification_messages.id"],
            name=op.f("fk_notification_delivery_attempts_message_id_notification_messages"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_delivery_attempts")),
    )
    op.create_index(
        "ix_notification_delivery_attempts_message_id",
        "notification_delivery_attempts",
        ["message_id"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_status",
        "notification_delivery_attempts",
        ["status"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_provider",
        "notification_delivery_attempts",
        ["provider"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_attempt_number",
        "notification_delivery_attempts",
        ["attempt_number"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_started_at",
        "notification_delivery_attempts",
        ["started_at"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_finished_at",
        "notification_delivery_attempts",
        ["finished_at"],
    )
    op.create_index(
        "ix_notification_delivery_attempts_created_at",
        "notification_delivery_attempts",
        ["created_at"],
    )


def downgrade() -> None:
    op.drop_table("notification_delivery_attempts")
    op.drop_table("notification_messages")
    op.drop_table("notification_preferences")
    op.drop_table("notification_templates")
    op.drop_table("notification_channels")
