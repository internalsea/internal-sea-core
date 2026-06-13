# Internal Sea Web

React frontend for Internal Sea — internal operating system UI.

**Local testing:** See [docs/LOCAL_TEST_AND_READINESS_REVIEW.md](../../docs/LOCAL_TEST_AND_READINESS_REVIEW.md).

## Purpose

Provides the app shell, navigation, design system and feature UIs for catalog and work management.

## Stack

- React 18 + TypeScript
- Vite 6
- React Router 6
- TanStack Query 5
- Tailwind CSS 3
- pnpm

## Structure

```
src/
├── app/              # App, router, providers
├── components/       # layout/, ui/, common/
├── features/         # Domain API + types (+ UI later)
├── lib/              # apiClient, config, navigation, designTokens, utils
├── pages/            # Route pages
└── types/            # Shared types and enums
```

## Commands

From repository root:

```bash
make web-install
make web-dev
make web-check
```

From this directory:

```bash
pnpm install
pnpm dev
pnpm check
```

## Environment variables

Copy `.env.example` to `.env`:

| Variable | Default |
|----------|---------|
| `VITE_APP_NAME` | Internal Sea |
| `VITE_API_BASE_URL` | http://localhost:8000/api/v1 |

**Important:** The browser must use `localhost` for the API URL, not Docker service hostnames.

## Design system overview

Internal Sea uses a **minimalistic, enterprise-grade** light theme. The UI prioritizes readability and decision-making over visual flair.

Full visual spec: [docs/DESIGN_GUIDELINES.md](../../docs/DESIGN_GUIDELINES.md)

### Design tokens

Location: `src/lib/designTokens.ts`

Exports:

- `colors` — semantic color values
- `badgeVariantClasses` — Tailwind classes per badge variant
- `statusVariantMap`, `qualityVariantMap`, `workStatusVariantMap`, `priorityVariantMap`, `projectStatusVariantMap`, `complianceStatusVariantMap`
- `resolveStatusVariant()` — lookup helper for `StatusBadge`

Tailwind theme extensions live in `tailwind.config.ts` (`core-*`, `app-*`, `status-*`).

### Using components

**Button** — primary actions, secondary/cancel, ghost toolbar actions, danger delete.

```tsx
import { Button } from '@/components/ui/Button'

<Button variant="primary">Save</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="danger" size="sm">Delete</Button>
```

**Card** — content containers with optional title.

```tsx
import { Card } from '@/components/ui/Card'

<Card title="Filters">…</Card>
```

**Badge** — static labels with explicit variant.

```tsx
import { Badge } from '@/components/ui/Badge'

<Badge variant="info">Local</Badge>
```

**StatusBadge** — domain status strings mapped via design tokens.

```tsx
import { StatusBadge } from '@/components/ui/StatusBadge'

<StatusBadge status="in_progress" />
<StatusBadge status="active" />
```

**PageHeader** — every page starts with title, description and optional actions.

```tsx
import { PageHeader } from '@/components/ui/PageHeader'
import { Button } from '@/components/ui/Button'

<PageHeader
  title="Data Products"
  description="Catalog of dashboards, datasets and metrics."
  actions={<Button>Create product</Button>}
/>
```

### Styling rules for new feature pages

1. Use `PageHeader` at the top of every page.
2. Wrap content in `Card` — white surface, border, `rounded-card`.
3. Use `StatusBadge` for status columns — never hardcode status colors.
4. Use semantic Tailwind colors (`core-blue`, `app-border`, `status-success`, etc.).
5. List pages: header → filter card → table card → pagination/empty state.
6. Form pages: header → form card → primary/secondary actions.
7. Keep typography at `text-sm` for body; use muted gray for metadata.
8. No animations, gradients or heavy shadows.

## Routes

