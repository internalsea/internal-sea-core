# Design Guidelines

Visual and UX direction for Internal Sea. The UI is an operating system for data products, work, teams, capabilities, projects, compliance and performance. It should help users make decisions quickly — not impress them visually.

## Design goal

**Minimalistic, calm, structured, professional, enterprise-grade.**

The app should feel suitable for:

- Data catalog browsing
- Jira-like work management
- Team and capability management
- Compliance tracking
- Performance dashboards
- Leadership reporting

### What to avoid

- Bright startup gradients
- Neon colors
- Playful or consumer-app UI
- Unnecessary animations
- Overloaded cards with too many colors
- Heavy shadows
- Dark-only design (light theme only for now)
- Bold text everywhere
- Large typography except page titles
- Icon-only primary navigation without labels

## Color palette

Use restrained enterprise colors. Do not invent custom colors per feature.

### Primary

| Token | Hex | Usage |
|-------|-----|-------|
| Deep Navy | `#111827` | Sidebar, primary text |
| Primary Blue | `#2563EB` | Primary actions, active states, links |
| Primary Blue Hover | `#1D4ED8` | Button hover |
| Primary Blue Soft | `#EFF6FF` | Info backgrounds |

### Neutrals

| Token | Hex | Usage |
|-------|-----|-------|
| App Background | `#F9FAFB` | Page background |
| Surface | `#FFFFFF` | Cards, top bar, tables |
| Surface Muted | `#F3F4F6` | Ghost button hover, code blocks |
| Border | `#E5E7EB` | Default borders |
| Border Strong | `#D1D5DB` | Inputs, secondary buttons |

### Text

| Token | Hex | Usage |
|-------|-----|-------|
| Text Primary | `#111827` | Headings, body emphasis |
| Text Secondary | `#374151` | Body text |
| Text Muted | `#6B7280` | Descriptions, metadata |
| Text Disabled | `#9CA3AF` | Disabled inputs, placeholders |

### Enterprise accent

| Token | Hex | Usage |
|-------|-----|-------|
| Teal | `#0F766E` | In-progress, operational states |
| Teal Soft | `#F0FDFA` | Teal badge backgrounds |

### Status colors

| Status | Hex | Soft background |
|--------|-----|-----------------|
| Success | `#15803D` | `#F0FDF4` |
| Warning | `#B45309` | `#FFFBEB` |
| Danger | `#B91C1C` | `#FEF2F2` |
| Info | `#1D4ED8` | `#EFF6FF` |
| Neutral | `#4B5563` | `#F3F4F6` |

### Color rules

- **Navy** for sidebar and main text hierarchy.
- **Blue** only for primary actions and active/link states.
- **Teal** rarely — in-progress and operational states.
- **Red** only for destructive actions or critical states.
- **Yellow/orange** only for warnings.
- **Gray** for draft, archived, unknown, disabled and secondary UI.

Tokens are defined in `apps/web/src/lib/designTokens.ts` and mirrored in `apps/web/tailwind.config.ts`.

## Typography

System enterprise font stack (no external fonts loaded yet):

```
Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

### Scale

| Role | Classes |
|------|---------|
| Page title | `text-2xl font-semibold tracking-tight text-gray-900` |
| Page description | `text-sm text-gray-500` |
| Section title | `text-lg font-semibold text-gray-900` |
| Card title | `text-base font-semibold text-gray-900` |
| Body | `text-sm text-gray-700` |
| Small / metadata | `text-xs text-gray-500` |
| Table header | `text-xs font-medium uppercase tracking-wide text-gray-500` |
| Table cell | `text-sm text-gray-700` |
| Form label | `text-sm font-medium text-gray-700` |
| Form help text | `text-xs text-gray-500` |
| Form error | `text-xs text-red-700` |

Prefer readable density. Use `font-semibold` only for hierarchy. Use muted text for metadata.

## Layout

### App shell

| Element | Value |
|---------|-------|
| Sidebar width | 260px |
| Top bar height | 64px |
| Page padding | 24px (`p-6`) |
| Section spacing | 24px |
| Card padding | 20px (`p-5`) or 24px (`p-6`) |
| Max content width | None by default |
| Page background | App Background `#F9FAFB` |

### Sidebar

