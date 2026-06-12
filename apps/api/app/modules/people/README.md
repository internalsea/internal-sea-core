# People Module

CRUD API for team members and planned resources.

**Status:** Implemented

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/people` | List with filters |
| POST | `/api/v1/people` | Create |
| GET | `/api/v1/people/{id}` | Get by ID |
| GET | `/api/v1/people/{id}/summary` | Relationship counts |
| PATCH | `/api/v1/people/{id}` | Update |
| DELETE | `/api/v1/people/{id}` | Deactivate (`is_active = false`) |

## Notes

- DELETE is a soft deactivate — see ADR-0011.
- Duplicate emails return 409 Conflict.
