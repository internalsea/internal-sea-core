# Work Items Feature

Jira-like work management UI connected to `/api/v1/work-items`.

## Routes

| Path | Purpose |
|------|---------|
| `/work-items` | List with search, filters and pagination |
| `/work-items/new` | Create form |
| `/work-items/:id` | Detail page |
| `/work-items/:id/edit` | Edit form |
| `/work-board` | Status board with quick status transitions |

## Structure

- `api.ts` — HTTP functions
- `hooks.ts` — TanStack Query keys and hooks
- `types.ts` — TypeScript types matching backend schemas
- `constants.ts` — Labels and filter options
- `utils.ts` — Formatting, payload cleaning, status transitions
- `components/` — Table, filters, form, board, badges

## Known limitations

- No drag-and-drop on the board
- No comments, activity feed or related work yet
- Owner/team/capability/data product links are UUID text fields only
- No auth — all actions available to Guest

## API

- `GET /work-items` — paginated list
- `GET /work-items/board` — columns grouped by status
- `GET/POST/PATCH/DELETE /work-items/{id}` — CRUD

Status updates from the board use `PATCH /work-items/{id}` with `{ status }`.
