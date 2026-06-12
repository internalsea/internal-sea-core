# Teams Module

CRUD API for delivery teams.

**Status:** Implemented

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/teams` | List with search |
| POST | `/api/v1/teams` | Create |
| GET | `/api/v1/teams/{id}` | Get by ID |
| GET | `/api/v1/teams/{id}/summary` | People, work, catalog and project counts |
| PATCH | `/api/v1/teams/{id}` | Update |
| DELETE | `/api/v1/teams/{id}` | Delete (409 if referenced) |

## Notes

- Does not cascade delete referenced people, data products, work items or projects.
