# Dashboard Feature

Operating overview for Internal Sea — summary metrics and compact section cards.

## API

| Function | Endpoint |
|----------|----------|
| `getDashboardSummary()` | `/dashboard/summary` |
| `getRecentDataProducts()` | `/dashboard/recent-data-products` |
| `getHighPriorityWorkItems()` | `/dashboard/high-priority-work-items` |
| `getProjectHealth()` | `/dashboard/project-health` |
| `getCapabilityWorkload()` | `/dashboard/capability-workload` |
| `getOwnershipGaps()` | `/dashboard/ownership-gaps` |

## Hooks

Each section uses a separate TanStack Query hook so one failing section does not block the rest.

## Route

`/dashboard` — home page (root redirects here).

## Design

- Metric cards at top with links to relevant modules
- Two-column responsive grid for section cards
- Tables and lists only — no chart library in MVP
