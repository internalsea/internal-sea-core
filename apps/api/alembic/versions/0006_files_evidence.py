"""create file storages, assets and attachments tables

Revision ID: 0006
Revises: 0005
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006"
down_revision: Union[str, None] = "0005"
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
        "file_storages",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("storage_type", sa.String(length=50), nullable=False),
        sa.Column("base_url", sa.String(length=2048), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        *TIMESTAMP_COLUMNS,
        sa.PrimaryKeyConstraint("id", name=op.f("pk_file_storages")),
        sa.UniqueConstraint("name", name="uq_file_storages_name"),
    )
    op.create_index("ix_file_storages_name", "file_storages", ["name"], unique=False)
    op.create_index(
        "ix_file_storages_storage_type", "file_storages", ["storage_type"], unique=False
    )
    op.create_index("ix_file_storages_is_active", "file_storages", ["is_active"], unique=False)

    op.create_table(
        "file_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "file_type",
            sa.String(length=50),
            nullable=False,
            server_default="document",
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "sensitivity",
            sa.String(length=50),
            nullable=False,
            server_default="internal",
        ),
        sa.Column("storage_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("original_filename", sa.String(length=512), nullable=True),
        sa.Column("mime_type", sa.String(length=255), nullable=True),
        sa.Column("file_size_bytes", sa.Integer(), nullable=True),
        sa.Column("external_url", sa.String(length=2048), nullable=True),
        sa.Column("storage_path", sa.String(length=2048), nullable=True),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("uploaded_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["storage_id"],
            ["file_storages.id"],
            name=op.f("fk_file_assets_storage_id_file_storages"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_file_assets_owner_id_people"),
        ),
        sa.ForeignKeyConstraint(
            ["uploaded_by_id"],
            ["users.id"],
            name=op.f("fk_file_assets_uploaded_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_file_assets")),
    )
    op.create_index("ix_file_assets_name", "file_assets", ["name"], unique=False)
    op.create_index("ix_file_assets_file_type", "file_assets", ["file_type"], unique=False)
    op.create_index("ix_file_assets_status", "file_assets", ["status"], unique=False)
    op.create_index("ix_file_assets_sensitivity", "file_assets", ["sensitivity"], unique=False)
    op.create_index("ix_file_assets_storage_id", "file_assets", ["storage_id"], unique=False)
    op.create_index("ix_file_assets_owner_id", "file_assets", ["owner_id"], unique=False)
    op.create_index(
        "ix_file_assets_uploaded_by_id", "file_assets", ["uploaded_by_id"], unique=False
    )
    op.create_index("ix_file_assets_created_at", "file_assets", ["created_at"], unique=False)
    op.create_index("ix_file_assets_updated_at", "file_assets", ["updated_at"], unique=False)

    op.create_table(
        "file_attachments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose", sa.String(length=255), nullable=True),
        sa.Column("is_evidence", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("evidence_type", sa.String(length=255), nullable=True),
        sa.Column("attached_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["file_assets.id"],
            name=op.f("fk_file_attachments_file_id_file_assets"),
        ),
        sa.ForeignKeyConstraint(
            ["attached_by_id"],
            ["users.id"],
            name=op.f("fk_file_attachments_attached_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_file_attachments")),
        sa.UniqueConstraint(
            "file_id",
            "entity_type",
            "entity_id",
            "purpose",
            name="uq_file_attachments_file_entity_purpose",
        ),
    )
    op.create_index("ix_file_attachments_file_id", "file_attachments", ["file_id"], unique=False)
    op.create_index(
        "ix_file_attachments_entity_type_entity_id",
        "file_attachments",
        ["entity_type", "entity_id"],
        unique=False,
    )
    op.create_index(
        "ix_file_attachments_entity_evidence",
        "file_attachments",
        ["entity_type", "entity_id", "is_evidence"],
        unique=False,
    )
    op.create_index(
        "ix_file_attachments_is_evidence", "file_attachments", ["is_evidence"], unique=False
    )
    op.create_index(
        "ix_file_attachments_evidence_type", "file_attachments", ["evidence_type"], unique=False
    )
    op.create_index(
        "ix_file_attachments_attached_by_id",
        "file_attachments",
        ["attached_by_id"],
        unique=False,
    )
    op.create_index(
        "ix_file_attachments_created_at", "file_attachments", ["created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_file_attachments_created_at", table_name="file_attachments")
    op.drop_index("ix_file_attachments_attached_by_id", table_name="file_attachments")
    op.drop_index("ix_file_attachments_evidence_type", table_name="file_attachments")
    op.drop_index("ix_file_attachments_is_evidence", table_name="file_attachments")
    op.drop_index("ix_file_attachments_entity_evidence", table_name="file_attachments")
    op.drop_index("ix_file_attachments_entity_type_entity_id", table_name="file_attachments")
    op.drop_index("ix_file_attachments_file_id", table_name="file_attachments")
    op.drop_table("file_attachments")

    op.drop_index("ix_file_assets_updated_at", table_name="file_assets")
    op.drop_index("ix_file_assets_created_at", table_name="file_assets")
    op.drop_index("ix_file_assets_uploaded_by_id", table_name="file_assets")
    op.drop_index("ix_file_assets_owner_id", table_name="file_assets")
    op.drop_index("ix_file_assets_storage_id", table_name="file_assets")
    op.drop_index("ix_file_assets_sensitivity", table_name="file_assets")
    op.drop_index("ix_file_assets_status", table_name="file_assets")
    op.drop_index("ix_file_assets_file_type", table_name="file_assets")
    op.drop_index("ix_file_assets_name", table_name="file_assets")
    op.drop_table("file_assets")

    op.drop_index("ix_file_storages_is_active", table_name="file_storages")
    op.drop_index("ix_file_storages_storage_type", table_name="file_storages")
    op.drop_index("ix_file_storages_name", table_name="file_storages")
    op.drop_table("file_storages")
