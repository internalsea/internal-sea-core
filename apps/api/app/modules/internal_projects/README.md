# Internal Projects API

Filtered API view over the shared `projects` table where `project_type = internal_project`.

Reuses `ProjectService`, schemas and repository from `app/modules/projects/`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/internal-projects` | List internal projects |
| POST | `/api/v1/internal-projects` | Create (forces `internal_project` type) |
| GET | `/api/v1/internal-projects/{id}` | Get if internal project |
| PATCH | `/api/v1/internal-projects/{id}` | Update if internal project |
| DELETE | `/api/v1/internal-projects/{id}` | Delete if internal project |

Non-internal projects return 404 on single-resource routes.
