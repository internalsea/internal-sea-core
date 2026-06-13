"""create core domain models

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-06

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: str | None = "0001"
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
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), server_default="viewer", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        *TIMESTAMP_COLUMNS,
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.UniqueConstraint("name", name=op.f("uq_teams_name")),
    )

    op.create_table(
        "capabilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.PrimaryKeyConstraint("id", name=op.f("pk_capabilities")),
        sa.UniqueConstraint("name", name=op.f("uq_capabilities_name")),
    )

    op.create_table(
        "people",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("role_title", sa.String(length=255), nullable=True),
        sa.Column("seniority_level", sa.String(length=50), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("capability_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("availability_percent", sa.Integer(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        *TIMESTAMP_COLUMNS,
        sa.CheckConstraint(
            "availability_percent IS NULL OR "
            "(availability_percent >= 0 AND availability_percent <= 100)",
            name=op.f("ck_people_availability_percent_range"),
        ),
        sa.ForeignKeyConstraint(
            ["capability_id"],
            ["capabilities.id"],
            name=op.f("fk_people_capability_id_capabilities"),
        ),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], name=op.f("fk_people_team_id_teams")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_people_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_people")),
        sa.UniqueConstraint("email", name=op.f("uq_people_email")),
        sa.UniqueConstraint("user_id", name=op.f("uq_people_user_id")),
    )
    op.create_index("ix_people_email", "people", ["email"], unique=False)

    op.create_table(
        "business_domains",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["owner_id"], ["people.id"], name=op.f("fk_business_domains_owner_id_people")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_business_domains")),
        sa.UniqueConstraint("name", name=op.f("uq_business_domains_name")),
    )

    op.create_table(
        "data_products",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=50), server_default="dataset", nullable=False),
        sa.Column("status", sa.String(length=50), server_default="draft", nullable=False),
        sa.Column("quality_status", sa.String(length=50), server_default="unknown", nullable=False),
        sa.Column("business_domain_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("business_owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("technical_owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("capability_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("refresh_frequency", sa.String(length=100), nullable=True),
        sa.Column("source_systems", sa.Text(), nullable=True),
        sa.Column("consumers", sa.Text(), nullable=True),
        sa.Column("documentation_url", sa.String(length=2048), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["business_domain_id"],
            ["business_domains.id"],
            name=op.f("fk_data_products_business_domain_id_business_domains"),
        ),
        sa.ForeignKeyConstraint(
            ["business_owner_id"],
            ["people.id"],
            name=op.f("fk_data_products_business_owner_id_people"),
        ),
        sa.ForeignKeyConstraint(
            ["capability_id"],
            ["capabilities.id"],
            name=op.f("fk_data_products_capability_id_capabilities"),
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_data_products_team_id_teams"),
        ),
        sa.ForeignKeyConstraint(
            ["technical_owner_id"],
            ["people.id"],
            name=op.f("fk_data_products_technical_owner_id_people"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_data_products")),
    )
    op.create_index("ix_data_products_name", "data_products", ["name"], unique=False)
    op.create_index("ix_data_products_status", "data_products", ["status"], unique=False)
    op.create_index("ix_data_products_type", "data_products", ["type"], unique=False)
    op.create_index(
        "ix_data_products_quality_status",
        "data_products",
        ["quality_status"],
        unique=False,
    )
    op.create_index(
        "ix_data_products_business_domain_id",
        "data_products",
        ["business_domain_id"],
        unique=False,
    )
    op.create_index(
        "ix_data_products_capability_id",
        "data_products",
        ["capability_id"],
        unique=False,
    )
    op.create_index("ix_data_products_team_id", "data_products", ["team_id"], unique=False)

    op.create_table(
        "work_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=50), server_default="task", nullable=False),
        sa.Column("status", sa.String(length=50), server_default="backlog", nullable=False),
        sa.Column("priority", sa.String(length=50), server_default="medium", nullable=False),
        sa.Column("assignee_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reporter_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("data_product_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("capability_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("estimate_points", sa.Integer(), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["assignee_id"],
            ["people.id"],
            name=op.f("fk_work_items_assignee_id_people"),
        ),
        sa.ForeignKeyConstraint(
            ["capability_id"],
            ["capabilities.id"],
            name=op.f("fk_work_items_capability_id_capabilities"),
        ),
        sa.ForeignKeyConstraint(
            ["data_product_id"],
            ["data_products.id"],
            name=op.f("fk_work_items_data_product_id_data_products"),
        ),
        sa.ForeignKeyConstraint(
            ["reporter_id"],
            ["users.id"],
            name=op.f("fk_work_items_reporter_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_work_items_team_id_teams"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_work_items")),
    )
    op.create_index("ix_work_items_title", "work_items", ["title"], unique=False)
    op.create_index("ix_work_items_type", "work_items", ["type"], unique=False)
    op.create_index("ix_work_items_status", "work_items", ["status"], unique=False)
    op.create_index("ix_work_items_priority", "work_items", ["priority"], unique=False)
    op.create_index("ix_work_items_assignee_id", "work_items", ["assignee_id"], unique=False)
    op.create_index(
        "ix_work_items_data_product_id",
        "work_items",
        ["data_product_id"],
        unique=False,
    )
    op.create_index(
        "ix_work_items_capability_id",
        "work_items",
        ["capability_id"],
        unique=False,
    )
    op.create_index("ix_work_items_team_id", "work_items", ["team_id"], unique=False)
    op.create_index("ix_work_items_due_date", "work_items", ["due_date"], unique=False)

    op.create_table(
        "comments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("data_product_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("work_item_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.CheckConstraint(
            "data_product_id IS NOT NULL OR work_item_id IS NOT NULL",
            name=op.f("ck_comments_target_required"),
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name=op.f("fk_comments_author_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["data_product_id"],
            ["data_products.id"],
            name=op.f("fk_comments_data_product_id_data_products"),
        ),
        sa.ForeignKeyConstraint(
            ["work_item_id"],
            ["work_items.id"],
            name=op.f("fk_comments_work_item_id_work_items"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comments")),
    )


def downgrade() -> None:
    op.drop_table("comments")
    op.drop_table("work_items")
    op.drop_table("data_products")
    op.drop_table("business_domains")
    op.drop_table("people")
    op.drop_table("capabilities")
    op.drop_table("teams")
    op.drop_table("users")
