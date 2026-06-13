# Internal Sea

Internal Sea is a single-repository, Python-first internal operating platform. It combines a business-facing Data Product Catalog, Jira-like Work and Task Management, and Team, Capability, Skill and Allocation Management into one connected system.

> **Naming:** Product name is **Internal Sea**. Repository folder (`internal-sea-core`) and database (`internal_sea_core`) are unchanged for local compatibility.

Business data products, delivery work, people, teams, capabilities, ownership, risks, decisions and technical debt live in one place instead of scattered tools.

## Main modules

| Module | Purpose |
|--------|---------|
| **Data Product Catalog** | Discover, describe and govern business data products |
| **Work Management** | Track delivery work, tasks and progress |
| **Team and Capability Management** | People, teams, skills, allocations and capability ownership |
| **Relationship Layer** | Links between products, work, people, risks and decisions |
| **Files and Evidence** | File metadata, external links and evidence attachments |
| **Compliance** | Policies, rules, controls, checks and evidence |
| **Auth** | Login, JWT, role-based access control |
| **Automation** | Schedules, triggers, manual runs and run history |
| **Performance** | Metric definitions, values and entity scorecards |
| **Notifications** | Channels, templates, messages, simulated sending and delivery history |
| **Background Worker** | Optional process for due automation and queued notifications |
| **Dashboard & Search** | Executive insights hub and global search |
| **SaaS Tenancy** | Company, workspace, members, onboarding and tenant-scoped data |

## SaaS hierarchy

```
Company
└── Workspace
    ├── Teams, People, Capabilities
    ├── Data Products, Projects, Work Items
    └── Compliance, Automation, Performance, Notifications
```

- **First-user onboarding:** `/onboarding/first-user` when no company exists
- **Demo company:** Internal Sea Demo / Default Workspace (after `make seed`)
- **Tenant headers:** `X-Company-ID`, `X-Workspace-ID` (stored in localStorage by the web app)

## Production warning

Internal Sea is **demo-ready** for local use. Before production:

- Change `JWT_SECRET_KEY` and database passwords
- Set `APP_ENV=production`, `DEBUG=false`, restrict `CORS_ORIGINS`
- Do **not** run `make seed` in production
- Use HTTPS and review [docs/PRODUCTION_READINESS_CHECKLIST.md](docs/PRODUCTION_READINESS_CHECKLIST.md)

## Technical debt

Known MVP limitations, security gaps and deferred work are tracked in **[docs/TECH_DEBT_REGISTER.md](docs/TECH_DEBT_REGISTER.md)**.

Internal Sea remains **MVP / pilot-stage** until P0 and P1 items in that register are resolved — especially tenant isolation hardening (TD-001), production deploy guardrails (TD-002) and pilot readiness items (TD-003 through TD-011).

## Health endpoints

```bash
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8000/api/v1/health/ready
```

## Operations docs

| Doc | Purpose |
|-----|---------|
| [DEPLOYMENT_GUIDELINES.md](docs/DEPLOYMENT_GUIDELINES.md) | Deploy steps and env matrix |
| [OPERATIONS_RUNBOOK.md](docs/OPERATIONS_RUNBOOK.md) | Startup, troubleshooting, JWT rotation |
| [PRODUCTION_READINESS_CHECKLIST.md](docs/PRODUCTION_READINESS_CHECKLIST.md) | Pre-go-live checklist |

## Technology stack

| Layer | Choice |
|-------|--------|
| Backend | Python, FastAPI |
| Frontend | React, TypeScript, Vite |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Python packages | uv |
| Frontend packages | pnpm |
| Local infra | Docker Compose |
| CI | GitHub Actions |

## Repository structure

```
internal-sea-core/
├── apps/
│   ├── api/          # FastAPI backend
│   └── web/          # React frontend
├── packages/
│   ├── core-domain/
│   ├── core-db/
│   ├── core-auth/
│   ├── core-integrations/
│   └── core-ai/
├── docs/             # Flat uppercase documentation
├── infra/docker/     # Docker-related files (later)
├── .github/workflows/
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── .env.example
```

