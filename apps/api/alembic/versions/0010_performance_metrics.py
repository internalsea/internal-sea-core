"""performance metrics

Revision ID: 0010
Revises: 0009
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0010"
down_revision: Union[str, None] = "0009"
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
        "performance_metric_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("subject_type", sa.String(length=50), nullable=False),
        sa.Column(
            "value_type",
            sa.String(length=50),
            nullable=False,
            server_default="number",
        ),
        sa.Column(
            "direction",
            sa.String(length=50),
            nullable=False,
            server_default="neutral",
        ),
        sa.Column("frequency", sa.String(length=50), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="active",
        ),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("target_value", sa.Numeric(18, 4), nullable=True),
        sa.Column("warning_threshold", sa.Numeric(18, 4), nullable=True),
        sa.Column("critical_threshold", sa.Numeric(18, 4), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_performance_metric_definitions_owner_id_people"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_performance_metric_definitions")),
        sa.UniqueConstraint("code", name="uq_performance_metric_definitions_code"),
    )
    op.create_index(
        "ix_performance_metric_definitions_name",
        "performance_metric_definitions",
        ["name"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_code",
        "performance_metric_definitions",
        ["code"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_subject_type",
        "performance_metric_definitions",
        ["subject_type"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_value_type",
        "performance_metric_definitions",
        ["value_type"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_direction",
        "performance_metric_definitions",
        ["direction"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_status",
        "performance_metric_definitions",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_definitions_owner_id",
        "performance_metric_definitions",
        ["owner_id"],
        unique=False,
    )

    op.create_table(
        "performance_metric_values",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("metric_definition_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_type", sa.String(length=50), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("value_numeric", sa.Numeric(18, 4), nullable=True),
        sa.Column("value_text", sa.Text(), nullable=True),
        sa.Column("value_bool", sa.Boolean(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="submitted",
        ),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("submitted_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approved_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["metric_definition_id"],
            ["performance_metric_definitions.id"],
            name=op.f("fk_performance_metric_values_metric_definition_id_performance_metric_definitions"),
        ),
        sa.ForeignKeyConstraint(
            ["submitted_by_id"],
            ["users.id"],
            name=op.f("fk_performance_metric_values_submitted_by_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["approved_by_id"],
            ["users.id"],
            name=op.f("fk_performance_metric_values_approved_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_performance_metric_values")),
        sa.UniqueConstraint(
            "metric_definition_id",
            "subject_type",
            "subject_id",
            "period_start",
            "period_end",
            name="uq_performance_metric_values_period",
        ),
    )
    op.create_index(
        "ix_performance_metric_values_metric_definition_id",
        "performance_metric_values",
        ["metric_definition_id"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_subject",
        "performance_metric_values",
        ["subject_type", "subject_id"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_period_start",
        "performance_metric_values",
        ["period_start"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_period_end",
        "performance_metric_values",
        ["period_end"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_status",
        "performance_metric_values",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_submitted_by_id",
        "performance_metric_values",
        ["submitted_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_approved_by_id",
        "performance_metric_values",
        ["approved_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_performance_metric_values_created_at",
        "performance_metric_values",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("performance_metric_values")
    op.drop_table("performance_metric_definitions")
