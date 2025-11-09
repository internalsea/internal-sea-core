# alembic/versions/20251109_seed_roles.py
from alembic import op

revision = "20251109_seed_roles"
down_revision = "ceb7d2b08176"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        INSERT INTO roles (name, description, created_at, updated_at)
        VALUES
          ('org_admin','Org Admin', now(), now()),
          ('member','Member', now(), now()),
          ('viewer','Viewer', now(), now()),
          ('team_manager','Team Manager', now(), now())
        ON CONFLICT (name) DO NOTHING;
    """)

def downgrade():
    op.execute("""
        DELETE FROM roles
        WHERE name IN ('org_admin','member','viewer','team_manager');
    """)
