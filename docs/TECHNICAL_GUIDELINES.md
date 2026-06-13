# Technical Guidelines

Conventions for building Internal Sea. Keep implementations simple and production-oriented without overengineering.

## Python-first backend

- Python 3.11+ for all backend and shared package code.
- Manage API dependencies with **uv** in `apps/api/` (`make install`).
- Shared logic lives in `packages/`; `apps/api` stays a thin HTTP layer.

## Database conventions

- **PostgreSQL 16** is the only database target.
- Use **SQLAlchemy 2.0 async** with `asyncpg` for runtime database access.
- Manage schema changes with **Alembic** — migrations are explicit, never automatic on app startup.
- All models use **UUID primary keys** via `UUIDPrimaryKeyMixin`.
- All business tables include **`created_at` / `updated_at`** via `TimestampMixin`.
- Database access goes through **repositories** (later); API endpoints must not embed raw SQL.
- Use `get_db_session()` dependency for request-scoped `AsyncSession` access.
- Health checks use `check_database_connection()` — do not open ad-hoc connections in endpoints.

## FastAPI conventions

- Use an **app factory** (`create_app()` in `app/main.py`) for testability and consistent startup.
- Version all HTTP routes under **`/api/v1`**; add `/api/v2` only when breaking changes require it.
- Place domain code under **`app/modules/<domain>/`** — one folder per product area.
- **Module pattern** (required for new APIs):

```
app/modules/<domain>/
├── router.py       # FastAPI routes — thin, no SQL
├── schemas.py      # Pydantic request/response models
├── service.py      # Business logic and orchestration
├── repository.py   # SQLAlchemy queries only
├── errors.py       # Domain-specific exceptions
└── README.md       # Module purpose and status
```

- **Delivery order:** document in `docs/DATA_MODEL.md` → SQLAlchemy model + migration → API module → UI slice.
- Keep **endpoints thin**: validate input, call a service, return a schema.
- Define **Pydantic schemas** per module — separate from SQLAlchemy models in `app/models/`.
- Register routers in `app/api/v1/router.py` only when implemented.
- One health router stays under `app/api/v1/endpoints/`.
- Dependency injection for settings, DB sessions and current user (when auth exists).
- OpenAPI tags match product modules: Catalog, Work, Teams, etc.
- Return appropriate HTTP status codes; use consistent error response shape.
- **Write tests for each new endpoint** before merging.

## React frontend conventions

- **React 18 + TypeScript + Vite** under `apps/web/`
- **pnpm** for package management
- **Tailwind CSS** for styling — light theme only in foundation phase
- **React Router** for client-side routing
- **TanStack Query** for server state (API calls, caching, refetch)
- No global client state library unless a clear need emerges

### Folder structure

```
src/
├── app/           # App shell, router, providers
├── components/    # layout/, ui/, common/
├── features/      # Domain-specific API + types (+ UI later)
├── lib/           # apiClient, config, navigation, utils
├── pages/         # Route-level page components
└── types/         # Shared TS types and enums
```

### Rules

- **No direct `fetch` in pages** — use `lib/apiClient.ts` or feature `api.ts` helpers
- Pages compose layout and feature components; keep pages thin
- Feature folders own API functions and types; UI components added per vertical slice
- Mirror backend enum strings in `types/enums.ts`
- Use TanStack Query hooks in components (not in api.ts)
- Run `make web-check` before opening frontend PRs

### Design system and styling

- Use **`apps/web/src/lib/designTokens.ts`** for status-to-badge color mappings — do not hardcode status colors inside feature components.
- Import badge variant classes from design tokens; use `StatusBadge` or `Badge` with a variant prop.
- Reuse **`components/ui/`** (Button, Card, Badge, StatusBadge, Input, PageHeader, EmptyState) before creating new styled elements.
- Follow [DESIGN_GUIDELINES.md](DESIGN_GUIDELINES.md) for colors, typography, layout and page patterns.
- Keep feature UI **minimal and enterprise-grade** — no custom gradients, heavy shadows or one-off color palettes per module.
- Tailwind semantic colors (`core-*`, `app-*`, `status-*`) are defined in `tailwind.config.ts`; prefer these over raw hex or default Tailwind palette colors.

### Feature UI pattern (Data Products, Work Items, …)

Each domain feature under `src/features/<domain>/` should include:

```
api.ts          # HTTP functions via apiClient — no fetch in pages
hooks.ts        # TanStack Query keys, queries and mutations
types.ts        # Types matching backend schemas
constants.ts    # Labels and filter options
utils.ts        # Formatting and payload helpers
components/     # Feature-specific UI
```

