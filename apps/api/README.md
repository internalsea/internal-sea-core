# Internal Sea API

FastAPI backend for Internal Sea — an internal operating system connecting catalog, work, people, compliance, performance, tools and commercial pipeline.

**Local testing:** See [docs/LOCAL_TEST_AND_READINESS_REVIEW.md](../../docs/LOCAL_TEST_AND_READINESS_REVIEW.md).

## Purpose

This service exposes the HTTP API. Implemented slices:

- **Data Products** — `/api/v1/data-products`
- **Work Items** — `/api/v1/work-items` (includes board)
- **Projects** — `/api/v1/projects` and `/api/v1/internal-projects`
- **People** — `/api/v1/people`
- **Teams** — `/api/v1/teams`
- **Capabilities** — `/api/v1/capabilities`
- **Dashboard** — `/api/v1/dashboard/*` (read-only aggregates)
- **Search** — `/api/v1/search` (unified global search)
- **Comments** — nested comment endpoints on catalog, work and projects
- **Activity** — `/api/v1/activity` (read-only timeline)
- **Relationships** — `/api/v1/relationships` (generic EntityLink CRUD)
- **Files** — `/api/v1/files` (metadata, storages, attachments, evidence flags)

Also implemented: **Auth**, **Compliance**, **Automation**, **Performance**.

## Environment variables

Copy root `.env.example` to `.env`. Key variables:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Async Postgres URL |
| `JWT_SECRET_KEY` | Signing secret (change in production) |
| `AUTH_ENABLED` | `false` bypasses auth for local tests only |
| `CORS_ORIGINS` | Comma-separated browser origins |
| `DEBUG` | Enables verbose error details (must be `false` in production) |
| `LOG_LEVEL` | Logging verbosity |

Production-like `APP_ENV` values validate secrets and reject `DEBUG=true` and wildcard CORS.

## Health endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | Public | Service metadata (version, environment) |
| GET | `/api/v1/health/live` | Public | Liveness — no database |
| GET | `/api/v1/health/ready` | Public | Readiness — requires database |
| GET | `/api/v1/health/db` | Public | Database probe |

Migrations are **not** run on startup — use `make db-migrate`.

## Error responses

Standard shape:

```json
{
  "error": "not_found",
  "message": "Resource not found",
  "details": null,
  "request_id": "uuid"
}
```

Legacy fields `detail` and `code` are included for compatibility. Responses include `X-Request-ID` header.

## Auth

- `POST /api/v1/auth/login` — public
- `GET /api/v1/auth/me` — authenticated
- User management — admin only
- Business routes — `ViewerUser` (read), `EditorUser` (write)

## Testing

```bash
make api-test
make api-check   # lint + mypy + pytest
```

Default tests mock the database and disable auth (`AUTH_ENABLED=false` in conftest).

## Structure

```
apps/api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── db/                  # SQLAlchemy session and health
│   ├── domain/              # Shared enums
│   ├── models/              # SQLAlchemy models
│   ├── api/v1/              # Router aggregation
│   ├── core/                # Pagination, errors, logging
│   └── modules/             # Domain modules (see below)
├── alembic/
├── tests/
└── pyproject.toml
```

## Data Product API

Base path: `/api/v1/data-products`  
OpenAPI tag: **Catalog**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/data-products` | List with filters and pagination |
| POST | `/api/v1/data-products` | Create |
| GET | `/api/v1/data-products/{id}` | Get by ID |
| PATCH | `/api/v1/data-products/{id}` | Partial update |
| DELETE | `/api/v1/data-products/{id}` | Delete |

## Work Item API

Base path: `/api/v1/work-items`  
OpenAPI tag: **Work**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/work-items` | List with filters and pagination |
| GET | `/api/v1/work-items/board` | Board columns grouped by status |
| POST | `/api/v1/work-items` | Create |
| GET | `/api/v1/work-items/{id}` | Get by ID |
| PATCH | `/api/v1/work-items/{id}` | Partial update |
| DELETE | `/api/v1/work-items/{id}` | Delete |

Supports `project_id` on create/update and as a list/board filter.

