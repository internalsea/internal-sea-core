# Dashboard Module

Read-only aggregates for the Internal Sea home dashboard.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/dashboard/summary` | Counts across catalog, work, projects and organization |
| GET | `/api/v1/dashboard/recent-data-products` | Latest updated data products |
| GET | `/api/v1/dashboard/high-priority-work-items` | High/critical open work items |
| GET | `/api/v1/dashboard/project-health` | Active and at-risk projects with work counts |
| GET | `/api/v1/dashboard/capability-workload` | Per-capability people, work and delivery load |
| GET | `/api/v1/dashboard/ownership-gaps` | Missing owners, teams and assignees |

## Design

- **Read-only** — no mutations
- **Cross-module queries** — repository reads from existing SQLAlchemy models
- **No business logic ownership** — other modules remain source of truth for CRUD
- **Ownership gaps** — severity rules in `gaps.py`

## Auth

Not implemented yet. Endpoints are open in local development.
