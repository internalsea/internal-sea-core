"""automation foundation

Revision ID: 0009
Revises: 0008
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

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
        "automation_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "frequency",
            sa.String(length=50),
            nullable=False,
            server_default="monthly",
        ),
        sa.Column("timezone", sa.String(length=100), nullable=True, server_default="UTC"),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cron_expression", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_automation_schedules_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_automation_schedules")),
    )
    op.create_index("ix_automation_schedules_name", "automation_schedules", ["name"], unique=False)
    op.create_index(
        "ix_automation_schedules_frequency", "automation_schedules", ["frequency"], unique=False
    )
    op.create_index(
        "ix_automation_schedules_is_active", "automation_schedules", ["is_active"], unique=False
    )
    op.create_index(
        "ix_automation_schedules_next_run_at", "automation_schedules", ["next_run_at"], unique=False
    )
    op.create_index(
        "ix_automation_schedules_last_run_at", "automation_schedules", ["last_run_at"], unique=False
    )
    op.create_index(
        "ix_automation_schedules_created_by_id",
        "automation_schedules",
        ["created_by_id"],
        unique=False,
    )

    op.create_table(
        "automation_triggers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column(
            "trigger_type",
            sa.String(length=50),
            nullable=False,
            server_default="schedule",
        ),
        sa.Column("action_type", sa.String(length=50), nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("target_type", sa.String(length=50), nullable=True),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("conditions", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("action_config", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["automation_schedules.id"],
            name=op.f("fk_automation_triggers_schedule_id_automation_schedules"),
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_automation_triggers_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_automation_triggers")),
    )
    op.create_index("ix_automation_triggers_name", "automation_triggers", ["name"], unique=False)
    op.create_index("ix_automation_triggers_status", "automation_triggers", ["status"], unique=False)
    op.create_index(
        "ix_automation_triggers_trigger_type", "automation_triggers", ["trigger_type"], unique=False
    )
    op.create_index(
        "ix_automation_triggers_action_type", "automation_triggers", ["action_type"], unique=False
    )
    op.create_index(
        "ix_automation_triggers_schedule_id", "automation_triggers", ["schedule_id"], unique=False
    )
    op.create_index(
        "ix_automation_triggers_target_type_target_id",
        "automation_triggers",
        ["target_type", "target_id"],
        unique=False,
    )
    op.create_index(
        "ix_automation_triggers_created_by_id",
        "automation_triggers",
        ["created_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_automation_triggers_last_run_at", "automation_triggers", ["last_run_at"], unique=False
    )
    op.create_index(
        "ix_automation_triggers_next_run_at", "automation_triggers", ["next_run_at"], unique=False
    )

    op.create_table(
        "automation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("trigger_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("target_type", sa.String(length=50), nullable=True),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action_type", sa.String(length=50), nullable=True),
        sa.Column("result_summary", sa.Text(), nullable=True),
        sa.Column("result_details", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("executed_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["trigger_id"],
            ["automation_triggers.id"],
            name=op.f("fk_automation_runs_trigger_id_automation_triggers"),
        ),
        sa.ForeignKeyConstraint(
            ["executed_by_id"],
            ["users.id"],
            name=op.f("fk_automation_runs_executed_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_automation_runs")),
    )
    op.create_index("ix_automation_runs_trigger_id", "automation_runs", ["trigger_id"], unique=False)
    op.create_index("ix_automation_runs_status", "automation_runs", ["status"], unique=False)
    op.create_index(
        "ix_automation_runs_started_at", "automation_runs", ["started_at"], unique=False
    )
    op.create_index(
        "ix_automation_runs_finished_at", "automation_runs", ["finished_at"], unique=False
    )
    op.create_index(
        "ix_automation_runs_target_type_target_id",
        "automation_runs",
        ["target_type", "target_id"],
        unique=False,
    )
    op.create_index(
        "ix_automation_runs_action_type", "automation_runs", ["action_type"], unique=False
    )
    op.create_index(
        "ix_automation_runs_executed_by_id", "automation_runs", ["executed_by_id"], unique=False
    )
    op.create_index(
        "ix_automation_runs_created_at", "automation_runs", ["created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_table("automation_runs")
    op.drop_table("automation_triggers")
    op.drop_table("automation_schedules")
