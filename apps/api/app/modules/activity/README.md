# Activity Module

Read-only activity timeline for Internal Sea entities.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/activity` | List activity with optional filters |
| GET | `/api/v1/activity/{entity_type}/{entity_id}` | List activity for a specific entity |

Activity events are created by domain services (create/update/delete/comment/status changes). No public mutation endpoints in MVP.
