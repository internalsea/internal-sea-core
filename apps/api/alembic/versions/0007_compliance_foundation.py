"""create compliance foundation tables

Revision ID: 0007
Revises: 0006
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007"
down_revision: Union[str, None] = "0006"
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
        "policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_policies_owner_id_people"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_policies")),
        sa.UniqueConstraint("name", name="uq_policies_name"),
    )
    op.create_index("ix_policies_name", "policies", ["name"], unique=False)
    op.create_index("ix_policies_status", "policies", ["status"], unique=False)
    op.create_index("ix_policies_owner_id", "policies", ["owner_id"], unique=False)
    op.create_index("ix_policies_effective_from", "policies", ["effective_from"], unique=False)
    op.create_index("ix_policies_effective_to", "policies", ["effective_to"], unique=False)

    op.create_table(
        "compliance_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "severity",
            sa.String(length=50),
            nullable=False,
            server_default="medium",
        ),
        sa.Column("subject_type", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["policy_id"],
            ["policies.id"],
            name=op.f("fk_compliance_rules_policy_id_policies"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_compliance_rules")),
    )
    op.create_index(
        "ix_compliance_rules_policy_id", "compliance_rules", ["policy_id"], unique=False
    )
    op.create_index("ix_compliance_rules_code", "compliance_rules", ["code"], unique=False)
    op.create_index("ix_compliance_rules_name", "compliance_rules", ["name"], unique=False)
    op.create_index(
        "ix_compliance_rules_severity", "compliance_rules", ["severity"], unique=False
    )
    op.create_index(
        "ix_compliance_rules_subject_type", "compliance_rules", ["subject_type"], unique=False
    )
    op.create_index(
        "ix_compliance_rules_is_active", "compliance_rules", ["is_active"], unique=False
    )

    op.create_table(
        "controls",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "control_type",
            sa.String(length=50),
            nullable=False,
            server_default="manual",
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="active",
        ),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("frequency", sa.String(length=50), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["rule_id"],
            ["compliance_rules.id"],
            name=op.f("fk_controls_rule_id_compliance_rules"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_controls_owner_id_people"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_controls")),
    )
    op.create_index("ix_controls_rule_id", "controls", ["rule_id"], unique=False)
    op.create_index("ix_controls_control_type", "controls", ["control_type"], unique=False)
    op.create_index("ix_controls_status", "controls", ["status"], unique=False)
    op.create_index("ix_controls_owner_id", "controls", ["owner_id"], unique=False)
    op.create_index("ix_controls_frequency", "controls", ["frequency"], unique=False)

    op.create_table(
        "compliance_checks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("control_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("subject_type", sa.String(length=50), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "check_type",
            sa.String(length=50),
            nullable=False,
            server_default="manual",
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="not_started",
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("result_summary", sa.Text(), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_check_at", sa.DateTime(timezone=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["rule_id"],
            ["compliance_rules.id"],
            name=op.f("fk_compliance_checks_rule_id_compliance_rules"),
        ),
        sa.ForeignKeyConstraint(
            ["control_id"],
            ["controls.id"],
            name=op.f("fk_compliance_checks_control_id_controls"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_compliance_checks_owner_id_people"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_compliance_checks")),
    )
    op.create_index("ix_compliance_checks_rule_id", "compliance_checks", ["rule_id"], unique=False)
    op.create_index(
        "ix_compliance_checks_control_id", "compliance_checks", ["control_id"], unique=False
    )
    op.create_index(
        "ix_compliance_checks_subject",
        "compliance_checks",
        ["subject_type", "subject_id"],
        unique=False,
    )
    op.create_index("ix_compliance_checks_status", "compliance_checks", ["status"], unique=False)
    op.create_index(
        "ix_compliance_checks_check_type", "compliance_checks", ["check_type"], unique=False
    )
    op.create_index(
        "ix_compliance_checks_owner_id", "compliance_checks", ["owner_id"], unique=False
    )
    op.create_index(
        "ix_compliance_checks_due_date", "compliance_checks", ["due_date"], unique=False
    )
    op.create_index(
        "ix_compliance_checks_completed_at", "compliance_checks", ["completed_at"], unique=False
    )
    op.create_index(
        "ix_compliance_checks_next_check_at",
        "compliance_checks",
        ["next_check_at"],
        unique=False,
    )

    op.create_table(
        "compliance_check_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("compliance_check_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="submitted",
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("submitted_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["compliance_check_id"],
            ["compliance_checks.id"],
            name=op.f("fk_compliance_check_evidence_compliance_check_id_compliance_checks"),
        ),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["file_assets.id"],
            name=op.f("fk_compliance_check_evidence_file_id_file_assets"),
        ),
        sa.ForeignKeyConstraint(
            ["submitted_by_id"],
            ["users.id"],
            name=op.f("fk_compliance_check_evidence_submitted_by_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["reviewed_by_id"],
            ["users.id"],
            name=op.f("fk_compliance_check_evidence_reviewed_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_compliance_check_evidence")),
        sa.UniqueConstraint(
            "compliance_check_id",
            "file_id",
            name="uq_compliance_check_evidence_check_file",
        ),
    )
    op.create_index(
        "ix_compliance_check_evidence_check_id",
        "compliance_check_evidence",
        ["compliance_check_id"],
        unique=False,
    )
    op.create_index(
        "ix_compliance_check_evidence_file_id",
        "compliance_check_evidence",
        ["file_id"],
        unique=False,
    )
    op.create_index(
        "ix_compliance_check_evidence_status",
        "compliance_check_evidence",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_compliance_check_evidence_submitted_by_id",
        "compliance_check_evidence",
        ["submitted_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_compliance_check_evidence_reviewed_by_id",
        "compliance_check_evidence",
        ["reviewed_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_compliance_check_evidence_reviewed_at",
        "compliance_check_evidence",
        ["reviewed_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_compliance_check_evidence_reviewed_at", table_name="compliance_check_evidence"
    )
    op.drop_index(
        "ix_compliance_check_evidence_reviewed_by_id", table_name="compliance_check_evidence"
    )
    op.drop_index(
        "ix_compliance_check_evidence_submitted_by_id", table_name="compliance_check_evidence"
    )
    op.drop_index("ix_compliance_check_evidence_status", table_name="compliance_check_evidence")
    op.drop_index("ix_compliance_check_evidence_file_id", table_name="compliance_check_evidence")
    op.drop_index("ix_compliance_check_evidence_check_id", table_name="compliance_check_evidence")
    op.drop_table("compliance_check_evidence")

    op.drop_index("ix_compliance_checks_next_check_at", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_completed_at", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_due_date", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_owner_id", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_check_type", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_status", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_subject", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_control_id", table_name="compliance_checks")
    op.drop_index("ix_compliance_checks_rule_id", table_name="compliance_checks")
    op.drop_table("compliance_checks")

    op.drop_index("ix_controls_frequency", table_name="controls")
    op.drop_index("ix_controls_owner_id", table_name="controls")
    op.drop_index("ix_controls_status", table_name="controls")
    op.drop_index("ix_controls_control_type", table_name="controls")
    op.drop_index("ix_controls_rule_id", table_name="controls")
    op.drop_table("controls")

    op.drop_index("ix_compliance_rules_is_active", table_name="compliance_rules")
    op.drop_index("ix_compliance_rules_subject_type", table_name="compliance_rules")
    op.drop_index("ix_compliance_rules_severity", table_name="compliance_rules")
    op.drop_index("ix_compliance_rules_name", table_name="compliance_rules")
    op.drop_index("ix_compliance_rules_code", table_name="compliance_rules")
    op.drop_index("ix_compliance_rules_policy_id", table_name="compliance_rules")
    op.drop_table("compliance_rules")

    op.drop_index("ix_policies_effective_to", table_name="policies")
    op.drop_index("ix_policies_effective_from", table_name="policies")
    op.drop_index("ix_policies_owner_id", table_name="policies")
    op.drop_index("ix_policies_status", table_name="policies")
    op.drop_index("ix_policies_name", table_name="policies")
    op.drop_table("policies")
