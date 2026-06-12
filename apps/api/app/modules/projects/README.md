# Projects API

First-class project management for client projects, internal projects, POCs, pilots, MVPs and initiatives.

Uses a single `projects` table with a `project_type` discriminator.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/projects` | List with filters and pagination |
| POST | `/api/v1/projects` | Create |
| GET | `/api/v1/projects/{id}` | Get by ID |
| GET | `/api/v1/projects/{id}/summary` | Work item counts summary |
| PATCH | `/api/v1/projects/{id}` | Partial update |
| DELETE | `/api/v1/projects/{id}` | Delete |

Internal projects use `/api/v1/internal-projects` — see `app/modules/internal_projects/`.

Work items can link via `project_id`.
