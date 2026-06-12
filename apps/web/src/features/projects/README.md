# Projects Feature

Client and internal project management UI connected to `/api/v1/projects` and `/api/v1/internal-projects`.

## Structure

```
api.ts          # HTTP functions for projects and internal projects
hooks.ts        # TanStack Query keys, queries and mutations
types.ts        # Types matching backend schemas
constants.ts    # Labels, filter options and select styling
utils.ts        # Formatting, payload cleaning and form helpers
components/     # Shared UI with variant prop for internal projects
```

## Routes

| Path | Purpose |
|------|---------|
| `/projects` | All projects list |
| `/projects/new` | Create project |
| `/projects/:id` | Project detail with summary cards |
| `/projects/:id/edit` | Edit project |
| `/internal-projects` | Internal projects list |
| `/internal-projects/new` | Create internal project |
| `/internal-projects/:id` | Internal project detail |
| `/internal-projects/:id/edit` | Edit internal project |

## Variant pattern

Internal projects reuse the same components with `variant="internal-projects"`:

- Hides type and client columns in list view
- Forces `project_type=internal_project` on create/update
- Uses internal project API endpoints

## Known limitations

- No timeline/Gantt view
- No compliance or performance integration
- Owner, team and capability fields are ID-based until People/Teams/Capabilities UI ships
- Work item project linking in UI pending (backend supports `project_id`)
