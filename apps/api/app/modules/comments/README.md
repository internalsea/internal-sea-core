# Comments Module

Plain-text comments on data products, work items, projects and internal projects.

## Endpoints

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

Adding a comment also records a `commented` activity event.
