"""worker execution foundation

Revision ID: 0012
Revises: 0011
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0012"
down_revision: Union[str, None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "automation_triggers",
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "automation_triggers",
        sa.Column("locked_by", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "automation_triggers",
        sa.Column("lock_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_automation_triggers_status_next_run_at",
        "automation_triggers",
        ["status", "next_run_at"],
    )
    op.create_index(
        "ix_automation_triggers_lock_expires_at",
        "automation_triggers",
        ["lock_expires_at"],
    )

    op.add_column(
        "automation_runs",
        sa.Column("worker_instance_id", sa.String(length=255), nullable=True),
    )
    op.create_index(
        "ix_automation_runs_worker_instance_id",
        "automation_runs",
        ["worker_instance_id"],
    )

    op.add_column(
        "notification_messages",
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notification_messages",
        sa.Column("locked_by", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "notification_messages",
        sa.Column("lock_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_notification_messages_status_scheduled_at",
        "notification_messages",
        ["status", "scheduled_at"],
    )
    op.create_index(
        "ix_notification_messages_lock_expires_at",
        "notification_messages",
        ["lock_expires_at"],
    )

    op.add_column(
        "notification_delivery_attempts",
        sa.Column("worker_instance_id", sa.String(length=255), nullable=True),
    )
    op.create_index(
        "ix_notification_delivery_attempts_worker_instance_id",
        "notification_delivery_attempts",
        ["worker_instance_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_notification_delivery_attempts_worker_instance_id",
        table_name="notification_delivery_attempts",
    )
    op.drop_column("notification_delivery_attempts", "worker_instance_id")

    op.drop_index("ix_notification_messages_lock_expires_at", table_name="notification_messages")
    op.drop_index(
        "ix_notification_messages_status_scheduled_at",
        table_name="notification_messages",
    )
    op.drop_column("notification_messages", "lock_expires_at")
    op.drop_column("notification_messages", "locked_by")
    op.drop_column("notification_messages", "locked_at")

    op.drop_index("ix_automation_runs_worker_instance_id", table_name="automation_runs")
    op.drop_column("automation_runs", "worker_instance_id")

    op.drop_index("ix_automation_triggers_lock_expires_at", table_name="automation_triggers")
    op.drop_index("ix_automation_triggers_status_next_run_at", table_name="automation_triggers")
    op.drop_column("automation_triggers", "lock_expires_at")
    op.drop_column("automation_triggers", "locked_by")
    op.drop_column("automation_triggers", "locked_at")