See [docs/PROJECT_VISION.md](docs/PROJECT_VISION.md) for product direction and [docs/IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for the build plan.

## Database setup

1. Copy environment variables: `cp .env.example .env`
2. Start infrastructure: `make docker-up` (or `make db-up` for Postgres and Redis only)
3. Run migrations: `make db-migrate`
4. Load demo data: `make seed`
5. Install and run API: `make install` then `make api-dev`
6. Verify: `make api-check`

### Local demo setup (quick start)

```bash
cp .env.example .env
make docker-up      # or: make db-up
make db-migrate
make seed
make api-dev        # terminal 1
make web-dev        # terminal 2
```

Or reset everything and reseed in one step:

```bash
make demo-reset
make api-dev
make web-dev
```

After seeding, open:

| Page | URL |
|------|-----|
| Data products | http://localhost:5173/data-products |
| Data product detail | http://localhost:5173/data-products/{id} |
| Work items | http://localhost:5173/work-items |
| Work board | http://localhost:5173/work-board |
| Projects | http://localhost:5173/projects |
| Internal projects | http://localhost:5173/internal-projects |
| People | http://localhost:5173/people |
| Teams | http://localhost:5173/teams |
| Capabilities | http://localhost:5173/capabilities |
| Files | http://localhost:5173/files |

### Health checks

| URL | Purpose |
|-----|---------|
| http://localhost:8000/api/v1/health | General health |
| http://localhost:8000/api/v1/health/db | Database connectivity |
| http://localhost:8000/api/v1/health/ready | Readiness (includes DB) |
| http://localhost:8000/docs | OpenAPI docs |

### DATABASE_URL: Docker vs local

| API runs in | Use host |
|-------------|----------|
| Docker Compose (`make docker-up`) | `postgres` |
| Local shell (`make api-dev`) | `localhost` |

Example for local API with Docker Postgres:

```env
DATABASE_URL=postgresql+asyncpg://internal_sea:internal_sea@localhost:5432/internal_sea_core
```

### Troubleshooting

- **API cannot connect to DB locally** — set `DATABASE_URL` host to `localhost`, not `postgres`.
- **API in Docker cannot connect** — use `postgres` as the hostname in `.env`.
- **Broken local database** — run `make docker-reset` then `make db-migrate`.

## Local development

1. Copy environment variables: `cp .env.example .env`
2. Install dependencies: `make install`
3. Start stack: `make docker-up` (Postgres, Redis, API, Web)
4. Run migrations: `make db-migrate`
5. Or run locally: `make api-dev` and `make web-dev` in separate terminals

### URLs

| Resource | URL |
|----------|-----|
| Web app | http://localhost:5173 |
| Dashboard | http://localhost:5173/dashboard |
| API root | http://localhost:8000/ |
| API health | http://localhost:8000/api/v1/health |
| OpenAPI docs | http://localhost:8000/docs |

### Useful commands

```bash
make install       # backend (uv) + frontend (pnpm)
make api-dev       # FastAPI with reload
make web-dev       # Vite dev server
make api-check     # backend lint + types + tests
make web-check     # frontend lint + types + build
make check         # api-check + web-check
make db-migrate    # alembic upgrade head
make seed          # load idempotent demo data
make demo-reset    # wipe DB, migrate and seed
make docker-up     # postgres, redis, api, web
make docker-down
make docker-logs
```

**Local readiness:** [docs/LOCAL_TEST_AND_READINESS_REVIEW.md](docs/LOCAL_TEST_AND_READINESS_REVIEW.md)

See [docs/DEVELOPMENT_GUIDELINES.md](docs/DEVELOPMENT_GUIDELINES.md) for how we work on this repo step by step.

## Current project status

**Twelve vertical slices implemented:**

1. **Data Product API** — CRUD at `/api/v1/data-products`
2. **Work Item API + UI** — CRUD and board at `/api/v1/work-items`; work items can link to projects via `project_id`
3. **Projects API + UI** — CRUD at `/api/v1/projects` and `/api/v1/internal-projects` with summary counts
4. **Organization API + UI** — People, Teams and Capabilities with summary cards and person team/capability dropdowns
5. **Project management UI** — list, search/filter, create/edit/delete, detail pages and summary cards
6. **Organization management UI** — people directory, teams and capabilities with deactivate/delete flows
7. **Demo seed data** — `make seed` loads realistic local data for catalog, work, projects and organization
8. **Dashboard** — executive and operational insights at `/dashboard` with overall health scores, actionable insights, work delivery, project/data product/compliance/performance/automation/notification health and recent activity
9. **Global search** — top bar search across catalog, work, projects and organization with unified dropdown results
10. **Comments and activity** — plain-text comments and system-generated activity timeline on detail pages
11. **Relationship layer** — generic EntityLink connections between data products, work items, projects, people, teams and capabilities
12. **Files and evidence** — file metadata, external links, attach to entities, evidence flags on detail pages

Run `make seed` after migrations to populate the UI, dashboard and search for demos and screenshots. Seed is idempotent (`make seed` twice creates no duplicates).

### Verify comments and activity locally

```bash
make docker-up
make db-migrate
make seed
make api-dev    # terminal 1
make web-dev    # terminal 2
```

Open a detail page (e.g. http://localhost:5173/work-items/{id}), add a comment and confirm it appears in the comments section and activity timeline.

### Verify relationships locally

After `make seed`, open a seeded data product detail page — the Relationships section should show demo links (e.g. depends_on Finance KPI Layer). You can add links by pasting a target UUID from another object's detail page.

### Verify files and evidence locally

```bash
make docker-up
make db-migrate
make seed
make api-dev    # terminal 1
make web-dev    # terminal 2
```

1. Open http://localhost:5173/files — confirm seeded files appear
2. Create a new file metadata record with an external URL
3. Open a data product detail page — Files section shows seeded attachments
4. Attach an existing file by pasting its ID; mark as evidence
5. Detach a file and confirm activity updates

```bash
# Create file
curl -X POST http://localhost:8000/api/v1/files \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Finance KPI Definitions",
    "description": "Certified finance KPI definitions and ownership notes.",
    "file_type": "evidence",
    "sensitivity": "confidential",
    "external_url": "https://example.com/docs/finance-kpi-definitions",
    "version": "v1.0"
  }'

# Attach file
curl -X POST http://localhost:8000/api/v1/files/attachments \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "PASTE_FILE_ID",
    "entity_type": "data_product",
    "entity_id": "PASTE_DATA_PRODUCT_ID",
    "purpose": "Certified KPI evidence",
    "is_evidence": true,
    "evidence_type": "kpi_certification"
  }'

# Get entity files
curl http://localhost:8000/api/v1/files/entity/data_product/PASTE_DATA_PRODUCT_ID
```

### Sign in locally

After `make seed`, open http://localhost:5173 — you will be redirected to `/login`.

| Email | Password | Can write? |
|-------|----------|------------|
| admin@example.com | admin12345 | Yes (admin) |
| editor@example.com | editor12345 | Yes (editor) |
| viewer@example.com | viewer12345 | No (read only) |

```bash
# API login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin12345"}'
```

### Verify compliance locally

```bash
make docker-up
make db-migrate
make seed
make api-dev    # terminal 1
make web-dev    # terminal 2
```

1. Open http://localhost:5173/compliance — overview, policies and checks tables
2. Create a policy; open policy detail and view rules
3. Create a compliance check; add evidence by pasting a file ID
4. Open a data product detail page — Compliance section shows related checks

```bash
# Create policy
curl -X POST http://localhost:8000/api/v1/compliance/policies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Product Governance Policy",
    "description": "Minimum requirements for active data products.",
    "status": "active",
    "version": "v1.0"
  }'

# Create compliance check
curl -X POST http://localhost:8000/api/v1/compliance/checks \
  -H "Content-Type: application/json" \
  -d '{
    "subject_type": "data_product",
    "subject_id": "PASTE_DATA_PRODUCT_ID",
    "title": "Business owner assigned",
    "check_type": "manual",
    "status": "in_progress"
  }'

# Add evidence
curl -X POST http://localhost:8000/api/v1/compliance/checks/PASTE_CHECK_ID/evidence \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "PASTE_FILE_ID",
    "status": "submitted",
    "description": "Business owner approval document."
  }'

# Get entity compliance
curl http://localhost:8000/api/v1/compliance/entity/data_product/PASTE_DATA_PRODUCT_ID

### Automation API examples

```bash
# Create schedule
curl -X POST http://localhost:8000/api/v1/automation/schedules \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Data Product Review",
    "frequency": "monthly",
    "timezone": "UTC",
    "is_active": true
  }'

# Create trigger
curl -X POST http://localhost:8000/api/v1/automation/triggers \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Review Executive Sales Dashboard",
    "status": "active",
    "trigger_type": "schedule",
    "action_type": "create_work_item",
    "schedule_id": "PASTE_SCHEDULE_ID",
    "target_type": "data_product",
    "target_id": "PASTE_DATA_PRODUCT_ID",
    "action_config": {
      "title": "Review dashboard documentation",
      "priority": "medium",
      "due_in_days": 7
    }
  }'

