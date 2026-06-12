"""create projects table and link work items

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-06

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
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
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "project_type",
            sa.String(length=50),
            server_default="client_project",
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            server_default="idea",
            nullable=False,
        ),
        sa.Column("client_name", sa.String(length=255), nullable=True),
        sa.Column("account_name", sa.String(length=255), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("capability_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("target_end_date", sa.Date(), nullable=True),
        sa.Column("actual_end_date", sa.Date(), nullable=True),
        sa.Column("budget_amount", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("budget_currency", sa.String(length=10), server_default="EUR", nullable=True),
        sa.Column("priority", sa.String(length=50), nullable=True),
        sa.Column("health_status", sa.String(length=50), nullable=True),
        sa.Column("delivery_notes", sa.Text(), nullable=True),
        *TIMESTAMP_COLUMNS,
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["people.id"],
            name=op.f("fk_projects_owner_id_people"),
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_projects_team_id_teams"),
        ),
        sa.ForeignKeyConstraint(
            ["capability_id"],
            ["capabilities.id"],
            name=op.f("fk_projects_capability_id_capabilities"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_projects")),
    )
    op.create_index("ix_projects_name", "projects", ["name"], unique=False)
    op.create_index("ix_projects_project_type", "projects", ["project_type"], unique=False)
    op.create_index("ix_projects_status", "projects", ["status"], unique=False)
    op.create_index("ix_projects_client_name", "projects", ["client_name"], unique=False)
    op.create_index("ix_projects_owner_id", "projects", ["owner_id"], unique=False)
    op.create_index("ix_projects_team_id", "projects", ["team_id"], unique=False)
    op.create_index("ix_projects_capability_id", "projects", ["capability_id"], unique=False)
    op.create_index("ix_projects_start_date", "projects", ["start_date"], unique=False)
    op.create_index("ix_projects_target_end_date", "projects", ["target_end_date"], unique=False)

    op.add_column(
        "work_items",
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        op.f("fk_work_items_project_id_projects"),
        "work_items",
        "projects",
        ["project_id"],
        ["id"],
    )
    op.create_index("ix_work_items_project_id", "work_items", ["project_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_work_items_project_id", table_name="work_items")
    op.drop_constraint(op.f("fk_work_items_project_id_projects"), "work_items", type_="foreignkey")
    op.drop_column("work_items", "project_id")

    op.drop_index("ix_projects_target_end_date", table_name="projects")
    op.drop_index("ix_projects_start_date", table_name="projects")
    op.drop_index("ix_projects_capability_id", table_name="projects")
    op.drop_index("ix_projects_team_id", table_name="projects")
    op.drop_index("ix_projects_owner_id", table_name="projects")
    op.drop_index("ix_projects_client_name", table_name="projects")
    op.drop_index("ix_projects_status", table_name="projects")
    op.drop_index("ix_projects_project_type", table_name="projects")
    op.drop_index("ix_projects_name", table_name="projects")
    op.drop_table("projects")