## Projects API

Base path: `/api/v1/projects`  
OpenAPI tag: **Projects**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/projects` | List with filters and pagination |
| POST | `/api/v1/projects` | Create |
| GET | `/api/v1/projects/{id}` | Get by ID |
| GET | `/api/v1/projects/{id}/summary` | Work item counts summary |
| PATCH | `/api/v1/projects/{id}` | Partial update |
| DELETE | `/api/v1/projects/{id}` | Delete |

### Query parameters (list)

`search`, `project_type`, `status`, `client_name`, `account_name`, `owner_id`, `team_id`, `capability_id`, `health_status`, `starts_after`, `ends_before`, `page`, `page_size`

## Internal Projects API

Base path: `/api/v1/internal-projects`  
OpenAPI tag: **Internal Projects**

Same operations as Projects, filtered to `project_type = internal_project`. Create always forces internal project type.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/internal-projects` | List internal projects |
| POST | `/api/v1/internal-projects` | Create (forces `internal_project`) |
| GET | `/api/v1/internal-projects/{id}` | Get if internal project |
| PATCH | `/api/v1/internal-projects/{id}` | Update if internal project |
| DELETE | `/api/v1/internal-projects/{id}` | Delete if internal project |

### Example requests

```bash
# Create client project
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Finance Data Platform Migration",
    "description": "Client project for migration and reporting foundation.",
    "project_type": "client_project",
    "status": "active",
    "client_name": "Example Client",
    "health_status": "healthy"
  }'

# Create internal project
curl -X POST "http://localhost:8000/api/v1/internal-projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Internal Sea MVP",
    "description": "Internal product build for catalog, work and capability management.",
    "status": "active",
    "health_status": "healthy"
  }'

# Project summary (work item counts)
curl "http://localhost:8000/api/v1/projects/{id}/summary"

# Link work item to project
curl -X PATCH "http://localhost:8000/api/v1/work-items/{id}" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "{project_id}"}'
```

## People API

Base path: `/api/v1/people`  
OpenAPI tag: **People**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/people` | List with filters and pagination |
| POST | `/api/v1/people` | Create |
| GET | `/api/v1/people/{id}` | Get by ID |
| GET | `/api/v1/people/{id}/summary` | Work item, data product and project counts |
| PATCH | `/api/v1/people/{id}` | Partial update |
| DELETE | `/api/v1/people/{id}` | Deactivate (`is_active = false`) |

### Query parameters (list)

`search`, `team_id`, `capability_id`, `seniority_level`, `is_active`, `location`, `min_availability`, `max_availability`, `page`, `page_size`

## Teams API

Base path: `/api/v1/teams`  
OpenAPI tag: **Teams**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/teams` | List with search and pagination |
| POST | `/api/v1/teams` | Create |
| GET | `/api/v1/teams/{id}` | Get by ID |
| GET | `/api/v1/teams/{id}/summary` | People, data product, work item and project counts |
| PATCH | `/api/v1/teams/{id}` | Partial update |
| DELETE | `/api/v1/teams/{id}` | Delete (409 if referenced) |

## Capabilities API

Base path: `/api/v1/capabilities`  
OpenAPI tag: **Capabilities**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/capabilities` | List with search and pagination |
| POST | `/api/v1/capabilities` | Create |
| GET | `/api/v1/capabilities/{id}` | Get by ID |
| GET | `/api/v1/capabilities/{id}/summary` | People, data product, work item and project counts |
| PATCH | `/api/v1/capabilities/{id}` | Partial update |
| DELETE | `/api/v1/capabilities/{id}` | Delete (409 if referenced) |

### Organization example requests

```bash
# Create capability
curl -X POST "http://localhost:8000/api/v1/capabilities" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Engineering",
    "description": "Builds and operates data pipelines, data products and platform integrations."
  }'

# Create team
curl -X POST "http://localhost:8000/api/v1/teams" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Core Platform Team",
    "description": "Internal Sea product and platform team."
  }'

