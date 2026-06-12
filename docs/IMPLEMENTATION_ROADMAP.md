# Implementation Roadmap

Phased delivery plan for Internal Sea. Each phase should end in something runnable or reviewable before moving on.

## Phase 1: Repository foundation

**Status:** Completed

- Monorepo layout (`apps/`, `packages/`, `docs/`, `infra/`)
- Root config: `pyproject.toml`, `Makefile`, `.env.example`, `.gitignore`
- Docker Compose for Postgres and Redis
- Documentation foundation and CI structure check
- Placeholder READMEs for apps and packages
- SonarCloud integration

**Exit criteria:** Repo clones cleanly; `make docker-up` starts infra; CI passes structure checks.

---

## Phase 2: Backend foundation

**Status:** Completed

- FastAPI app under `apps/api/`
- uv dependency setup in `apps/api/pyproject.toml`
- App settings from environment (Pydantic Settings)
- Health endpoints (`/`, `/api/v1/health`, `/live`, `/ready`)
- CORS, logging, core utilities and module placeholders
- Pytest suite and `make api-check`
- API service in Docker Compose
- CI backend job (ruff, mypy, pytest)

**Exit criteria:** API starts locally and returns health check.

---

## Phase 3: Docker and database foundation

**Status:** Completed

- SQLAlchemy 2.0 async engine and session in `apps/api/app/db/`
- Alembic migrations with async support
- `SystemInfo` infrastructure table and first migration
- Database health endpoints (`/health/db`, DB-aware `/health/ready`)
- Makefile database commands (`db-migrate`, `db-revision`, etc.)
- CI migration-check job with PostgreSQL service
- Mocked DB tests in default CI; optional integration tests

**Exit criteria:** `make db-migrate` applies; `/api/v1/health/ready` reports database status.

---

## Phase 4: Core domain models

**Status:** Completed

- SQLAlchemy models: User, Person, Team, Capability, BusinessDomain, DataProduct, WorkItem, Comment
- Shared enums in `app/domain/enums.py`
- Alembic migration `0002_create_core_domain_models`
- Model metadata tests; seed placeholder
- Updated [DATA_MODEL.md](DATA_MODEL.md)

**Exit criteria:** Business tables defined; migration applies in CI; models import cleanly.

---

## Phase 5: Operating model expansion + Data Product API

**Status:** Completed

- Full target object model documented in [DATA_MODEL.md](DATA_MODEL.md)
- Expanded enums for projects, compliance, performance, tools, commercial pipeline
- Module placeholders for all future domains
- **Data Product CRUD API** at `/api/v1/data-products` (list, create, get, patch, delete)
- Repository / service / router pattern with pagination and filters
- API tests (mocked DB); no schema migration required

**Exit criteria:** OpenAPI shows Catalog tag; `make api-check` passes; data products manageable via API.

---

## Phase 6: Frontend foundation

**Status:** Completed

- React + TypeScript + Vite under `apps/web/`
- pnpm, Tailwind CSS, ESLint, TanStack Query, React Router
- App shell with sidebar navigation and top bar
- API client and health status indicator
- Placeholder pages for all major product areas
- Data Product feature API/types (no UI yet)
- Docker web service; frontend CI job

**Exit criteria:** `make web-check` passes; app loads at http://localhost:5173 with API status.

---

## Phase 7: Data Product Catalog UI

**Status:** Next

- List table with search and filters
- Create/edit/delete forms
- Detail page
- Connected to `/api/v1/data-products`

**Exit criteria:** End-to-end catalog flow via UI and API.

---

## Phase 8: Work Item API

**Status:** Completed

- Work item CRUD at `/api/v1/work-items`
- Board endpoint at `/api/v1/work-items/board`
- Repository / service / router pattern with pagination and filters
- API tests (mocked DB)

**Exit criteria:** Work items manageable via API with tests.

---

## Phase 9: Work Item UI and Board

**Status:** Completed

- List page with search, filters and pagination
- Create/edit/delete and detail pages
- Work board grouped by status with status transition buttons
- Connected to Work Item API via feature module

**Exit criteria:** End-to-end work management via UI and API.

---

## Phase 10: Projects / Internal Projects API

**Status:** Completed

- `Project` model and migration `0003_create_projects`
- CRUD at `/api/v1/projects` with filters, pagination and summary endpoint
- Internal projects view at `/api/v1/internal-projects`
- `WorkItem.project_id` link and filter support
- API tests (mocked DB)

