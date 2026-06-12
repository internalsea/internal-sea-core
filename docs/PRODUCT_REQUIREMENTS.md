# Product Requirements

High-level requirements for Internal Sea. Detailed stories and acceptance criteria are added per phase.

## MVP scope (implement now)

The first usable version focuses on catalog, work, people and basic relationships:

| Area | MVP deliverable |
|------|-----------------|
| **Catalog** | Data Products CRUD API and UI (API done in Phase 5) |
| **Work** | Work Items CRUD API and UI — list, board, create/edit/delete (**implemented**) |
| **Projects** | Projects and Internal Projects CRUD API and UI — list, search/filter, create/edit/delete, detail, summary cards (**implemented**) |
| **People** | People, Teams, Capabilities CRUD API and UI with filters and summary counts (**implemented**) |
| **Relationships** | Generic EntityLink layer connecting core objects (**implemented**) |
| **Dashboard** | Executive and operational insights hub — summary, health scores, actionable insights, module health cards and recent activity (**implemented**) |
| **Search** | Global search across catalog, work, projects and organization (**implemented**) |
| **Collaboration** | Comments and activity timeline on detail pages (**implemented**) |
| **Files** | File metadata, external links and evidence attachments (**implemented**) |
| **Compliance** | Policies, rules, controls, checks and evidence (**implemented**) |
| **Auth** | Login/logout, JWT, roles, protected writes (**implemented**) |

### MVP must have

| ID | Requirement |
|----|-------------|
| PR-01 | Catalog data products (CRUD API **implemented**) |
| PR-02 | Manage work items (**list, board, CRUD UI implemented**) |
| PR-02b | Manage projects and internal projects (**implemented** — list, CRUD, summary, work item linking, UI) |
| PR-03 | Manage people, teams and capabilities (**implemented** — list, CRUD, filters, summary counts, UI) |
| PR-04 | Link work to data products and **projects** |
| PR-05 | Show ownership on catalog objects |
| PR-06 | Dashboard (**implemented** — executive summary, operational health, actionable insights, work delivery, project/data product/compliance/performance/automation/notification insights, recent activity) |
| PR-07 | Demo dataset for local testing (**implemented** — `make seed`) |
| PR-08 | Global search (**implemented** — top bar dropdown, unified results, click to navigate) |
| PR-09 | Comments and activity timeline (**implemented** — plain-text comments, system activity feed) |
| PR-10 | Relationship layer (**implemented** — EntityLink create/list/delete on detail pages) |
| PR-11 | Files and evidence (**implemented** — metadata, external links, attach to entities, evidence flags) |
| PR-12 | Compliance foundation (**implemented** — policies, checks, evidence, entity compliance section) |
| PR-13 | Auth and permissions (**implemented** — login/logout, JWT, admin/editor/viewer roles, protected API and UI writes) |

### Relationship Layer MVP

| Capability | Status |
|------------|--------|
| Create links between supported entities | **Implemented** |
| List outgoing and incoming links per entity | **Implemented** |
| Delete links | **Implemented** |
| Dependency, blocker, ownership, support link types | **Implemented** |
| Relationships section on detail pages | **Implemented** |
| Activity events for link/unlink | **Implemented** |
| Entity picker in relationship forms | **Implemented** |
| Readable entity references on detail pages | **Implemented** |

No graph visualization or AI suggestions yet. Manual UUID fallback available in advanced form sections.

### Comments and Activity MVP

| Capability | Status |
|------------|--------|
| Comments on data products | **Implemented** |
| Comments on work items | **Implemented** |
| Comments on projects and internal projects | **Implemented** |
| Activity events for create/update/delete/comment/status changes | **Implemented** |
| Activity timeline on detail pages | **Implemented** |

Plain text only — no rich text, attachments, notifications or full audit logging yet.

### Files and Evidence MVP

| Capability | Status |
|------------|--------|
| Register file metadata | **Implemented** |
| Register external document links | **Implemented** |
| Attach files to data products, work items, projects and internal projects | **Implemented** |
| Mark attachments as evidence with evidence type | **Implemented** |
| Show files on entity detail pages | **Implemented** |
| Prepare for compliance evidence workflows | **Implemented** (metadata layer) |

No binary upload, file preview, cloud storage integration or compliance checks yet.

### Global search MVP

| Capability | Status |
|------------|--------|
| Search data products | **Implemented** |
| Search work items | **Implemented** |
| Search projects and internal projects | **Implemented** |
| Search people, teams, capabilities | **Implemented** |
| Result dropdown in top bar | **Implemented** |
| Click result to navigate | **Implemented** |

Uses simple PostgreSQL `ilike` matching — no external search engine.

### Entity Picker MVP

| Capability | Status |
|------------|--------|
| Search/select entity in forms | **Implemented** |
| Display entity names instead of UUIDs on detail pages | **Implemented** |
| Relationship target selector | **Implemented** |
| File selector for attachments and evidence | **Implemented** |
| Compliance subject selector | **Implemented** |
| Owner / team / capability selectors | **Implemented** |
| Entity lookup API for display labels | **Implemented** |
| Search files, policies and compliance checks | **Implemented** |

No AI suggestions, graph visualization or multi-select pickers yet.

### Demo dataset

The seed command (`make seed`) supports testing without manual data entry:

| Area | Demo coverage |
|------|----------------|
| **Catalog** | Business domains and data products with owners, teams and quality status |
| **Work board** | Work items across statuses, types and priorities linked to projects |
| **Project management** | Client projects, internal projects, budgets and health status |
| **Organization management** | People, teams and capabilities with relationships |

Seed is idempotent and intended for local/demo use only.

---

## Target scope (documented, not MVP)

Grouped requirements for the full operating model. **Not implemented yet** unless noted.

### Catalog and business assets

- Data products, dashboards, reports, files, datasets, metrics, KPIs, APIs, AI agents, automations
- File storage backends (S3, SharePoint, etc.)
- MVP: asset types represented via `DataProduct.type`

### Project and work management

- Projects, internal projects, initiatives, roadmap items — **API + UI live** (`project_type` discriminator)
- Work items, epics, tasks, bugs, risks, decisions, technical debt
- **Work item ↔ project linking via `project_id`** (API + UI entity picker live)
- MVP: work item types via `WorkItem.type`; **list and board UI live**; **project list, detail, summary cards live**
- Future: compliance checks, performance metrics, meetings and files on project detail

### Team and capability management

- People, teams, capabilities, skills, allocations, roles, seniority
- MVP: **People/Teams/Capabilities API + UI live** — create/list/update/deactivate, search/filter, summary cards, team/capability dropdowns on person form
- Skills and allocations later

### Performance

- Team, project, person and capability performance metrics
- Utilization, capacity, velocity, quality, SLA adherence, delivery health
- Target only — no API yet

### Compliance and governance

- MVP: **Compliance Foundation live** — policies, rules, controls, compliance checks, evidence links, entity compliance section, compliance overview
- Manual checks only; no automated rule execution, schedules or approvals yet
- Exceptions and approvals: target only

### Policies and rules

- MVP: policy CRUD, rule/control display, rule severity and subject type
- Automated compliance evaluation: target only

### Automation foundation (MVP)

- Schedules, triggers, manual run, simulation, run history, entity automation section
- Safe action types: create work item, add comment, create activity event, send notification (simulation)
- Background worker MVP: optional worker process, due trigger scan, queued notification processing, run history, worker status UI
- Real external notifications, webhooks and AI actions: future

### Background Worker (MVP)

- Worker process (`run-once`, `run-loop`)
- Due automation scanning and `next_run_at` updates
- Queued notification processing (simulation default)
- Worker status and due-work API; manual run-once for editors
- Docker worker profile (optional)

### Notification Channels (MVP)

- Channels, templates, preferences, messages and delivery attempts
- Simulated sending (default); in-app record marking when not simulating on in-app channels
- Automation `send_notification` action (simulation only)
- `NotificationsSection` on data product, work item, project, internal project and compliance check detail pages
- External email/Teams/Slack delivery is future scope

### Performance Metrics (MVP)

- Metric definitions and manual metric values
- Entity scorecards with simple score, trend and interpretation
- `PerformanceSection` on people, teams, capabilities, projects, internal projects and data products
- Seeded demo scorecards for screenshots
- Automatic calculation, advanced analytics, HR review workflows and compensation use: future

### Advanced Dashboard (MVP)

| Capability | Status |
|------------|--------|
| Executive summary (overall score, KPI counts) | **Implemented** |
| Operational health scores (work, project, compliance, performance, automation) | **Implemented** |
| Actionable insights (deterministic rules, severity sort) | **Implemented** |
| Work delivery breakdown | **Implemented** |
| Project insights | **Implemented** |
| Data product health | **Implemented** |
| Compliance insights | **Implemented** |
| Performance insights and metric gaps | **Implemented** |
| Automation and worker queue health | **Implemented** |
| Notification health | **Implemented** |
| Recent activity feed | **Implemented** |

No AI-generated insights, external BI embedding, real-time streaming or heavy charting. Scores are transparent heuristics over existing PostgreSQL data.

### SaaS tenant foundation

| Capability | Status |
|------------|--------|
| Company and Workspace hierarchy | **Implemented** |
| CompanyMember roles (owner/admin/editor/viewer) | **Implemented** |
| First-user onboarding | **Implemented** |
| Tenant-scoped data (`company_id` / `workspace_id`) | **Implemented** (priority modules) |
| Current company/workspace context in UI | **Implemented** |
| Demo company seed (Internal Sea Demo) | **Implemented** |

No CRM Account module, billing, subscriptions, SSO or invite emails in this phase.

### Tools

- Tool registry, categories, integrations
- Target only

### Commercial pipeline

- Potential deals, opportunities, POC, pilot, MVP, client/account, deal stages
- Experiment progression into projects
- Target only

### Meetings

- Meeting types, action items, links to projects and compliance
- Target only

### Files and evidence

- MVP: file metadata, attachments on data products, work items, projects and internal projects; evidence flags
- Compliance evidence links via compliance check evidence records
- Binary upload, meetings and deals attachments: target only

### Relationship layer (extended)

- External references, graph visualization, AI relationship suggestions
- Policy/rule/compliance entity links in relationship picker (future)

---

## Post-MVP (near term)

| ID | Requirement |
|----|-------------|
| PR-11 | Files and evidence foundation |

## Later

| ID | Requirement |
|----|-------------|
| PR-12 | AI assistant and summarization |

## Non-functional expectations

- Internal SaaS usability, secrets out of repo, monorepo maintainability, health checks and structured logging

## Traceability

See [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) and [DATA_MODEL.md](DATA_MODEL.md).