- Fixed left navigation
- Deep navy background `#111827`
- Product name at top with optional "Core" subtitle
- Grouped navigation: **Core**, **Organization**, **Governance**, **Operations**
- Active item: white text, subtle white overlay background
- Group labels: uppercase, `text-xs`, gray-500
- Hover: gray-800 background
- Scrollable nav uses the `sidebar-scroll` class — custom thin scrollbar with transparent track and muted slate thumb; never rely on default browser scrollbars on dark panels

### Top bar

- White background, bottom border
- Global search placeholder: "Search products, work, people..."
- API status: green dot (online), red dot (unavailable)
- User placeholder: Guest

### Cards

- White background
- Border `#E5E7EB`
- `rounded-xl` (`rounded-card`)
- Minimal or no shadow
- Optional header title

### Tables

- White container with border and `rounded-xl`
- Header background `#F9FAFB`
- Row hover `#F9FAFB`
- Row border `#E5E7EB`
- Compact but readable
- Actions aligned right

### Forms

- Simple vertical layout
- Labels above inputs
- Input height ~40px (`h-10`)
- Consistent spacing (`space-y-1.5` per field)
- Clear validation errors below field
- Advanced fields separated from main fields

## Components

Use shared components from `apps/web/src/components/ui/` before creating one-off styles.

### Button

Variants: `primary`, `secondary`, `ghost`, `danger`  
Sizes: `sm`, `md`, `lg`

| Variant | Style |
|---------|-------|
| Primary | Blue background, white text |
| Secondary | White background, gray border |
| Ghost | Transparent, gray text |
| Danger | Red background, white text |

### Badge

Variants: `neutral`, `info`, `success`, `warning`, `danger`, `teal`  
Small rounded-md labels — not pill-shaped.

### StatusBadge

Maps domain status strings to badge variants via design tokens. Never hardcode status colors in feature components.

### PageHeader

Title, optional description, optional actions on the right. Use at the top of every page.

### EmptyState / LoadingState / ErrorState

Use for list pages and async data. Empty states include a dashed border and centered copy.

## Status mapping

Use `apps/web/src/lib/designTokens.ts` for all status-to-color mappings.

### Data product status

| Status | Variant |
|--------|---------|
| draft | neutral |
| active | success |
| deprecated | warning |
| archived | neutral |

### Quality status

| Status | Variant |
|--------|---------|
| unknown | neutral |
| good | success |
| warning | warning |
| critical | danger |

### Work status

| Status | Variant |
|--------|---------|
| backlog | neutral |
| ready | info |
| in_progress | teal |
| review | warning |
| done | success |
| closed | neutral |

### Priority

| Priority | Variant |
|----------|---------|
| low | neutral |
| medium | info |
| high | warning |
| critical | danger |

### Project status

| Status | Variant |
|--------|---------|
| idea | neutral |
| planned | info |
| active | teal |
| on_hold | warning |
| completed | success |
| cancelled | danger |
| archived | neutral |

### Compliance status

| Status | Variant |
|--------|---------|
| not_started | neutral |
| in_progress | teal |
| compliant | success |
| non_compliant | danger |
| exception | warning |
| not_applicable | neutral |

### Policy status

| Status | Variant |
|--------|---------|
| draft | neutral |
| active | success |
| deprecated | warning |
| archived | neutral |

### Rule severity

| Severity | Variant |
|----------|---------|
| low | neutral |
| medium | info |
| high | warning |
| critical | danger |

### Evidence status

| Status | Variant |
|--------|---------|
| missing | danger |
| submitted | info |
| accepted | success |
| rejected | danger |
| expired | warning |

### Compliance overview page

1. `PageHeader` — title, New Policy and New Check actions
2. Overview metric cards — policies, rules, checks, overdue counts
3. Policies table — name, status, version, effective dates
4. Compliance checks table — title, subject, status, due date
5. Future governance placeholder — automation, approvals, schedules

### Policy detail layout

- Overview card with policy metadata and status badge
- Rules table nested under policy
- Related checks (when linked via rules)

### Compliance section on entity detail pages

- Summary stats: total, compliant, non-compliant, open
- Compact checks table with link to full check detail
- New Check action pre-fills subject via query params

### Login page

1. Centered card on soft blue-grey wave background — no sidebar or top bar
2. Use `AuthLayout` and `AuthCard` for consistent auth/public entry styling
3. Card surface uses cool off-white (`auth.surface`), not flat white, with subtle shadow
4. Product name and one-line description
5. Email and password fields, primary sign-in button
6. Inline error message on failed login
7. Demo credentials helper for local development only