# Create person
curl -X POST "http://localhost:8000/api/v1/people" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nikita Rogatov",
    "email": "nikita@example.com",
    "role_title": "Partner, Data Engineering and Cloud",
    "seniority_level": "partner",
    "availability_percent": 80,
    "location": "Netherlands"
  }'
```

## Dashboard API

Base path: `/api/v1/dashboard`  
OpenAPI tag: **Dashboard**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/dashboard/summary` | Counts across catalog, work, projects and organization |
| GET | `/api/v1/dashboard/recent-data-products` | Latest updated data products (`limit`, default 8) |
| GET | `/api/v1/dashboard/high-priority-work-items` | Open high/critical work items (`limit`, default 10) |
| GET | `/api/v1/dashboard/project-health` | Active and at-risk projects with work counts (`limit`, default 8) |
| GET | `/api/v1/dashboard/capability-workload` | Per-capability people, work and delivery load |
| GET | `/api/v1/dashboard/ownership-gaps` | Missing owners, teams and assignees (`limit`, default 10) |
| GET | `/api/v1/dashboard/executive-summary` | Executive KPIs and overall score |
| GET | `/api/v1/dashboard/operational-health` | Domain health scores and risk counts |
| GET | `/api/v1/dashboard/data-product-health` | Data product quality and ownership health (`limit`, default 10) |
| GET | `/api/v1/dashboard/work-delivery` | Work item delivery breakdown |
| GET | `/api/v1/dashboard/project-insights` | Project health insights (`limit`, default 10) |
| GET | `/api/v1/dashboard/compliance-insights` | Compliance checks and overdue items (`limit`, default 10) |
| GET | `/api/v1/dashboard/performance-insights` | Performance scorecards and metric gaps (`limit`, default 10) |
| GET | `/api/v1/dashboard/automation-health` | Triggers, schedules and run failures (`limit`, default 10) |
| GET | `/api/v1/dashboard/notification-health` | Channels, templates and failed messages (`limit`, default 10) |
| GET | `/api/v1/dashboard/recent-activity` | Recent activity feed (`limit`, default 15) |
| GET | `/api/v1/dashboard/actionable-insights` | Deterministic actionable insights (`limit`, default 20) |
| GET | `/api/v1/dashboard/advanced` | Combined advanced dashboard payload |

All dashboard endpoints require **viewer** authentication.

### Example requests

```bash
# Summary metrics
curl http://localhost:8000/api/v1/dashboard/summary \
  -H "Authorization: Bearer PASTE_TOKEN"

# Executive summary
curl http://localhost:8000/api/v1/dashboard/executive-summary \
  -H "Authorization: Bearer PASTE_TOKEN"

# Actionable insights
curl http://localhost:8000/api/v1/dashboard/actionable-insights \
  -H "Authorization: Bearer PASTE_TOKEN"

# Automation health
curl http://localhost:8000/api/v1/dashboard/automation-health \
  -H "Authorization: Bearer PASTE_TOKEN"

# Project health
curl "http://localhost:8000/api/v1/dashboard/project-health?limit=8" \
  -H "Authorization: Bearer PASTE_TOKEN"

# Ownership gaps
curl "http://localhost:8000/api/v1/dashboard/ownership-gaps?limit=10" \
  -H "Authorization: Bearer PASTE_TOKEN"
```

## Search API

