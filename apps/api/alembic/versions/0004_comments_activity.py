"""add project comments and activity events

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-12

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(op.f("ck_comments_target_required"), "comments", type_="check")
    op.add_column("comments", sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        op.f("fk_comments_project_id_projects"),
        "comments",
        "projects",
        ["project_id"],
        ["id"],
    )
    op.create_check_constraint(
        op.f("ck_comments_target_required"),
        "comments",
        "data_product_id IS NOT NULL OR work_item_id IS NOT NULL OR project_id IS NOT NULL",
    )

    op.create_table(
        "activity_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("details", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["users.id"],
            name=op.f("fk_activity_events_actor_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_activity_events")),
    )
    op.create_index(
        "ix_activity_events_entity_type_entity_id",
        "activity_events",
        ["entity_type", "entity_id"],
        unique=False,
    )
    op.create_index("ix_activity_events_action", "activity_events", ["action"], unique=False)
    op.create_index("ix_activity_events_actor_id", "activity_events", ["actor_id"], unique=False)
    op.create_index(
        "ix_activity_events_created_at", "activity_events", ["created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_activity_events_created_at", table_name="activity_events")
    op.drop_index("ix_activity_events_actor_id", table_name="activity_events")
    op.drop_index("ix_activity_events_action", table_name="activity_events")
    op.drop_index("ix_activity_events_entity_type_entity_id", table_name="activity_events")
    op.drop_table("activity_events")

    op.drop_constraint(op.f("ck_comments_target_required"), "comments", type_="check")
    op.drop_constraint(op.f("fk_comments_project_id_projects"), "comments", type_="foreignkey")
    op.drop_column("comments", "project_id")
    op.create_check_constraint(
        op.f("ck_comments_target_required"),
        "comments",
        "data_product_id IS NOT NULL OR work_item_id IS NOT NULL",
    )
