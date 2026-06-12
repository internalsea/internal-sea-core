# People Feature

People directory UI connected to `/api/v1/people`.

## Routes

| Path | Purpose |
|------|---------|
| `/people` | List with search and filters |
| `/people/new` | Create person |
| `/people/:id` | Detail with summary cards |
| `/people/:id/edit` | Edit person |

## Notes

- DELETE deactivates the person (`is_active = false`) — see ADR-0011.
- PersonForm uses Teams and Capabilities dropdowns (first 100 items).
- Default list filter shows active people only.

## Known limitations

- No skills or allocations UI
- No performance metrics integration
- User ID field remains a UUID text input