Apply the same auth layout treatment to Register, First User Onboarding and Company Setup pages.

### Current user menu

- Top bar right: display name or email, role badge, logout button
- Compact inline layout — dropdown optional

### Permission-gated actions

- Hide create/edit/delete and attach/evidence actions for viewers
- Use `PermissionGate` or `useCanWrite()` — viewers should not see destructive controls
- Read-only detail pages remain fully accessible to viewers

## Page patterns

### Standard list page

1. `PageHeader` — title, description, primary action (e.g. Create)
2. Filter/search card — inputs, status filters
3. Table card — sortable columns, row actions
4. Pagination below table
5. `EmptyState` when no results

### Standard detail page

1. `PageHeader` — entity name, status badge, edit/delete actions
2. Overview card — key fields in a grid
3. Related sections — tabs or stacked cards
4. Comments section — plain-text textarea, list of comments, no avatars
5. Activity timeline — vertical list with action badges, title and timestamp

### Standard form page

1. `PageHeader` — create/edit title
2. Form card — labeled fields, validation errors
3. Primary submit + secondary cancel actions at bottom

### Work board page

1. `PageHeader` — title, description, list view and create actions
2. Filter card — search, type, priority (status filter optional; board groups by status)
3. Horizontal columns — one card per active status (Backlog → Done)
4. Column header — title and count badge
5. Work item cards — title, type/priority badges, due date, quick Open/Edit/Move actions
6. **No drag-and-drop in MVP** — status changes via explicit "Move to …" buttons
7. List and board must use the same status labels and badge variants

### Work item card pattern

- White surface, border, compact padding
- Title as link-style button
- Type and priority badges below title
- Metadata: due date (red if overdue), estimate points, linked data product ID
- Actions: Open, Edit, next-status transition button

### Comments section pattern

- White `Card` with `SectionHeader`
- Plain-text `textarea` (max 5000 chars) and primary submit button
- Simple list of comments — body, timestamp, author placeholder (`System` or short user id)
- No avatars, rich text, mentions or attachments in MVP
- Inline error on submit failure; do not clear text on failure

### Relationships section pattern

- White `Card` with outgoing/incoming groups
- Link type badge + entity type badge per row
- Add relationship form: `EntityPicker` for target entity search/select
- Link type select; optional collapsible **Use manual ID** for UUID fallback
- Related entities display via `EntityReference` (type badge + title + link)
- Remove action per link; no graph visualization in MVP

### Entity picker pattern

Use `EntityPicker` from `src/features/entity-picker/` for any form field that links to another entity.

- Selected value shows as a **pill** with type badge, title and clear action
- Search input debounces (300ms); dropdown max height ~320px
- Result rows: type badge, title, description, status metadata when available
- Placeholder text adapts to allowed types (e.g. "Search people…")

Use `EntityReference` on detail pages and lists to show readable names instead of raw UUIDs.

**Manual ID fallback:** Keep collapsible advanced sections for edge cases (unsupported types, bulk paste, debugging). Do not show raw UUIDs in normal UI unless in advanced/debug context.

### Activity timeline pattern

- White `Card` with vertical timeline
- Each item: action badge, title, optional description, timestamp, actor placeholder
- Read-only — no user edits
- Small error card if the feed fails; must not break the rest of the detail page

### Priority and status badges

Use feature badge components (`WorkItemStatusBadge`, `WorkItemPriorityBadge`, `WorkItemTypeBadge`) backed by design tokens — never hardcode colors in board or table cells.

### Project list pattern

1. `PageHeader` — title, description, "New Project" / "New Internal Project" action
2. Filter card — search, status, health; type and client filters for all-projects view only
3. `ProjectTable` — name with description subtitle, status/health badges, timeline column, row actions
4. Pagination — previous/next with total count
5. `EmptyState` when no results

Internal projects reuse the same table and filters with `variant="internal-projects"` — type and client columns hidden.

### Project detail page pattern

1. `PageHeader` — project name, description, Edit and Back actions
2. `ProjectSummaryCards` — compact four-card row: Total Work, Open, Completed, Overdue
3. Overview card — type, status, health, priority, client (projects only)
4. Timeline, ownership, budget and delivery notes cards
5. Placeholder sections for work items, data products, compliance, performance, meetings, files and activity

### Summary card style