# Run simulation
curl -X POST http://localhost:8000/api/v1/automation/triggers/PASTE_TRIGGER_ID/run \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"simulate": true}'

# Run real safe action
curl -X POST http://localhost:8000/api/v1/automation/triggers/PASTE_TRIGGER_ID/run \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"simulate": false}'

# Get entity automations
curl http://localhost:8000/api/v1/automation/entity/data_product/PASTE_DATA_PRODUCT_ID \
  -H "Authorization: Bearer PASTE_TOKEN"

### Worker API examples

Optional background worker for due automation triggers and queued notifications:

```bash
# Worker status
curl http://localhost:8000/api/v1/worker/status \
  -H "Authorization: Bearer PASTE_TOKEN"

# Due work summary
curl http://localhost:8000/api/v1/worker/due-work \
  -H "Authorization: Bearer PASTE_TOKEN"

# Run one cycle (editor/admin)
curl -X POST http://localhost:8000/api/v1/worker/run-once \
  -H "Authorization: Bearer PASTE_TOKEN"
```

CLI:

```bash
make worker-once
make worker-dev
docker compose --profile worker up worker
```

# Create metric definition
curl -X POST http://localhost:8000/api/v1/performance/metrics \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Product Quality Score",
    "code": "DP_QUALITY_SCORE",
    "subject_type": "data_product",
    "value_type": "score",
    "direction": "higher_is_better",
    "unit": "points",
    "target_value": 90,
    "status": "active"
  }'

