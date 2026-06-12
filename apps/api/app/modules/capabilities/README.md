# Capabilities Module

CRUD API for skill and service capability areas.

**Status:** Implemented

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/capabilities` | List with search |
| POST | `/api/v1/capabilities` | Create |
| GET | `/api/v1/capabilities/{id}` | Get by ID |
| GET | `/api/v1/capabilities/{id}/summary` | People, work, catalog and project counts |
| PATCH | `/api/v1/capabilities/{id}` | Update |
| DELETE | `/api/v1/capabilities/{id}` | Delete (409 if referenced) |

## Notes

- Does not cascade delete referenced people, data products, work items or projects.
