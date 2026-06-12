"""saas tenant foundation

Revision ID: 0013
Revises: 0012
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TENANT_TABLES_COMPANY_WORKSPACE = (
    "people",
    "teams",
    "capabilities",
    "business_domains",
    "data_products",
    "work_items",
    "projects",
    "entity_links",
    "file_assets",
    "file_attachments",
    "compliance_checks",
    "automation_triggers",
    "performance_metric_values",
    "notification_messages",
)

TENANT_TABLES_COMPANY_ONLY = (
    "comments",
    "activity_events",
    "file_storages",
    "policies",
    "compliance_rules",
    "controls",
    "compliance_check_evidence",
    "automation_schedules",
    "automation_runs",
    "performance_metric_definitions",
    "notification_channels",
    "notification_templates",
    "notification_preferences",
    "notification_delivery_attempts",
)


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("industry", sa.String(length=50), nullable=True),
        sa.Column("company_size", sa.String(length=50), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("website", sa.String(length=2048), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="trial"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="uq_companies_slug"),
    )
    op.create_index("ix_companies_name", "companies", ["name"])
    op.create_index("ix_companies_slug", "companies", ["slug"])
    op.create_index("ix_companies_status", "companies", ["status"])
    op.create_index("ix_companies_industry", "companies", ["industry"])
    op.create_index("ix_companies_country", "companies", ["country"])

    op.create_table(
        "workspaces",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("default_timezone", sa.String(length=100), nullable=True, server_default="UTC"),
        sa.Column("default_currency", sa.String(length=10), nullable=True, server_default="EUR"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id", "slug", name="uq_workspaces_company_slug"),
    )
    op.create_index("ix_workspaces_company_id", "workspaces", ["company_id"])
    op.create_index("ix_workspaces_slug", "workspaces", ["slug"])
    op.create_index("ix_workspaces_status", "workspaces", ["status"])

    op.create_table(
        "company_members",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("person_id", sa.UUID(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="viewer"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["person_id"], ["people.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id", "user_id", name="uq_company_members_company_user"),
    )
    op.create_index("ix_company_members_company_id", "company_members", ["company_id"])
    op.create_index("ix_company_members_user_id", "company_members", ["user_id"])
    op.create_index("ix_company_members_person_id", "company_members", ["person_id"])
    op.create_index("ix_company_members_role", "company_members", ["role"])
    op.create_index("ix_company_members_status", "company_members", ["status"])

    for table in TENANT_TABLES_COMPANY_WORKSPACE:
        op.add_column(table, sa.Column("company_id", sa.UUID(), nullable=True))
        op.add_column(table, sa.Column("workspace_id", sa.UUID(), nullable=True))
        op.create_index(f"ix_{table}_company_id", table, ["company_id"])
        op.create_index(f"ix_{table}_workspace_id", table, ["workspace_id"])
        op.create_foreign_key(
            f"fk_{table}_company_id_companies",
            table,
            "companies",
            ["company_id"],
            ["id"],
        )
        op.create_foreign_key(
            f"fk_{table}_workspace_id_workspaces",
            table,
            "workspaces",
            ["workspace_id"],
            ["id"],
        )

    for table in TENANT_TABLES_COMPANY_ONLY:
        op.add_column(table, sa.Column("company_id", sa.UUID(), nullable=True))
        op.create_index(f"ix_{table}_company_id", table, ["company_id"])
        op.create_foreign_key(
            f"fk_{table}_company_id_companies",
            table,
            "companies",
            ["company_id"],
            ["id"],
        )


def downgrade() -> None:
    for table in TENANT_TABLES_COMPANY_ONLY:
        op.drop_constraint(f"fk_{table}_company_id_companies", table, type_="foreignkey")
        op.drop_index(f"ix_{table}_company_id", table_name=table)
        op.drop_column(table, "company_id")

    for table in TENANT_TABLES_COMPANY_WORKSPACE:
        op.drop_constraint(f"fk_{table}_workspace_id_workspaces", table, type_="foreignkey")
        op.drop_constraint(f"fk_{table}_company_id_companies", table, type_="foreignkey")
        op.drop_index(f"ix_{table}_workspace_id", table_name=table)
        op.drop_index(f"ix_{table}_company_id", table_name=table)
        op.drop_column(table, "workspace_id")
        op.drop_column(table, "company_id")

    op.drop_table("company_members")
    op.drop_table("workspaces")
    op.drop_table("companies")