| Path | Page |
|------|------|
| `/dashboard` | Executive and operational dashboard — summary, health scores, actionable insights, work/project/catalog/compliance/performance/automation/notification cards, recent activity |
| `/data-products` | Data Products (placeholder list) |
| `/data-products/:id` | Data product detail (comments and activity) |
| `/work-items` | Work Items list |
| `/work-items/new` | Create work item |
| `/work-items/:id` | Work item detail |
| `/work-items/:id/edit` | Edit work item |
| `/work-board` | Work board by status |
| `/projects` | Projects list |
| `/projects/new` | Create project |
| `/projects/:id` | Project detail |
| `/projects/:id/edit` | Edit project |
| `/internal-projects` | Internal projects list |
| `/internal-projects/new` | Create internal project |
| `/internal-projects/:id` | Internal project detail |
| `/internal-projects/:id/edit` | Edit internal project |
| `/people` | People list |
| `/people/new` | Create person |
| `/people/:id` | Person detail |
| `/people/:id/edit` | Edit person |
| `/teams` | Teams list |
| `/teams/new` | Create team |
| `/teams/:id` | Team detail |
| `/teams/:id/edit` | Edit team |
| `/capabilities` | Capabilities list |
| `/capabilities/new` | Create capability |
| `/capabilities/:id` | Capability detail |
| `/capabilities/:id/edit` | Edit capability |
| `/notifications` | Notifications overview (channels, templates, messages) |
| `/notifications/templates/new` | Create notification template |
| `/notifications/templates/:id` | Template detail and render preview |
| `/notifications/templates/:id/edit` | Edit template |
| `/notifications/messages/new` | Create notification message |
| `/notifications/messages/:id` | Message detail and simulated send |
| `/notifications/messages/:id/edit` | Edit message |
| `/performance` | Performance overview |
| `/performance/metrics/new` | Create metric definition |
| `/performance/metrics/:id` | Metric definition detail |
| `/performance/metrics/:id/edit` | Edit metric definition |
| `/performance/values/new` | Create metric value |
| `/performance/values/:id/edit` | Edit metric value |
| `/compliance` | Compliance overview |
| `/compliance/policies/new` | Create policy |
| `/compliance/policies/:id` | Policy detail |
| `/compliance/policies/:id/edit` | Edit policy |
| `/compliance/checks/new` | Create compliance check |
| `/compliance/checks/:id` | Check detail with evidence |
| `/compliance/checks/:id/edit` | Edit check |
| `/policies` | Policies (legacy placeholder) |
| `/automation` | Automation overview — schedules, triggers, runs |
| `/automation/triggers/new` | Create automation trigger |
| `/automation/triggers/:id` | Trigger detail and run history |
| `/automation/triggers/:id/edit` | Edit trigger |
| `/automation/schedules/new` | Create schedule |
| `/automation/schedules/:id/edit` | Edit schedule |
| `/tools` | Tools |
| `/meetings` | Meetings |
| `/deals` | Deals |
| `/files` | Files |
| `/settings` | Settings |

## Comments feature

See `src/features/comments/README.md`.

Enabled on data product, work item, project and internal project detail pages.

## Activity feature

See `src/features/activity/README.md`.

Read-only timeline on the same detail pages.

## Relationships feature

See `src/features/relationships/README.md`.

Enabled on data product, work item, project, internal project, person, team and capability detail pages. Users paste target UUIDs until entity picker ships.

## Files feature

See `src/features/files/README.md`.

| Route | Page |
|-------|------|
| `/files` | File browser with filters |
| `/files/new` | Create file metadata |
| `/files/:id` | File detail |
| `/files/:id/edit` | Edit file metadata |

`FilesSection` is embedded on:

- Data product detail (`entityType="data_product"`)
- Work item detail (`entityType="work_item"`)
- Project detail (`entityType="project"`)
- Internal project detail (`entityType="internal_project"`)

**Known limitations:**

- No binary upload or file picker — attach by pasting file UUID
- No file preview
- Owner fields show raw UUIDs

## Performance feature

See `src/features/performance/README.md`.

### Notifications UI

- Simulation-first send dialog; external providers not implemented in MVP
- `NotificationsSection` on entity detail pages

See `src/features/notifications/README.md`.

`PerformanceSection` is embedded on:

- Data product detail (`subjectType="data_product"`)
- Project detail (`subjectType="project"`)
- Internal project detail (`subjectType="internal_project"`)
- Person detail (`subjectType="person"`)
- Team detail (`subjectType="team"`)
- Capability detail (`subjectType="capability"`)

**Known limitations:**

- No chart library or time-series visualizations
- Metric values are manual — no automatic calculation
- Global search does not index metric definitions yet

## Work Items feature

See `src/features/work-items/README.md`.

**Known limitation:** No drag-and-drop on the board yet — status changes use explicit buttons.

## Projects feature

See `src/features/projects/README.md`.

**Known limitations:**

- No timeline/Gantt view
- Work item project linking in forms pending (backend supports `project_id`)

## Organization feature

See `src/features/people/README.md`, `src/features/teams/README.md` and `src/features/capabilities/README.md`.

**Known limitations:**

- No skills or allocations UI
- User ID and some relationship fields still show raw UUIDs on detail pages
- Team/capability dropdowns load first 100 items only

## Environment variables

Copy `apps/web/.env.example` to `apps/web/.env` (or set in root `.env` for Docker Compose):

| Variable | Purpose |
|----------|---------|
| `VITE_API_BASE_URL` | API base URL (default `http://localhost:8000/api/v1`) |
| `VITE_APP_NAME` | Application title |

`VITE_*` variables are embedded at **build time**. Set `VITE_API_BASE_URL` before `pnpm build` for production.

## Auth flow