Base path: `/api/v1/search`  
OpenAPI tag: **Search**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/search` | Unified search across catalog, work, projects, organization, files and compliance |
| GET | `/api/v1/search/entity/{entity_type}/{entity_id}` | Lookup a single entity by type and ID for display labels |

### Supported `types` filter values

`data_product`, `work_item`, `project`, `internal_project`, `person`, `team`, `capability`, `file`, `policy`, `compliance_check`

### Query parameters

`q` (required, min 2 chars), `types` (optional, repeatable), `limit` (default 20, max 50)

Entity lookup returns `EntityLookupResult` (`id`, `type`, `title`, `description`, `status`, `secondary_status`, `url`) — used by the frontend `EntityReference` component.

### Examples

```bash
curl "http://localhost:8000/api/v1/search?q=sales"
curl "http://localhost:8000/api/v1/search?q=nikita&types=person&limit=10"
curl "http://localhost:8000/api/v1/search?q=governance&types=policy"
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/search/entity/person/PASTE_PERSON_ID"
```

## Comments API

OpenAPI tag: **Comments**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/data-products/{id}/comments` | List comments |
| POST | `/api/v1/data-products/{id}/comments` | Add comment |
| GET | `/api/v1/work-items/{id}/comments` | List comments |
| POST | `/api/v1/work-items/{id}/comments` | Add comment |
| GET | `/api/v1/projects/{id}/comments` | List comments |
| POST | `/api/v1/projects/{id}/comments` | Add comment |
| GET | `/api/v1/internal-projects/{id}/comments` | List comments (internal only) |
| POST | `/api/v1/internal-projects/{id}/comments` | Add comment (internal only) |
| PATCH | `/api/v1/comments/{id}` | Update comment |
| DELETE | `/api/v1/comments/{id}` | Delete comment |

### Example requests

```bash
# Add comment to data product
curl -X POST "http://localhost:8000/api/v1/data-products/{id}/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "Business owner confirmed that this product is still active."
  }'
```

## Activity API

Base path: `/api/v1/activity`  
OpenAPI tag: **Activity**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/activity` | List activity with optional filters |
| GET | `/api/v1/activity/{entity_type}/{entity_id}` | List activity for one entity |

Activity events are system-generated by domain services. No public create endpoint in MVP.

### Example requests

```bash
# Activity for a data product
curl "http://localhost:8000/api/v1/activity/data_product/{id}"
```

## Relationships API

Base path: `/api/v1/relationships`  
OpenAPI tag: **Relationships**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/relationships` | List links with filters |
| POST | `/api/v1/relationships` | Create link |
| GET | `/api/v1/relationships/entity/{type}/{id}` | Outgoing + incoming view |
| GET | `/api/v1/relationships/{id}` | Get link |
| PATCH | `/api/v1/relationships/{id}` | Update link |
| DELETE | `/api/v1/relationships/{id}` | Delete link |

### Example requests

```bash
# Create relationship
curl -X POST "http://localhost:8000/api/v1/relationships" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "data_product",
    "source_id": "PASTE_DATA_PRODUCT_ID",
    "target_type": "work_item",
    "target_id": "PASTE_WORK_ITEM_ID",
    "link_type": "improves",
    "title": "Work item improves this data product",
    "description": "This task improves documentation and quality status."
  }'

# Get relationships for entity
curl "http://localhost:8000/api/v1/relationships/entity/data_product/PASTE_DATA_PRODUCT_ID"
```

## Files API

Base path: `/api/v1/files`  
OpenAPI tag: **Files**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/files` | List file assets with filters |
| POST | `/api/v1/files` | Create file metadata |
| GET | `/api/v1/files/{id}` | Get file |
| PATCH | `/api/v1/files/{id}` | Update file |
| DELETE | `/api/v1/files/{id}` | Soft-delete (status = deleted) |
| GET | `/api/v1/files/storages` | List storage backends |
| POST | `/api/v1/files/storages` | Create storage |
| POST | `/api/v1/files/attachments` | Attach file to entity |
| DELETE | `/api/v1/files/attachments/{id}` | Detach file |
| GET | `/api/v1/files/entity/{type}/{id}` | List files for entity |
| GET | `/api/v1/files/{id}/attachments` | List entities where file is attached |

### Example requests

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

No binary upload, download or preview endpoints yet.

## Tenancy API

Base path: `/api/v1/tenancy`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/onboarding/first-user` | Public | Create first user, company, workspace (empty system only) |
| GET | `/current` | Bearer | Current company/workspace/member context |
| GET | `/companies` | Bearer | Companies for current user |
| POST | `/companies` | Bearer | Create company (owner membership) |
| GET/PATCH | `/companies/{id}` | Bearer / Admin+ | Company read/update |
| GET/POST | `/companies/{id}/workspaces` | Bearer / Admin+ | Workspace list/create |
| GET/PATCH | `/workspaces/{id}` | Bearer / Admin+ | Workspace read/update |
| GET/POST | `/companies/{id}/members` | Bearer / Admin+ | Member list/add |
| PATCH/DELETE | `/members/{id}` | Admin+ | Update/remove member |