- Four equal-width cards in a responsive grid (`sm:grid-cols-2 lg:grid-cols-4`)
- Uppercase muted label (`text-xs`), large count (`text-2xl font-semibold`)
- Use standard `Card` component — no custom colors per metric
- Overdue count uses the same neutral card style; danger color reserved for inline overdue indicators

### Health badge style

Use `ProjectHealthBadge` backed by `projectHealthVariantMap`:

| Health | Variant |
|--------|---------|
| unknown | neutral |
| healthy | success |
| warning | warning |
| critical | danger |

### Organization list pattern

1. `PageHeader` — title, description, primary create action
2. Filter card — search; people also filter by seniority, status, location, team and capability
3. Table — name with metadata subtitle, badges for status/seniority, relationship columns
4. Pagination — previous/next with total count
5. `EmptyState` when no results

People default to **active** filter. Deactivated people use "Deactivate" (not "Delete") with confirmation explaining historical links are preserved.

### Organization summary cards

- **Person:** Assigned Work, Business Products, Technical Products, Owned Projects (4 cards)
- **Team / Capability:** People, Active People, Data Products, Open Work, Projects, Internal Projects (6 cards)
- Same compact card style as project summary — uppercase muted label, large count
- No per-metric color coding

### Deactivate vs delete UX

| Entity | Action | Label | Notes |
|--------|--------|-------|-------|
| Person | Soft deactivate | "Deactivate" | Preserves work/project/catalog links |
| Team | Hard delete | "Delete" | Blocked with error if referenced |
| Capability | Hard delete | "Delete" | Blocked with error if referenced |

Use `EntityPicker` for team/capability on person forms. `user_id` remains in advanced section.

## Dashboard layout pattern

The home dashboard (`/dashboard`) is the primary operating overview. Keep it **list- and card-first** — no chart library in MVP.

### Structure

1. `PageHeader` — title and short operating description
2. **Summary metric grid** — 8 `MetricCard` tiles linking to relevant modules
3. **Two-column section grid** (`xl:grid-cols-2`) — responsive stacks to one column on smaller screens
4. Each section uses `DashboardSection` — title, optional action link, compact table or list body

### Metric card style

- White surface, subtle border, optional soft tint for warning/danger variants
- Uppercase muted label (`text-xs`), large count (`text-2xl font-semibold`)
- Optional `href` to navigate to the related module list
- Variant logic driven by data (e.g. overdue work, critical quality) — not decorative color

### Compact section card style

- Reuse `Card` with `padding="lg"`
- Section header row: title left, "View all" / module links right
- Tables: `text-sm`, uppercase muted column headers, `divide-y` row separators
- Inline section errors — do not block the full page when one query fails

### Advanced executive dashboard layout

1. `PageHeader` — title and executive/operational description
2. **Executive summary row** — overall score, active projects, data products, open/overdue work, compliance and ownership gap counts (`ExecutiveSummaryCards`)
3. **Operational health panel** — domain health scores with `MiniProgressBar` and `HealthScoreBadge`
4. **Two-column grid** — actionable insights wide/high priority; module insight cards (work, projects, data products, compliance, performance, automation, notifications, activity)

### Health score pattern

- Scores 0–100 map to `good` (≥85), `warning` (70–84), `critical` (&lt;70), `unknown` (no data)
- Use `HealthScoreBadge` for status labels and `MiniProgressBar` for compact score display
- Do not use chart libraries for MVP health visualization

### Actionable insight pattern

- List rows: `InsightSeverityBadge`, category label, title, description, recommended action
- Link to source entity when `url` is provided
- Empty state: "No critical insights found." — balanced demo should show a few warnings, not only critical items

### Mini progress bar pattern

- Simple horizontal bar, optional label, variant from score thresholds
- No animation required; no chart library

### Dashboard MVP constraints

- **No chart-heavy design** — tables, lists, metric cards and mini bars first
- **No decorative gradients or heavy shadows**
- Compact operational cards with inline loading/error/empty states per section
- Status communicated via `Badge` / `StatusBadge` / `HealthScoreBadge` and numeric columns

## Global search dropdown pattern

Global search lives in the **top bar** (`GlobalSearch` component).

### Behavior

- Placeholder: `Search products, work, people...`
- Minimum query length: **2 characters** before API call
- Debounce: ~280ms
- Dropdown opens on input focus when query is non-empty
- Closes on Escape, outside click, or result selection
- Enter selects first result (optional MVP shortcut)