**Exit criteria:** Projects manageable via API; work items linkable to projects.

---

## Phase 11: Projects and Internal Projects UI

**Status:** Completed

- Project list with search, filters and pagination
- Create/edit/delete and detail pages
- Summary cards from `/projects/{id}/summary`
- Internal projects UI slice reusing shared project components
- Connected to Projects and Internal Projects APIs

**Exit criteria:** End-to-end project management via UI and API.

---

## Phase 12: People / Teams / Capabilities API

**Status:** Completed

- People CRUD at `/api/v1/people` with filters, pagination and summary
- Teams CRUD at `/api/v1/teams` with summary counts
- Capabilities CRUD at `/api/v1/capabilities` with summary counts
- People DELETE deactivates (`is_active = false`)
- Teams/capabilities DELETE blocked when referenced (409 Conflict)
- API tests (mocked DB)

**Exit criteria:** People, teams and capabilities manageable via API.

---

## Phase 13: People / Teams / Capabilities UI

**Status:** Completed

- People list with search, filters and pagination
- Create/edit/deactivate and detail pages with summary cards
- Teams and capabilities list, CRUD, detail with summary cards
- PersonForm team/capability dropdowns from organization APIs
- Connected to People, Teams and Capabilities APIs

**Exit criteria:** End-to-end organization management via UI and API.

---

## Phase 14: Seed Data

**Status:** Completed

- Idempotent seed runner (`make seed`, `python -m app.seed.seed`)
- Demo data for capabilities, teams, people, business domains, projects, data products and work items
- `make demo-reset` for clean local demo environment
- Unit tests for seed data definitions; optional integration tests

**Exit criteria:** `make seed` populates UI with realistic demo records; repeated runs do not duplicate.

---

## Phase 15: Dashboard API and UI

**Status:** Completed

- Dashboard API at `/api/v1/dashboard/*` — summary, recent products, priority work, project health, capability workload, ownership gaps
- Dashboard UI at `/dashboard` with metric cards and section grid
- Governance/compliance placeholder card
- Separate TanStack Query per section for resilience
- API and schema tests (mocked DB); optional integration tests

**Exit criteria:** Dashboard loads with meaningful summary from demo data (`make seed`).

---

## Phase 16: Global Search

**Status:** Completed

- Unified search API at `GET /api/v1/search`
- PostgreSQL `ilike` queries across catalog, work, projects and organization
- Top bar `GlobalSearch` with debounced dropdown results
- Click-to-navigate result URLs per entity type
- API and schema tests (mocked DB); optional integration tests

**Exit criteria:** Top bar search finds seeded entities and navigates to detail pages.

---

## Phase 17: Comments and Activity

**Status:** Completed

- Comments on data products, work items, projects and internal projects
- Plain-text comments API with nested endpoints
- Activity events for create/update/delete/comment/status changes
- Activity timeline on detail pages (read-only, system-generated)
- API and schema tests (mocked DB)

**Exit criteria:** Users can add comments; activity visible on detail pages.

---

## Phase 18: Relationship Layer

**Status:** Completed

- EntityLink model and migration
- Relationships API (`/api/v1/relationships`)
- Application-level entity validation (no hard FKs to all tables)
- Outgoing/incoming relationship view per entity
- RelationshipsSection on detail pages (data product, work item, project, person, team, capability)
- Seed demo relationships
- Activity events for link/unlink
- API and schema tests (mocked DB)

**Exit criteria:** Related records visible across modules; users can add and delete links.

---

## Phase 19: Files and Evidence foundation

**Status:** Completed

- FileStorage, FileAsset and FileAttachment models and migration
- Files API (`/api/v1/files`) — storages, assets, attachments
- Entity file listing and attach/detach with duplicate prevention
- Evidence flags on attachments (`is_evidence`, `evidence_type`)
- Files UI — list, create/edit, detail pages
- FilesSection on data product, work item, project and internal project detail pages
- Seed demo files and evidence attachments
- Activity events for attach/detach

**Exit criteria:** Users can register file metadata, attach files to core entities and mark evidence.

---

## Phase 20: Compliance foundation

**Status:** Completed

- Policy, ComplianceRule, Control, ComplianceCheck and ComplianceCheckEvidence models and migration
- Compliance API (`/api/v1/compliance`) — policies, rules, controls, checks, evidence, overview, entity compliance
- Entity validation for supported subject types
- Evidence integration with FileAsset and FileAttachment
- Compliance UI — overview page, policy and check CRUD, evidence by file ID
- ComplianceSection on data product, project, internal project, team and capability detail pages
- Seed demo policies, rules, controls and checks
- Dashboard compliance counts