Send optional headers `X-Company-ID` and `X-Workspace-ID` when the user belongs to multiple companies.

### Examples

```bash
curl http://localhost:8000/api/v1/tenancy/current \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "X-Company-ID: PASTE_COMPANY_ID" \
  -H "X-Workspace-ID: PASTE_WORKSPACE_ID"
```

## Auth API

Base path: `/api/v1/auth`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/login` | Public | Login with email/password |
| GET | `/me` | Bearer | Current user |
| POST | `/logout` | Bearer | Logout acknowledgement |
| GET | `/users` | Admin | List users |
| POST | `/users` | Admin | Create user |
| GET/PATCH/DELETE | `/users/{id}` | Admin | User CRUD / deactivate |

### Demo credentials (local seed)

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin12345 | admin |
| editor@example.com | editor12345 | editor |
| viewer@example.com | viewer12345 | viewer |

### Examples

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin12345"
  }'

# Current user
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer PASTE_TOKEN"

# Create data product (requires editor or admin token)
curl -X POST http://localhost:8000/api/v1/data-products \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Product",
    "type": "dataset",
    "status": "draft"
  }'
```

All module endpoints except `/health` and `/auth/login` require a valid bearer token when `AUTH_ENABLED=true`.

See [app/modules/auth/README.md](app/modules/auth/README.md).

## Compliance API

Base path: `/api/v1/compliance`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/overview` | Compliance summary counts |
| GET/POST | `/policies` | List/create policies |
| GET/PATCH/DELETE | `/policies/{id}` | Policy CRUD |
| GET | `/policies/{id}/rules` | Rules for a policy |
| GET/POST | `/rules` | List/create rules |
| GET/PATCH/DELETE | `/rules/{id}` | Rule CRUD |
| GET/POST | `/controls` | List/create controls |
| GET/PATCH/DELETE | `/controls/{id}` | Control CRUD |
| GET | `/rules/{id}/controls` | Controls for a rule |
| GET/POST | `/checks` | List/create compliance checks |
| GET/PATCH/DELETE | `/checks/{id}` | Check CRUD |
| GET | `/entity/{subject_type}/{subject_id}` | Checks for an entity |
| GET/POST | `/checks/{id}/evidence` | List/add evidence |
| PATCH/DELETE | `/evidence/{id}` | Update/delete evidence |

### Examples

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
    "description": "Check that active data product has a business owner.",
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
```

See [app/modules/compliance/README.md](app/modules/compliance/README.md).

## Automation API

Base path: `/api/v1/automation`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/overview` | Automation summary counts |
| GET/POST | `/schedules` | List/create schedules |
| GET/PATCH/DELETE | `/schedules/{id}` | Schedule CRUD |
| GET/POST | `/triggers` | List/create triggers |
| GET/PATCH/DELETE | `/triggers/{id}` | Trigger CRUD |
| GET | `/triggers/{id}/runs` | Run history for trigger |
| POST | `/triggers/{id}/run` | Manual run (`simulate` default `true`) |
| GET | `/runs` | List runs |
| GET | `/entity/{target_type}/{target_id}` | Triggers for entity |

```bash
curl -X POST http://localhost:8000/api/v1/automation/schedules \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Monthly Data Product Review", "frequency": "monthly", "timezone": "UTC", "is_active": true}'

curl -X POST http://localhost:8000/api/v1/automation/triggers/PASTE_TRIGGER_ID/run \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"simulate": true}'
```

See [app/modules/automation/README.md](app/modules/automation/README.md).

## Performance API

Base path: `/api/v1/performance`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/overview` | Performance summary counts |
| GET/POST | `/metrics` | List/create metric definitions |
| GET/PATCH/DELETE | `/metrics/{id}` | Definition CRUD |
| GET/POST | `/values` | List/create metric values |
| GET/PATCH/DELETE | `/values/{id}` | Value CRUD |
| GET | `/entity/{subject_type}/{subject_id}/scorecard` | Entity scorecard |
| GET | `/entity/{subject_type}/{subject_id}/values` | Values for entity |

