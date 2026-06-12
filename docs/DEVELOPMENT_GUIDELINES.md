# Development Guidelines

How we build Internal Sea incrementally — especially when using Cursor or similar AI-assisted workflows.

## Step-by-step with Cursor

1. **Read the roadmap** — Confirm the current phase in [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md).
2. **Scope one slice** — Pick a single vertical feature (e.g. "health endpoint" not "entire catalog").
3. **Prompt with context** — Reference relevant docs (`DATA_MODEL.md`, `TECHNICAL_GUIDELINES.md`) in your prompt.
4. **Review diffs** — Read generated code; reject unrelated changes.
5. **Run checks** — `make api-check`, `make web-check`, or `make check` as applicable.
6. **Update docs** — Adjust roadmap status, decision log, or data model when behavior changes.

## Frontend workflow

```bash
make web-install   # first time
make web-dev       # http://localhost:5173
make web-check     # lint + typecheck + build
```

- Frontend development starts after the first backend API exists (health + at least one resource).
- Implement **one vertical slice** at a time (e.g. catalog list in Prompt 7, not all modules).
- Avoid mock-heavy UI that will be thrown away — use real API clients early.
- Copy `apps/web/.env.example` to `apps/web/.env` if overriding `VITE_API_BASE_URL`.
- Browser must reach API at `http://localhost:8000` — not Docker internal hostnames.

## Prompt-based workflow

Work in **small Cursor prompts** aligned to [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) phases:

1. Complete one prompt scope fully before starting the next.
2. Run **`make api-check`** after each backend prompt.
3. **Commit** after a successful prompt with a clear message.
4. Do **not mix frontend and backend** in the same prompt until the first vertical slice (catalog API + UI).
5. Verify endpoints manually (`/docs` or `curl`) when adding routes.

## Commit discipline

- **Small commits** — One logical change per commit; easy to revert and review.
- **Clear messages** — State why, not only what (e.g. "Add Postgres health check for Compose wiring").
- **No drive-by refactors** — Avoid mixing formatting sweeps with feature work.

## Vertical slices

Prefer shipping a thin end-to-end path over horizontal layers:

| Prefer | Avoid |
|--------|-------|
| API endpoint + one test + doc note | All models with no API |
| One catalog screen calling real API | Full design system before first page |
| Migration + model + repository for one entity | Ten entities migrated at once |

## Before you commit

When tooling is wired (Phase 2+):

```bash
make api-format
make api-check
make web-check
make check
```

For Phase 1:

- Verify `make docker-up` / `make docker-down` if you touched Compose.
- Ensure CI-required files still exist (see `.github/workflows/ci.yml`).

## Keep documentation updated

| Change | Update |
|--------|--------|
| New architectural choice | [DECISION_LOG.md](DECISION_LOG.md) |
| New or changed entity | [DATA_MODEL.md](DATA_MODEL.md) |
| Completed phase | [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) |
| New env variable | `.env.example` and README |

## Avoid large rewrites

- Extend existing patterns before replacing subsystems.
- If a rewrite is necessary, document rationale in the decision log and split across PRs.
- Do not delete working features without an explicit decision.

## Pull requests

- Link to phase or requirement IDs when helpful.
- Include a short test plan in the PR description.
- Keep PRs reviewable — roughly ≤ 400 lines changed when possible.

## Local environment

1. Copy `.env.example` to `.env`.
2. `make db-up` or `make docker-up` for Postgres (and Redis).
3. `make db-migrate` to apply Alembic migrations.
4. `make seed` to load demo data (optional but recommended for UI work).
5. `make install` then `make api-dev`, or use the full Docker stack.
6. Follow [apps/api/README.md](../apps/api/README.md) for API-specific commands.

## Demo data (seed)

Populate the local database with realistic demo records:

```bash
make seed
```

Or reset everything and reseed from scratch:

```bash
make demo-reset
```

| Command | When to use |
|---------|-------------|
| `make seed` | After migrations when you want demo data without wiping the DB |
| `make db-seed` | Alias for `make seed` |
| `make demo-reset` | Clean slate — drops volumes, migrates, seeds |

Seed is **idempotent**: running `make seed` multiple times does not create duplicates.

Seed data is for **local and demo environments only** — not for production.

See [apps/api/app/seed/README.md](../apps/api/app/seed/README.md) for what is created and natural-key behavior.

## Database workflow

### Start local database

```bash
make db-up          # Postgres + Redis only
# or
make docker-up      # Postgres + Redis + API
```

### Run migrations

```bash
make db-migrate
```

Migrations are **not** applied on app startup. Always run `make db-migrate` after pulling new migration files.

### Create a migration

After changing SQLAlchemy models:

```bash
make db-revision message="add users table"
make db-migrate
```

Review autogenerated migrations before committing.

### Reset local database

When the local database is corrupted or you need a clean slate:

```bash
make docker-reset
make db-migrate
```

This removes Docker volumes and recreates Postgres from scratch.

### DATABASE_URL: Docker vs local host

| Scenario | `DATABASE_URL` host |
|----------|---------------------|
| API in Docker Compose | `postgres` |
| API on host (`make api-dev`) | `localhost` |

Both can use the same `.env` file — adjust `DATABASE_URL` depending on how you run the API.

## Running tests

```bash
make api-test      # backend pytest (excludes @integration)
make web-check     # lint + typecheck + build
make check         # api-check + web-check
```

Integration tests (require live Postgres) are marked `@pytest.mark.integration`.

## Adding a new backend module

1. Add models + Alembic migration.
2. Create `app/modules/<name>/` with router, service, repository, schemas, errors.
3. Register router in `app/api/v1/router.py`.
4. Use `ViewerUser` / `EditorUser` / `AdminUser` on endpoints.
5. Add tests: schemas, service (mocked), API (mocked service).
6. Update module README and OpenAPI tags.

## Adding a new frontend feature

1. Create `apps/web/src/features/<name>/` with `api.ts`, `types.ts`, `hooks.ts`.
2. Add page(s) under `apps/web/src/pages/`.
3. Register routes in `apps/web/src/app/router.tsx` (`new` and `:id/edit` before `:id`).
4. Add navigation entry in `apps/web/src/lib/navigation.ts`.
5. Use `PermissionGate` for write actions.
6. Run `make web-check`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API cannot connect to DB | Check `DATABASE_URL` host (`localhost` vs `postgres`) |
| 401 on all requests | Login again; verify `AUTH_ENABLED` |
| CORS error in browser | Add frontend URL to `CORS_ORIGINS` |
| Migration fails | `make db-current`; resolve conflicts; never edit applied migrations |
| Frontend build warns about API URL | Set `VITE_API_BASE_URL` before `pnpm build` |
| Docker web won't start | Ensure API healthcheck passes (`/health/live`) |

## Getting unstuck

- Re-read [COMPONENT_ARCHITECTURE.md](COMPONENT_ARCHITECTURE.md) for boundaries.
- Check [DECISION_LOG.md](DECISION_LOG.md) for past choices.
- Shrink scope and land something runnable, then iterate.