**Exit criteria:** Users can create policies and checks, attach evidence, and view compliance on entity detail pages.

---

## Phase 21: Auth and permissions

**Status:** Completed

- User model updates (`is_superuser`, `last_login_at`)
- JWT login, `/auth/me`, admin user management
- bcrypt password hashing
- Role dependencies on all module routers
- Login page, AuthProvider, protected routes
- PermissionGate and write action hiding for viewers
- Seeded demo users (admin/editor/viewer)

**Exit criteria:** Authenticated users with role-gated mutations.

---

## Phase 22: Entity picker / smart relationship selector

**Status:** Completed

- Search API extended with `file`, `policy`, `compliance_check` types
- Entity lookup endpoint `GET /api/v1/search/entity/{type}/{id}`
- Reusable `EntityPicker` and `EntityReference` frontend components
- Forms updated: relationships, files, compliance, ownership and link fields
- Detail pages show readable entity names instead of raw UUIDs
- Manual UUID fallback in advanced form sections where needed

**Exit criteria:** Users can search/select entities in forms; detail pages show human-readable references.

---

## Phase 23: Automation triggers and schedules

**Status:** Completed

- `AutomationSchedule`, `AutomationTrigger`, `AutomationRun` models and migration `0009`
- Automation API: schedules, triggers, runs, overview, entity automations
- Manual runner with simulation (default) and safe real actions
- Automation UI: overview page, forms, trigger detail, run history
- `AutomationSection` on entity detail pages
- Demo seed schedules and triggers

**Exit criteria:** Editors can create schedules/triggers, run simulations and safe actions, view run history.

---

## Phase 24: Performance metrics foundation

**Status:** Completed

- `PerformanceMetricDefinition`, `PerformanceMetricValue` models and migration `0010`
- Performance API: definitions, values, overview, entity scorecards
- Simple score/trend calculation (manual values in MVP)
- Performance UI: overview, forms, definition detail, value create/edit
- `PerformanceSection` on entity detail pages
- Demo seed metric definitions and values

**Exit criteria:** Editors can define metrics, record values, view scorecards on detail pages.

---

## Phase 25: Production readiness review

**Status:** Completed

- Settings validation for production-like environments
- Standard error responses and request ID middleware
- Request logging and graceful engine shutdown
- Frontend API client hardening (401 handling, error parsing, network errors)
- Docker healthchecks and complete API image dependencies
- Deployment/operations docs and production readiness checklist
- Additional smoke tests (config, errors, request ID, OpenAPI coverage)

**Exit criteria:** `make check` passes; health endpoints work; docs cover deploy and operations.

---

## Phase 26: Notification channels foundation

**Status:** Completed

- Notification channels, templates, preferences, messages and delivery attempts
- Simulation-first sending (no external delivery)
- Simple `{{placeholder}}` template rendering
- Automation `send_notification` integration (safe simulation)
- Notifications UI and `NotificationsSection` on detail pages
- Seed demo channels, templates and messages

**Exit criteria:** Editors can create channels/templates/messages and simulate sends; delivery attempts are recorded.

---

## Phase 27: Background worker execution

**Status:** Completed

- Worker module (`run-once`, `run-loop` CLI)
- Due automation trigger scanning and `next_run_at` calculation
- Queued notification message processing
- DB row locks, run/delivery history with `worker_instance_id`
- Worker API (`/worker/status`, `/worker/due-work`, `/worker/run-once`)
- Docker worker profile, Makefile commands, Automation page worker UI
- Seed due trigger and queued notification for demo

**Exit criteria:** `make worker-once` processes demo due work; Automation page shows worker status.

---

## Phase 28: Advanced dashboard and insights

**Status:** Completed

- Executive summary and operational health scores (transparent formulas)
- Actionable insights with deterministic rules
- Section endpoints: work delivery, project insights, data product health, compliance, performance, automation, notifications, recent activity
- Advanced dashboard UI with independent section loading
- `GET /api/v1/dashboard/advanced` combined endpoint

**Exit criteria:** Dashboard shows executive overview, insights and module health cards from seeded demo data.

---

## Phase 29: SaaS tenant foundation

**Status:** Completed

