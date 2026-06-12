# core-domain

Shared domain package for Internal Sea.

This package will contain:

- Domain constants and enumerations (status values, object types)
- Shared business rules that do not depend on HTTP or the database
- Value objects and validation helpers used by the API and other packages

Keep this package free of FastAPI, SQLAlchemy and external I/O so it stays easy to test.

Implementation begins in Phase 2–3. See [docs/TECHNICAL_GUIDELINES.md](../../docs/TECHNICAL_GUIDELINES.md).