- Pages compose feature components only — keep pages thin.
- Mutations invalidate list, detail and board query keys as applicable.
- Board endpoints (e.g. `GET /work-items/board`) are consumed through the feature `api.ts` layer — not direct fetches in pages.
- Board state is **server-driven**; refetch after status updates rather than optimistic local column moves (until drag-and-drop ships).

### Project model pattern

- Use **one model with a type discriminator** (`project_type`) when entities are operationally similar (client projects, internal projects, POCs, pilots, MVPs, initiatives).
- Expose **focused API views** when it helps UX — e.g. `/internal-projects` filters the same `projects` table.
- Avoid duplicate tables for internal vs client projects unless the data model diverges significantly.

### Organization frontend feature pattern

People, Teams and Capabilities are **separate features** under `src/features/people/`, `src/features/teams/` and `src/features/capabilities/` — each with own `api.ts`, `hooks.ts`, `types.ts` and components.

- `PersonForm` may import `useTeams` and `useCapabilities` for dropdown options — import hooks only, not components, to avoid circular dependencies.
- Fetch selector data with `page_size: 100` — no advanced autocomplete in MVP.
- People DELETE maps to `deactivatePerson` in the frontend API layer.
- Summary cards consume `/{id}/summary` endpoints via dedicated query keys.

### Dashboard API conventions

- Dashboard endpoints are **read-only aggregates** — no mutations.
- The dashboard module **does not own business logic** of other domains; it queries existing SQLAlchemy models via `DashboardRepository` and `AdvancedDashboardRepository`.
- Cross-module queries in the dashboard repository are acceptable for MVP; optimize only when needed.
- Keep endpoints **separate per section** (`/summary`, `/executive-summary`, `/actionable-insights`, etc.) so partial failures are isolated.
- Health scores and actionable insights use **transparent formulas** in `app/modules/dashboard/scoring.py` and `insights.py` — no hidden AI scoring.
- Advanced section limits normalize to a **max of 50** via `normalize_dashboard_limit`.
- Ownership gap severity rules live in `app/modules/dashboard/gaps.py` — not in catalog or work modules.
- Do not implement performance metrics or compliance APIs inside the dashboard module (query their models only).

### SaaS tenancy conventions

- Every new business object should include **`company_id`**; use **`workspace_id`** where workspace-specific.
- List queries must filter by current company; create operations set tenant IDs from `CurrentTenant`.
- Do not trust `company_id` from the client request body.
- Seed must create a default demo company and backfill tenant IDs (`app/seed/tenant.py`).
- `company_id` remains nullable in the database until a future migration enforces NOT NULL.

### Search API conventions

- Global search uses **PostgreSQL `ilike`** for MVP — no Elasticsearch, OpenSearch, Meilisearch or vector search.
- `GET /api/v1/search` returns a **unified `SearchResult` format** with frontend-relative `url` paths.
- Search is **read-only** — no indexing pipeline or background jobs.
- Per-entity queries merge in Python with simple ranking; do not introduce an external search service until needed.
- Future options: PostgreSQL full-text search, embeddings, AI assistant search — document in decision log when adopted.
- URL builders live in `app/modules/search/urls.py` — keep route paths aligned with React Router.

### Search frontend conventions

- Feature folder: `src/features/search/`
- `GlobalSearch` in top bar; debounce via `useDebouncedValue` in `lib/hooks.ts`
- TanStack Query enabled only when trimmed query length ≥ 2
- Navigate with React Router to `result.url` from API — do not reconstruct paths in the UI

### Entity picker conventions

- Feature folder: `src/features/entity-picker/`
- Forms should use `EntityPicker` for relationship, ownership and link fields — not raw UUID inputs
- `EntityReference` resolves IDs to titles via `GET /api/v1/search/entity/{type}/{id}`
- Picker search uses `GET /api/v1/search` with `types` filter; debounce in component (300ms)
- Backend still validates entity IDs on write — picker is convenience, not authorization
- Search remains simple `ilike` MVP; no AI suggestions or entity graph yet
- Manual UUID fallback allowed in collapsible advanced sections only
- Future: smart suggestions, command palette, relationship graph visualization

### Dashboard frontend conventions

- Feature folder: `src/features/dashboard/` with separate TanStack Query hooks per section.
- **One query per card/section** — a failing section shows inline error without crashing the page.
- Executive summary and operational health load independently from insight cards.
- Reuse `MetricCard`, `MiniProgressBar`, `HealthScoreBadge`, design tokens and existing badges — **no heavy charting dependencies**.
- Actionable insights link to source entities via `getDashboardEntityHref` when URLs are provided.

### Organization API conventions

- **People DELETE** deactivates (`is_active = false`) instead of hard delete — people may be referenced by work items, projects and data products.
- **Teams and capabilities DELETE** are hard deletes only when no references exist; return **409 Conflict** otherwise.
- Do **not** cascade delete people, data products, work items or projects when removing a team or capability.
- Use **`/{id}/summary`** endpoints for dashboard and detail pages — aggregate counts in the repository layer.
- Keep organization APIs separate from the future performance API — performance metrics will reference these entities but live in their own module.

