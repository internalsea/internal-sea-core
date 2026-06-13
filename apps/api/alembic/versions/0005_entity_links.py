"""create entity_links table

Revision ID: 0005
Revises: 0004
Create Date: 2026-06-12

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005"
down_revision: str | None = "0004"
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
        "entity_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("link_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.CheckConstraint(
            "NOT (source_type = target_type AND source_id = target_id)",
            name="ck_entity_links_no_self_link",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_entity_links_created_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_entity_links")),
        sa.UniqueConstraint(
            "source_type",
            "source_id",
            "target_type",
            "target_id",
            "link_type",
            name="uq_entity_links_source_target_type",
        ),
    )
    op.create_index(
        "ix_entity_links_source_type_source_id",
        "entity_links",
        ["source_type", "source_id"],
        unique=False,
    )
    op.create_index(
        "ix_entity_links_target_type_target_id",
        "entity_links",
        ["target_type", "target_id"],
        unique=False,
    )
    op.create_index(
        "ix_entity_links_source_target",
        "entity_links",
        ["source_type", "source_id", "target_type", "target_id"],
        unique=False,
    )
    op.create_index("ix_entity_links_link_type", "entity_links", ["link_type"], unique=False)
    op.create_index(
        "ix_entity_links_created_by_id", "entity_links", ["created_by_id"], unique=False
    )
    op.create_index("ix_entity_links_created_at", "entity_links", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_entity_links_created_at", table_name="entity_links")
    op.drop_index("ix_entity_links_created_by_id", table_name="entity_links")
    op.drop_index("ix_entity_links_link_type", table_name="entity_links")
    op.drop_index("ix_entity_links_source_target", table_name="entity_links")
    op.drop_index("ix_entity_links_target_type_target_id", table_name="entity_links")
    op.drop_index("ix_entity_links_source_type_source_id", table_name="entity_links")
    op.drop_table("entity_links")
