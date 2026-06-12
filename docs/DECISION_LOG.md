# Decision Log

Architecture Decision Records (ADRs) for Internal Sea. New decisions append with the next ADR number.

---

## ADR-0001: Use monorepo

**Status:** Accepted

**Context:** Internal Sea combines catalog, work management and team capability features. Shared domain types, auth and database access will be reused by the API and future workers. Splitting into multiple repositories early would add coordination overhead without current scale requirements.

**Decision:** Use a single repository with `apps/` for deployables and `packages/` for shared Python libraries.

**Consequences:**

- One clone, one CI pipeline, atomic cross-package changes.
- Clear ownership of shared code; risk of tight coupling if package boundaries are ignored.
- Frontend and backend version together; document API compatibility in release notes when needed.

---

## ADR-0002: Use Python FastAPI backend

**Status:** Accepted

**Context:** The team is Python-first. We need async-capable APIs, automatic OpenAPI docs and fast iteration for internal tools.

**Decision:** Implement the backend with FastAPI under `apps/api/`.

**Consequences:**

- Strong typing with Pydantic; excellent developer experience for API-first work.
- Python ecosystem for data and integrations aligns with catalog and analytics adjacency.
- Frontend remains a separate React app; no server-rendered Python templates in MVP.

---

## ADR-0003: Use React TypeScript frontend

**Status:** Accepted

**Context:** Internal users need responsive, table-heavy UIs with clear navigation. The team wants typed components and a mainstream hiring pool.

**Decision:** Build the frontend with React, TypeScript and Vite under `apps/web/`. Use pnpm as the package manager.

**Consequences:**

- Fast dev server via Vite; standard component model for complex dashboards.
- Separate deployment artifact from API; CORS and auth must be configured explicitly.
- Type sharing with backend is manual or codegen until we add tooling.

---

## ADR-0004: Use PostgreSQL

**Status:** Accepted

**Context:** Relational data with ownership, links and reporting queries fits a relational model. We need ACID transactions and mature tooling.

**Decision:** PostgreSQL 16 as the primary database. SQLAlchemy 2.0 and Alembic added in Phase 3. Redis for cache/session/queue as needed.

**Consequences:**

- Rich querying for dashboards and relationships; familiar ops story.
- Migrations required for schema changes; model design should stay intentional.
- Redis is optional for MVP features but available in Compose from Phase 1.

---

## ADR-0005: Use flat uppercase docs structure

**Status:** Accepted

**Context:** Consistency with existing team projects improves discoverability. Product and engineering docs should be easy to find at repo root level.

**Decision:** Store documentation as flat uppercase Markdown files in `/docs` (e.g. `PROJECT_VISION.md`, `DATA_MODEL.md`).

**Consequences:**

- Predictable paths for humans and AI prompts; no nested doc hierarchy to navigate.
- Filenames are verbose; sorting groups related topics alphabetically.
- Cross-link with relative paths between docs in the same folder.

---

## ADR-0006: Use SonarCloud for code quality

**Status:** Accepted

**Context:** The monorepo will grow across Python and TypeScript with shared packages. We want consistent quality gates, security hotspot tracking and coverage trends in one place, integrated with GitHub pull requests.

**Decision:** Use SonarCloud with root `sonar-project.properties` and a dedicated GitHub Actions workflow (`.github/workflows/sonarcloud.yml`). Enforce the quality gate on pushes to `main`; run analysis without blocking on pull requests until the gate is stable.

**Consequences:**

- Requires `SONAR_TOKEN` in GitHub repository secrets and matching org/project keys in SonarCloud.
- Coverage paths must be produced by CI test jobs as backend and frontend are implemented.
- Placeholder org/project keys in `sonar-project.properties` must be replaced before the first successful scan.

---

## ADR-0010: Use one Project model with project_type

**Status:** Accepted

**Context:** Internal Sea manages client projects, internal projects, POCs, pilots, MVPs and initiatives. These share most fields (name, status, dates, owner, team, budget) but differ in how users browse and filter them.

**Decision:** Use a single `projects` table with a `project_type` enum discriminator. Expose two API views: `/api/v1/projects` (all types) and `/api/v1/internal-projects` (filtered to `internal_project` by default). Do not create separate `projects` and `internal_projects` tables.

