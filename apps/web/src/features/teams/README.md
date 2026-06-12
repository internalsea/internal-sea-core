# Teams Feature

Teams management UI connected to `/api/v1/teams`.

## Routes

| Path | Purpose |
|------|---------|
| `/teams` | List with search |
| `/teams/new` | Create team |
| `/teams/:id` | Detail with summary cards |
| `/teams/:id/edit` | Edit team |

## Notes

- Delete returns 409 if team is referenced by people, work items, projects or data products.
