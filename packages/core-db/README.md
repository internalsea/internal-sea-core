# core-db

Database package for Internal Sea.

This package will contain:

- SQLAlchemy 2.0 models aligned with [docs/DATA_MODEL.md](../../docs/DATA_MODEL.md)
- Database session factory and connection helpers
- Repository or query helpers as patterns emerge
- Alembic migrations (may live here or under `apps/api` — decided in Phase 3)

PostgreSQL is the target database. See [docs/DECISION_LOG.md](../../docs/DECISION_LOG.md) ADR-0004.

Implementation begins in Phase 3.