- Company, Workspace and CompanyMember models
- Migration `0013` with nullable `company_id` / `workspace_id` on major tables
- Tenancy API (`/tenancy/*`) with first-user onboarding
- Tenant dependencies (`X-Company-ID`, `X-Workspace-ID`)
- Tenant scoping on priority modules (data products, work items, projects, people, teams, capabilities, dashboard, search)
- Demo company seed (Internal Sea Demo / Default Workspace)
- Frontend TenancyProvider, onboarding and settings pages

**Exit criteria:** Demo login shows company context; empty DB supports first-user onboarding.

---

## Phase 30: Import/export foundation

**Status:** Planned

---

## Phase 31: First release candidate

**Status:** Planned

---

## Technical Debt Roadmap

Known MVP limitations, deferred decisions and follow-up work are tracked in **[TECH_DEBT_REGISTER.md](TECH_DEBT_REGISTER.md)** (61 items as of 2026-06-12). Security review findings from [LOCAL_TEST_AND_READINESS_REVIEW.md](LOCAL_TEST_AND_READINESS_REVIEW.md) are mapped in the register's [Security review results](TECH_DEBT_REGISTER.md#security-review-results-2026-06-12) section.

### Top P0 / P1 items (address before team pilot or production)

| ID | Title | Priority |
|----|-------|----------|
| [TD-001](TECH_DEBT_REGISTER.md#td-001-incomplete-tenant-api-scoping-on-deferred-modules) | Incomplete tenant API scoping on deferred modules | P0 |
| [TD-002](TECH_DEBT_REGISTER.md#td-002-production-misconfiguration-risk-secrets-seed-demo-users) | Production misconfiguration risk (secrets, seed, demo users) | P0 |
| [TD-061](TECH_DEBT_REGISTER.md#td-061-production-https-and-cors-not-enforced-beyond-config-validation) | Production HTTPS and CORS not enforced beyond config validation | P0 |
| [TD-003](TECH_DEBT_REGISTER.md#td-003-nullable-company_id-at-database-level) | Nullable `company_id` at database level | P1 |
| [TD-004](TECH_DEBT_REGISTER.md#td-004-global-unique-teamcapability-names-not-per-company) | Global unique Team/Capability names | P1 |
| [TD-005](TECH_DEBT_REGISTER.md#td-005-jwt-access-tokens-stored-in-localstorage) | JWT in `localStorage` | P1 |
| [TD-006](TECH_DEBT_REGISTER.md#td-006-no-password-reset-or-user-invitation-flows) | No password reset or invitation flows | P1 |
| [TD-007](TECH_DEBT_REGISTER.md#td-007-activity-feed-is-not-audit-grade-no-immutable-audit-trail) | No audit-grade immutable trail | P1 |
| [TD-008](TECH_DEBT_REGISTER.md#td-008-companymember-tenant-roles-not-enforced-on-all-modules) | CompanyMember roles not enforced everywhere | P1 |
| [TD-009](TECH_DEBT_REGISTER.md#td-009-no-production-monitoring-or-external-observability) | No production monitoring | P1 |
| [TD-010](TECH_DEBT_REGISTER.md#td-010-backup-and-restore-not-automated) | Backup not automated | P1 |
| [TD-011](TECH_DEBT_REGISTER.md#td-011-integration-tests-excluded-from-default-ci) | Integration tests excluded from CI | P1 |

### Recommended next technical debt prompt

**Prompt TD-01: Tenant Isolation Hardening** — complete tenant scoping on files, compliance, automation, performance, notifications, relationships, comments and activity; then NOT NULL `company_id`, per-company uniqueness and CompanyMember RBAC (TD-001, TD-003, TD-004, TD-008).

After tenant hardening, run **Prompt TD-06: Production Operations and Monitoring** for CI integration tests, deploy guardrails, HTTPS/CORS hardening and observability (TD-002, TD-061, TD-009, TD-010, TD-011).

Feature work **Phase 30 (Import/Export)** remains the next product prompt but should follow or parallel tenant hardening depending on pilot timeline — see [TD-019](TECH_DEBT_REGISTER.md#td-019-importexport-foundation-not-implemented).

---

## Working style

- One vertical slice at a time (see [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md))
- Update docs when decisions or scope change
- Record significant choices in [DECISION_LOG.md](DECISION_LOG.md)
- Track deferred work in [TECH_DEBT_REGISTER.md](TECH_DEBT_REGISTER.md)
