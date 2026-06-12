"""auth permissions

Revision ID: 0008
Revises: 0007
Create Date: 2026-06-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_superuser", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    )
    op.execute("UPDATE users SET is_superuser = is_admin")
    op.drop_column("users", "is_admin")

    op.add_column("users", sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True))

    op.alter_column("users", "full_name", existing_type=sa.String(length=255), nullable=True)


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    )
    op.execute("UPDATE users SET is_admin = is_superuser")
    op.drop_column("users", "is_superuser")

    op.drop_column("users", "last_login_at")

    op.alter_column("users", "full_name", existing_type=sa.String(length=255), nullable=False)