1. `AuthProvider` reads token from `localStorage` on load.
2. `GET /auth/me` validates session.
3. `ProtectedRoute` redirects unauthenticated users to `/login`.
4. `apiClient` attaches `Authorization: Bearer` header.
5. On 401, session clears and user redirects to `/login`.

## API client

All features use `src/lib/apiClient.ts`:

- Typed `ApiError` with `status`, `message`, `requestId`
- Parses standard `error` / `message` and legacy `detail` fields
- Network failures surface as user-friendly errors

## Protected routes

All routes under `AppLayout` require authentication except `/login`.

## Docker

```bash
make docker-up   # starts web on http://localhost:5173
```

## Global search

See `src/features/search/README.md`.

- Top bar `GlobalSearch` component with debounced dropdown
- Supported types: data products, work items, projects, internal projects, people, teams, capabilities
- Works best after `make seed`

**Known limitations:**

- Simple `ilike` matching only — no fuzzy ranking beyond basic title priority
- No dedicated `/search` results page yet
- Data product results link to `/data-products/{id}` (detail route pending)

## Dashboard feature

See `src/features/dashboard/README.md`.

Sections load via separate TanStack Query hooks for resilience — one failed section does not break the page. Run `make seed` for meaningful demo data on `/dashboard`.

**Advanced sections:** executive summary, operational health, actionable insights, work delivery, project insights, data product health, compliance, performance, automation, notifications, recent activity.

**Known limitations:**

- No heavy chart library — metric cards, mini progress bars, tables and lists only
- Health scores are simple heuristics, not AI or official compliance KPIs
- `/dashboard/advanced` API exists but the UI loads section endpoints independently

## Auth feature

See `src/features/auth/README.md`.

| Route | Page |
|-------|------|
| `/login` | Sign in (public) |
| All other routes | Protected — requires valid JWT |

- `AuthProvider` loads token from `localStorage` and calls `/auth/me`
- `apiClient` sends `Authorization: Bearer` header
- `PermissionGate` / `useCanWrite()` hide write actions for viewers
- Top bar shows current user and logout

**Demo credentials:** admin@example.com / admin12345, editor@example.com / editor12345, viewer@example.com / viewer12345

## Tenancy feature

See `src/features/tenancy/README.md`.

| Route | Page |
|-------|------|
| `/onboarding/first-user` | First user setup (public, empty system) |
| `/settings` | User, workspace, and company settings (header gear icon) |
| `/settings/company` | Redirects to `/settings?section=company` |
| `/settings/workspace` | Redirects to `/settings?section=workspace` |

- `TenancyProvider` loads `/tenancy/current` after auth
- `apiClient` sends `X-Company-ID` and `X-Workspace-ID` from localStorage
- Top bar shows current company and workspace via `CurrentCompanyBadge`
- Demo seed: **Internal Sea Demo** / **Default Workspace**

## Compliance feature

See `src/features/compliance/README.md`.

`ComplianceSection` is embedded on:

- Data product detail (`subjectType="data_product"`)
- Project detail (`subjectType="project"`)
- Internal project detail (`subjectType="internal_project"`)
- Team detail (`subjectType="team"`)
- Capability detail (`subjectType="capability"`)

**Known limitations:**

- Rule/control pickers not yet implemented — paste UUIDs in advanced mode
- No automated checks or approval workflows

## Automation feature

See `src/features/automation/README.md`.

`AutomationSection` is embedded on:

- Data product detail (`targetType="data_product"`)
- Work item detail (`targetType="work_item"`)
- Project detail (`targetType="project"`)
- Internal project detail (`targetType="internal_project"`)
- Team detail (`targetType="team"`)
- Capability detail (`targetType="capability"`)
- Compliance check detail (`targetType="compliance_check"`)

**Worker status UI** on `/automation`:

- `WorkerStatusCard`, `DueWorkCard`, `RunWorkerOnceButton` (editor)
- See `src/features/worker/README.md`

**Known limitations:**

- No complex cron parsing; custom schedules keep manual `next_run_at`
- Real runs limited to safe actions (work item, comment, activity event, notification queue)
- External notification delivery not implemented

## Entity picker feature

See `src/features/entity-picker/README.md`.

`EntityPicker` and `EntityReference` are used in:

- Relationship form (target entity search)
- File attachment form (file search)
- Compliance check form (subject and owner)
- Compliance evidence form (file search)
- Work item, project, person and data product forms (ownership and link fields)
- Detail pages (readable entity names instead of raw UUIDs)

Manual UUID entry remains available in **advanced mode** on relationship, file and compliance forms where needed.

## Next step

**Prompt 23:** Automation triggers and schedules foundation.

See [docs/IMPLEMENTATION_ROADMAP.md](../../docs/IMPLEMENTATION_ROADMAP.md).
