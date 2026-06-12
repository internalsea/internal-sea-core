# Capabilities Feature

Capabilities management UI connected to `/api/v1/capabilities`.

## Routes

| Path | Purpose |
|------|---------|
| `/capabilities` | List with search |
| `/capabilities/new` | Create capability |
| `/capabilities/:id` | Detail with summary cards |
| `/capabilities/:id/edit` | Edit capability |

## Notes

- Delete returns 409 if capability is referenced by people, work items, projects or data products.