# Create metric value
curl -X POST http://localhost:8000/api/v1/performance/values \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "metric_definition_id": "PASTE_METRIC_ID",
    "subject_type": "data_product",
    "subject_id": "PASTE_DATA_PRODUCT_ID",
    "period_start": "2026-06-01",
    "period_end": "2026-06-30",
    "value_numeric": 92,
    "status": "submitted",
    "source": "Manual demo seed"
  }'

# Get entity scorecard
curl http://localhost:8000/api/v1/performance/entity/data_product/PASTE_DATA_PRODUCT_ID/scorecard \
  -H "Authorization: Bearer PASTE_TOKEN"
```

### Notifications API (simulation-first)

```bash
# Create channel
curl -X POST http://localhost:8000/api/v1/notifications/channels \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Local In-App Notifications",
    "channel_type": "in_app",
    "status": "active",
    "description": "Local MVP notification records."
  }'

# Create template
curl -X POST http://localhost:8000/api/v1/notifications/templates \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Product Review Reminder",
    "status": "active",
    "event_type": "data_product_review",
    "subject_template": "Data product review: {{title}}",
    "body_template": "Please review {{title}}. Entity: {{entity_type}}/{{entity_id}}."
  }'

# Create message
curl -X POST http://localhost:8000/api/v1/notifications/messages \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "PASTE_CHANNEL_ID",
    "template_id": "PASTE_TEMPLATE_ID",
    "priority": "normal",
    "event_type": "manual",
    "subject": "Demo notification",
    "body": "This is a local simulated notification.",
    "recipient_type": "email",
    "recipient_value": "admin@example.com"
  }'