```bash
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

curl http://localhost:8000/api/v1/performance/entity/data_product/PASTE_DATA_PRODUCT_ID/scorecard \
  -H "Authorization: Bearer PASTE_TOKEN"
```

See [app/modules/performance/README.md](app/modules/performance/README.md).

## Notifications API

Base path: `/api/v1/notifications`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/overview` | Notification summary counts |
| GET/POST | `/channels` | List/create channels |
| GET/PATCH/DELETE | `/channels/{id}` | Channel CRUD |
| GET/POST | `/templates` | List/create templates |
| POST | `/templates/render` | Render template preview |
| GET/POST | `/preferences` | List/create preferences |
| GET/POST | `/messages` | List/create messages |
| POST | `/messages/{id}/send` | Send/simulate message |
| POST | `/messages/{id}/queue` | Queue draft message for worker |
| GET | `/messages/{id}/delivery-attempts` | Message delivery history |
| GET | `/entity/{entity_type}/{entity_id}` | Entity-linked messages |

Simulation is default (`simulate: true`). External providers are not called in MVP.

```bash
curl -X POST http://localhost:8000/api/v1/notifications/messages/PASTE_MESSAGE_ID/send \
  -H "Authorization: Bearer PASTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"simulate": true}'
```

See [app/modules/notifications/README.md](app/modules/notifications/README.md).

## Worker API

Base path: `/api/v1/worker`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/status` | viewer | Worker config and due counts |
| GET | `/due-work` | viewer | Due and locked work summary |
| POST | `/run-once` | editor | Run one in-process worker cycle |

CLI (separate process):

```bash
make worker-once
make worker-dev
uv run python -m app.worker.main run-once
uv run python -m app.worker.main run-loop --interval 30
```

Docker: `docker compose --profile worker up worker`

See [app/worker/README.md](app/worker/README.md).

## Future module placeholders

Under `app/modules/` — documented, not all registered yet:

`tools`, `meetings`, `deals`, `pilots`, `mvps`

## Database

SQLAlchemy 2.0 async + Alembic. Run `make db-migrate` after pulling migrations.

Latest migration: `0012_worker_execution_foundation` — worker locking fields and indexes.

Previous: `0011_notifications_foundation` — notification channels, templates, messages and delivery attempts.

Previous: `0010_performance_metrics` — performance metric definitions and values.

Previous: `0009_automation_foundation` — automation schedules, triggers and runs.

Previous: `0008_auth_permissions` — adds `is_superuser`, `last_login_at`; migrates `is_admin` to `is_superuser`.

| Local API / seed | `DATABASE_URL` host = `localhost` |
| Docker API | `DATABASE_URL` host = `postgres` |

## Seed data

Populate the local database with demo records:

```bash
make seed
# or
cd apps/api && uv run python -m app.seed.seed
```

Full demo reset (wipe volumes, migrate, seed):

```bash
make demo-reset
```

### What is created

| Category | Count |
|----------|------:|
| Capabilities | 8 |
| Teams | 5 |
| People | 10 |
| Business domains | 6 |
| Client projects | 3 |
| Internal projects | 3 |
| Data products | 6 |
| Work items | 10 |
| File storages | 2 |
| File assets | 4 |
| Policies | 2 |
| Compliance rules | 5 |
| Controls | 3 |
| Compliance checks | 4 |
| Auth users | 3 (+ reporter users from work items) |

Seed is **idempotent** — safe to run multiple times. See [app/seed/README.md](app/seed/README.md).

## Commands

```bash
make install
make db-migrate
make seed          # demo data (optional)
make api-dev
make api-check
```

Docs: http://localhost:8000/docs

## Next steps

1. **Prompt 22:** Entity picker / smart relationship selector
2. Automation triggers and schedules
3. Automation triggers and schedules

See [docs/IMPLEMENTATION_ROADMAP.md](../../docs/IMPLEMENTATION_ROADMAP.md).
