# Seed Data

Idempotent demo dataset for local development, screenshots and product testing.

## Run

From the repository root:

```bash
make seed
```

Or from `apps/api`:

```bash
uv run python -m app.seed.seed
```

Requires:

1. Postgres running (`make db-up` or `make docker-up`)
2. Migrations applied (`make db-migrate`)
3. `DATABASE_URL` pointing at your database

### DATABASE_URL

| How you run seed / API | Host in `DATABASE_URL` |
|------------------------|-------------------------|
| Local shell (`make seed`, `make api-dev`) | `localhost` |
| Inside Docker API container | `postgres` |

Example for local seed against Docker Postgres:

```env
DATABASE_URL=postgresql+asyncpg://internal_sea:internal_sea@localhost:5432/internal_sea_core
```

### Full demo reset

Wipes volumes, waits for Postgres, migrates and seeds:

```bash
make demo-reset
```

## What is created

| Category | Count | Examples |
|----------|------:|----------|
| Capabilities | 8 | Data Engineering, BI, AI, CloudOps |
| Teams | 5 | Core Platform Team, Data Products Team |
| People | 10 | Nikita Rogatov, Sofia Marin, Maya Singh |
| Business domains | 6 | Finance, Sales, Product, Inventory |
| Client projects | 3 | Finance Data Platform Migration |
| Internal projects | 3 | Internal Sea MVP |
| Data products | 6 | Executive Sales Dashboard, Finance KPI Layer |
| Work items | 10 | Catalog API, Work Board, governance tasks |
| Relationships | 6 | Dashboard depends_on KPI layer, team owns MVP |
| File storages | 2 | External Documentation, SharePoint Demo |
| File assets | 4 | Executive Sales Dashboard Specification, Finance KPI Definitions |

Work item reporters are stored as minimal `User` records (no auth/password) because `WorkItem.reporter_id` references `users`.

## Idempotency

Natural keys:

| Entity | Key |
|--------|-----|
| Capability | `name` |
| Team | `name` |
| Person | `email` (fallback: `full_name`) |
| Business domain | `name` |
| Project | `name` |
| Data product | `name` |
| Work item | `title` + `type` |
| File storage | `name` |
| File asset | `name` |
| File attachment | `file_id` + `entity_type` + `entity_id` + `purpose` |
| Entity link | `source_type` + `source_id` + `target_type` + `target_id` + `link_type` |

Running `make seed` multiple times:

- Does **not** create duplicates
- Updates basic fields (description, status, relationships) when seed data changes
- Preserves record IDs and relationships

## Files

| File | Purpose |
|------|---------|
| `seed_data.py` | Static seed dictionaries — edit demo content here |
| `seed.py` | Async runner and `get_or_create_*` helpers |
| `README.md` | This guide |

## UI after seeding

With `make api-dev` and `make web-dev`:

- http://localhost:5173/data-products
- http://localhost:5173/work-items
- http://localhost:5173/work-board
- http://localhost:5173/projects
- http://localhost:5173/internal-projects
- http://localhost:5173/people
- http://localhost:5173/teams
- http://localhost:5173/capabilities

Seed data is for **local and demo environments only** — not for production.
