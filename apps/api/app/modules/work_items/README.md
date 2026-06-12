# Work Items Module

Manages delivery work items, status, assignment, and links to data products.

**Target entities:** WorkItem, Comment

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/work-items` | Paginated list with filters |
| GET | `/api/v1/work-items/board` | Board columns grouped by status |
| POST | `/api/v1/work-items` | Create work item |
| GET | `/api/v1/work-items/{id}` | Get by ID |
| PATCH | `/api/v1/work-items/{id}` | Update work item |
| DELETE | `/api/v1/work-items/{id}` | Delete work item |

Board columns include: Backlog, Ready, In Progress, Review, Done (excludes Closed by default).

Frontend UI lives in `apps/web/src/features/work-items/`.