### Reusing feature components across related API views

- Frontend components can be reused across related API views when the underlying entity is the same (e.g. `Project` for both `/projects` and `/internal-projects`).
- Internal projects should reuse the `features/projects/` module — do not duplicate API, hooks or form logic in a separate feature folder.
- A **`variant` prop** (`"projects" | "internal-projects"`) is acceptable when UI differs slightly (hidden columns, read-only type, different endpoints).
- Share query keys per API surface (`projectKeys` vs `internalProjectKeys`) but share types, constants, utils and presentational components.

## Naming rules

| Area | Convention | Example |
|------|------------|---------|
| Python modules | `snake_case` | `data_product_service.py` |
| Python classes | `PascalCase` | `DataProduct` |
| API routes | `kebab-case` paths | `/api/v1/data-products` |
| DB tables | `snake_case`, plural | `data_products` |
| React components | `PascalCase` | `DataProductList.tsx` |
| TS files (non-component) | `camelCase` or `kebab-case` | `apiClient.ts` |
| Env vars | `SCREAMING_SNAKE_CASE` | `DATABASE_URL` |

## Modular architecture

```
apps/api/          → HTTP, routing, auth middleware
packages/core-domain/   → Pure domain rules, no I/O
packages/core-db/       → Models, repositories, migrations
packages/core-auth/     → Tokens, permissions
```

- Dependencies point inward: API → packages, never packages → API.
- No circular imports between packages; extract shared types to `core-domain` if needed.

## Avoid premature abstractions

- Do not introduce generic repositories, event buses or plugin frameworks until a second use case exists.
- Prefer explicit functions over deep inheritance hierarchies.
- Copy-paste a little before abstracting — then extract when the pattern is clear.

## Test expectations

- **Unit tests** for domain rules in `core-domain` and services with mocked DB.
- **API tests** with TestClient and test database (Phase 3+).
- **Frontend tests** for critical flows; start with component tests for forms and tables.
- Run `make api-check` before opening PRs (ruff, mypy, pytest).
- Aim for meaningful coverage on business logic, not 100% line coverage on boilerplate.

## Tooling

| Tool | Purpose |
|------|---------|
| ruff | Lint and format Python |
| pytest | Python tests |
| mypy | Static typing (incremental strictness) |
| GitHub Actions | CI on push and PR |

Configuration lives in root `pyproject.toml` until per-package splits are needed.

## Relationships (EntityLink)

- The generic relationship model uses **application-level validation** — do not add foreign keys for every possible entity type.
- Keep **supported entity types explicit** in `SUPPORTED_ENTITY_TYPES`; future enum values stay unvalidated until their modules exist.
- **Relationship creation** should record `linked` / `unlinked` activity events when ActivityService is available.
- Avoid a graph database until relationship queries or visualization genuinely require it — PostgreSQL is sufficient for MVP.

## Comments and activity

- **Activity events** are created by domain **services**, not routers — record on create/update/delete and significant field changes.
- **Comments** create a `commented` activity event when added.
- Do **not** expose activity mutation endpoints publicly for MVP — activity is system-generated.
- `actor_id` remains optional in MVP; wire to authenticated user when mutating endpoints are updated to pass actor context.
- Use `entity_type` + `entity_id` for activity; comments keep explicit foreign keys (`data_product_id`, `work_item_id`, `project_id`) for now.

## Files and evidence

- **No binary upload in MVP** — store metadata and external URLs only.
- **File metadata first** — `FileAsset` holds name, type, sensitivity, version and location fields; `storage_path` and `checksum` are for future storage integration.
- **Generic FileAttachment** uses `entity_type` + `entity_id` with **application validation** — do not add FKs to every entity table.
- **Supported entity types must be explicit** in `SUPPORTED_FILE_ENTITY_TYPES`; future enum values stay unvalidated until implemented.
- **Future storage integrations** should use `FileStorage` records and populate `storage_path` / `checksum` when upload is added.
- **Delete** sets `FileStatus.deleted` rather than hard-deleting referenced files.
- Record **linked/unlinked** activity events on attach/detach.

## Authentication and authorization

- Register the auth router at `/api/v1/auth`; login is public, `/auth/me` requires a valid bearer token.
- Use `ViewerUser`, `EditorUser` and `AdminUser` from `app.api.auth_deps` on module routers.
- **Health endpoints remain public** — do not add auth dependencies to `/health` routes.
- **Backend is the source of truth** — never rely on frontend permission hiding alone.
- Set `AUTH_ENABLED=false` only for local/tests; production must keep auth enabled.
- Role checks stay simple (`viewer` / `editor` / `admin` / `is_superuser`) until enterprise RBAC is needed.