# Send simulation
curl -X POST http://localhost:8000/api/v1/notifications/messages/PASTE_MESSAGE_ID/send \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"simulate": true}'
```

External email, Teams, Slack and webhook delivery are **future scope**.

### Verify dashboard locally

```bash
make docker-up
make db-migrate
make seed
make api-dev    # terminal 1
make web-dev    # terminal 2
```

Open http://localhost:5173/dashboard — confirm executive summary, operational health, actionable insights and module insight cards load with seeded data.

Use the **top bar search** to find seeded records (e.g. `sales`, `Nikita`, `Internal Sea`, `Data Engineering`).

### Verify organization management locally

```bash
make docker-up
make db-migrate
make api-dev    # terminal 1
make web-dev    # terminal 2
```

1. Open http://localhost:5173/capabilities — create a capability
2. Open http://localhost:5173/teams — create a team
3. Open http://localhost:5173/people — create a person linked to team/capability
4. Open person detail — confirm summary cards
5. Edit person; deactivate person
6. Open team/capability detail — confirm summary cards; delete if unreferenced

### Verify organization APIs locally

```bash
make docker-up
make db-migrate
make api-dev
make api-check
```

Open http://localhost:8000/docs — test **People**, **Teams** and **Capabilities** tags.

1. Create a capability, team and person
2. List and filter people by team, seniority or active status
3. Open summary endpoints for relationship counts
4. Deactivate a person — confirm `is_active` becomes false

### Verify project management locally

```bash
make docker-up
make db-migrate
make api-dev    # terminal 1
make web-dev    # terminal 2
```

1. Open http://localhost:5173/projects
2. Create a client project — confirm it appears in the list
3. Search and filter by type, status or health
4. Open the detail page — confirm summary cards load
5. Edit and delete the project
6. Open http://localhost:5173/internal-projects
7. Create an internal project — confirm list, detail, edit and delete work

### Verify work management locally

```bash
make docker-up
make db-migrate
make api-dev    # terminal 1
make web-dev    # terminal 2
```

1. Open http://localhost:5173/work-items
2. Create a work item
3. Confirm it appears in the list; search and filter
4. Open detail page; edit and delete
5. Open http://localhost:5173/work-board
6. Confirm item appears in the correct status column
7. Use "Move to …" to advance status

Auth, drag-and-drop, comments and people/team/capability selectors are not implemented yet.

## Broader object scope

Internal Sea targets a full internal operating model:

| Domain | Examples | Status |
|--------|----------|--------|
| Catalog | Data products, dashboards, reports, datasets | **API live** for data products |
| Work | Work items, projects, meetings | **API + UI live** for work items and projects |
| People | People, teams, capabilities | **API + UI live** |
| Performance | Metric definitions, values, scorecards | **API + UI live** |
| Compliance | Policies, rules, controls, checks | **API + UI live** |
| Automation | Schedules, triggers, manual runs | **API + UI live** |
| Tools | Integrations, tool registry | Documented |
| Commercial | Deals, POC, pilot, MVP | Documented |
| Relationships | Entity links, activity, audit | Documented |

See [docs/DATA_MODEL.md](docs/DATA_MODEL.md) for MVP vs target scope.
