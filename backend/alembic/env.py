# alembic/env.py
from __future__ import annotations

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Load app settings / DB URL ---
from app.core.config import settings

# IMPORTANT: import Base and ensure all models are imported
# This import path assumes you placed Base in app/models/base.py
# and __init__.py imports all model classes (as we set up earlier).
from app.models import Base  # re-exports Base and imports all models

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata

def get_url() -> str:
    return settings.DATABASE_URL  # e.g. "postgresql+psycopg2://user:pass@host/db"

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,                 # detect type changes
        compare_server_default=True,       # detect server_default changes
        include_object=_include_object,    # optional filter
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=_include_object,  # optional filter
        )
        with context.begin_transaction():
            context.run_migrations()

def _include_object(object, name, type_, reflected, compare_to):
    # Skip Alembic's own bookkeeping table
    if type_ == "table" and name == "alembic_version":
        return False
    return True

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