## Compliance

- **Generic compliance subjects** use `subject_type` + `subject_id` on `ComplianceCheck` with **application validation** — do not add FKs to every entity table.
- **Supported subject types** are explicit in `SUPPORTED_COMPLIANCE_SUBJECT_TYPES`; `person` and `tool` remain in the enum but are rejected until implemented.
- **Evidence** links checks to `FileAsset` via `ComplianceCheckEvidence`; adding evidence may also create a `FileAttachment` on the subject with `is_evidence=true` and `evidence_type="compliance"`.
- **Checks are manual in MVP** — no automated rule execution, schedules or approval workflows yet.
- **Compliance is separate from full audit logging** — activity events record high-level changes; compliance does not replace audit export.
- Record **updated/linked** activity events when checks are created/updated and when evidence is added.

## Performance metrics

- **Metrics are manual in MVP** — no automatic calculation engine or scheduled metric jobs yet.
- **Generic subjects** use `subject_type` + `subject_id` on `PerformanceMetricValue` with **application validation** — do not add FKs to every entity table.
- **Scorecard is calculated** from latest values per active definition; it is not stored as a table in MVP.
- **Project-scoped definitions** may apply to internal projects for scorecards and values.
- Avoid HR-specific performance review or compensation workflows in MVP.

## Automation

- **Manual run** — `POST /automation/triggers/{id}/run` with `simulate: true` by default.
- **Safe action allowlist** — only `create_work_item`, `add_comment`, `create_activity_event`, `send_notification` on real runs (notification still simulation-first).
- Validate `action_config` JSON before action execution; reject unsupported action types on real runs.
- Automation does not replace permission checks — manual runs require editor role.

## Background worker

- Worker is a **separate process** (CLI or Docker `worker` profile); API runs without it.
- Worker must be **idempotent** — use DB row locks (`locked_at`, `lock_expires_at`) not distributed locks.
- Worker actions must be **safe and permission-independent** — system execution only for MVP-safe actions.
- External notification delivery remains **disabled by default** (`NOTIFICATION_EXTERNAL_DELIVERY_ENABLED=false`).
- Avoid long-running transactions; keep worker cycles small and observable.
- Start with **one worker instance**; scale-out requires external queue (future).

## API response conventions

- List endpoints return `{ items, total, page, page_size, pages }`.
- Create endpoints return **201** with the created resource.
- Delete endpoints return **204** with empty body.
- Use `normalize_pagination()` and `MAX_PAGE_SIZE = 100` from `app.core.pagination`.

## Error response standard

All API errors return:

```json
{
  "error": "not_found",
  "message": "Human-readable message",
  "details": null,
  "request_id": "uuid",
  "detail": "Human-readable message",
  "code": "not_found"
}
```

Legacy `detail` / `code` fields remain for backward compatibility.

Handlers cover: domain errors, `HTTPException`, `RequestValidationError` (422), `IntegrityError` (409), and unhandled exceptions (500).

## Request ID

- Middleware reads or generates `X-Request-ID`.
- Response includes the same header.
- Error responses include `request_id`.
- Request logging includes `request_id`.

## Migration policy

- Migrations live in `apps/api/alembic/versions/`.
- Run manually with `make db-migrate` — **never** on API startup.
- Review autogenerated migrations before commit.
- Downgrade functions must exist for reversible changes.

## Seed policy

- Seed is idempotent and local/demo only.
- Natural keys: names, codes, emails, composite period keys.
- Do not seed production unless explicitly intended.

## Backend validation policy

- Pydantic schemas reject empty required strings.
- Generic `subject_type` / `subject_id` references validated in services.
- `UserRead` never exposes `hashed_password`.
- Automation `action_config` validated before execution; unsafe actions blocked on real runs.

## Frontend API client policy

- Use `apiClient.ts` for all HTTP calls.
- Attach `Authorization: Bearer` when token exists.
- On 401, clear session and redirect to `/login` (avoid redirect loops).
- Parse both `message` and legacy `detail` from error bodies.
- Surface `request_id` from `ApiError` when debugging.

## Notifications (MVP)

- No external email, Teams, Slack or webhook delivery in MVP.
- Simulation is the default send mode (`simulate=true`).
- `provider_config` must not store secrets; use environment variables or a future secret manager.
- Template rendering is simple `{{placeholder}}` replacement only (no template engine).
- Background delivery worker and digest notifications are future scope.
- Notification records are separate from activity events (both may be written on send).

## Documentation

- Update [DECISION_LOG.md](DECISION_LOG.md) for architectural choices.
- Update [DATA_MODEL.md](DATA_MODEL.md) when entities or relationships change.
- Use Mermaid in docs when diagrams clarify structure.