### Dropdown style

- White surface, `rounded-xl`, subtle border and light shadow
- Max height ~420px with scroll
- Width aligned to search input (~`max-w-xl`)
- Footer: `Showing {count} results`

### Result item pattern

Each row shows:

1. **Type badge** (`SearchResultTypeBadge`) — mapped labels and variants per entity
2. **Title** — primary match text
3. **Meta line** — description, status and secondary status joined with `·`
4. Optional updated date in muted `text-xs`

### Type badge mapping

| Type | Label | Variant |
|------|-------|---------|
| `data_product` | Data Product | info |
| `work_item` | Work Item | teal |
| `project` | Project | warning |
| `internal_project` | Internal Project | teal |
| `person` | Person | neutral |
| `team` | Team | neutral |
| `capability` | Capability | info |

### MVP constraints

- No command-palette library
- No icons required
- Inline loading, error and empty states inside dropdown
- Search failure must not break the top bar layout

## Files section pattern

Use `FilesSection` on entity detail pages for attached documents and evidence.

### Layout

- `Card` + `SectionHeader` with title (default "Files and Evidence" on projects)
- List of attached files with type, sensitivity and evidence badges
- "Attach file" toggles inline form with `EntityPicker` (`allowedTypes: ['file']`); manual file ID in advanced mode
- Loading, error and empty states inside the card

### Evidence badge pattern

When `is_evidence` is true on an attachment:

- Show teal **Evidence** badge next to file name
- Show `evidence_type` as muted secondary text when present

### File metadata page pattern

Global file browser at `/files`:

- Filters: search, type, status, sensitivity, evidence
- Table columns: name, type, status, sensitivity, version, owner, updated
- Detail page sections: Overview, Location, Ownership, Technical metadata, Attachments

### External links

- Open external document URLs in a **new tab** with `rel="noopener noreferrer"`
- Use primary blue link styling — not raw URL strings in body text

## Automation UI patterns

### Automation overview

- Summary cards for active schedules/triggers, failed runs and upcoming runs
- Tables for triggers, schedules and recent runs on `/automation`
- Future capabilities listed as a muted placeholder card (worker, notifications, AI, webhooks)

### Trigger detail

- Overview card with status, action, schedule and target (`EntityReference`)
- JSON blocks for `conditions` and `action_config` (monospace, scrollable)
- Run history table with status and action badges
- Manual run: simulation default; real run requires editor confirmation dialog

### Run history table

- Columns: status, action type, target, started, finished, result summary
- Use `AutomationRunStatusBadge` and `AutomationActionTypeBadge`

### JSON config editor (MVP)

- Textarea with monospace font; validate JSON on submit
- Show action-specific example snippets when action type changes
- Empty JSON fields submit as `null`

### Simulation vs real run

- Simulation: secondary button, no destructive styling
- Real run: primary button with confirmation — explain possible side effects (work item, comment, activity)

### Entity automation section

- Embeddable `AutomationSection` on detail pages
- Lists triggers for the entity; link to trigger detail; editor action to create trigger with pre-filled target

### Performance scorecard section

- Embeddable `PerformanceSection` on entity detail pages
- Summary cards: average score, health status, metrics count, last updated
- Compact metric list: current value, target, score, trend badge, interpretation
- No chart library in MVP — use tables and badges only

### Metric value table pattern

- Columns: metric, subject, value, status, period, source, updated, actions
- Use `EntityReference` for subject display where possible

### Trend badge pattern

- `up` → success, `down` → warning, `stable` / `unknown` → neutral
- Pair with interpretation text; do not rely on color alone

## Notifications UI

- Use notification status badges: draft (neutral), simulated (teal), sent (success), failed (danger)
- Message detail: overview metadata, body, delivery attempts table, simulation send dialog
- Send dialog defaults to simulate mode with clear warning when real send is selected
- Template detail: subject/body preview and optional JSON context render test panel

## Accessibility

- Keyboard navigable sidebar and forms
- Visible focus rings on interactive elements (`ring-core-blue`)
- Semantic headings on each page
- Status badges use text plus color — never color alone
- WCAG AA contrast target for core flows

## Reference

Implementation: `apps/web/`  
Design tokens: `apps/web/src/lib/designTokens.ts`  
Tailwind theme: `apps/web/tailwind.config.ts`

Align new screens with these patterns before introducing one-off layouts.