**Consequences:**

- One migration, one repository and one service — less duplication.
- Internal project routes enforce type constraints on create/read/update/delete.
- UI can still present separate navigation for Projects vs Internal Projects.
- If types diverge significantly later, extract specialized tables or use JSON metadata before splitting.

---

## ADR-0011: Deactivate people instead of deleting them

**Status:** Accepted

**Context:** People are referenced by work items (assignee), data products (business/technical owner) and projects (owner). Hard-deleting a person would break historical delivery records or require complex cascade rules.

**Decision:** `DELETE /api/v1/people/{id}` sets `is_active = false` instead of removing the row. Deactivated people remain in the database for referential integrity and audit.

**Consequences:**

- List endpoints support `is_active` filter to hide inactive people from default views.
- UI should show "Deactivate" rather than "Delete" for people.
- Reactivation is possible via `PATCH` with `is_active: true`.
- Hard delete may be reconsidered only with a formal archival model.

---

## ADR-0012: Keep primary team and primary capability on Person for MVP

**Status:** Accepted

**Context:** People may belong to multiple teams and capability areas in a full HR/allocation model. Many-to-many skills and time-based allocations are target scope but add schema and UI complexity.

**Decision:** Store one `team_id` and one `capability_id` on `Person` for MVP. Defer `Skill`, `Allocation` and many-to-many membership tables to a later phase.

**Consequences:**

- Simple foreign keys suffice for project, work item and catalog linking in MVP.
- Summary counts on teams and capabilities reflect primary membership only.
- Prompt 13 UI can use straightforward select dropdowns.
- Many-to-many skills/allocations will require migration and API versioning when added.

---

## ADR-0025: Use request IDs for API traceability

**Status:** Accepted

**Context:** Operators and developers need to correlate client errors with server logs without full distributed tracing infrastructure.

**Decision:** Add `RequestIdMiddleware` that accepts or generates `X-Request-ID`, returns it on responses, includes it in error JSON and request access logs.

**Consequences:**

- Clients can pass `X-Request-ID` for end-to-end correlation.
- No external observability vendor required for MVP debugging.
- Future workers and gateways can propagate the same header.

---

## ADR-0026: Keep background execution out of MVP readiness pass

**Status:** Accepted

**Context:** Automation schedules and triggers exist, but no worker process polls or executes them yet. Production readiness should harden what exists without scope creep.

**Decision:** Defer background worker implementation to Phase 27. Readiness pass focuses on API reliability, auth, errors, docs and CI — not job runners.

**Consequences:**

- `next_run_at` fields remain informational until a worker ships.
- Redis remains optional/unused in core paths.
- Automation manual run + simulation remain the supported execution model.

---

## ADR-0027: Keep JWT auth as MVP auth model before SSO

**Status:** Accepted

**Context:** Enterprise SSO and MFA are target capabilities but add significant integration and operations overhead.

**Decision:** Continue JWT bearer auth with bcrypt passwords and viewer/editor/admin roles for MVP. Document limitations; reject insecure production configuration via settings validation.

**Consequences:**

- Fast local/demo onboarding with seed users.
- `localStorage` token storage acceptable for MVP with HTTPS requirement in production guidance.
- SSO/MFA remain explicit future phases without blocking current delivery.

---

## ADR-0029: Use Company and Workspace as SaaS tenant hierarchy

**Status:** Accepted

**Context:** Internal Sea is a SaaS-style internal operating system, not a CRM. The correct root hierarchy is Company / Workspace / Team / Member, not Client / Account.

**Decision:** Introduce Company, Workspace and CompanyMember as first-class SaaS objects. Use `company_id` and `workspace_id` to scope major operational entities. Keep CRM-style Client/Account for future commercial modules only.

**Consequences:**

- Existing objects become tenant-scoped.
- First user creates a company and default workspace.
- Authorization will use company membership.
- Multi-company support becomes possible later.
- Account/CRM module is deferred.

---

## Template for new ADRs

```markdown
## ADR-XXXX: Title

**Status:** Proposed | Accepted | Superseded

**Context:** ...

**Decision:** ...

**Consequences:** ...
```
