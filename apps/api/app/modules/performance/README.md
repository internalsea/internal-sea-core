# Performance Module

Manual performance metrics and entity scorecards for Internal Sea.

## Scope

- Metric definitions (what to measure)
- Metric values (recorded values per entity and period)
- Entity scorecards (calculated read model)
- Overview aggregates

## API

Base path: `/api/v1/performance`

- `GET /overview` — summary counts
- `GET|POST /metrics` — metric definitions
- `GET|PATCH|DELETE /metrics/{id}` — definition detail
- `GET|POST /values` — metric values
- `GET|PATCH|DELETE /values/{id}` — value detail
- `GET /entity/{subject_type}/{subject_id}/scorecard` — entity scorecard
- `GET /entity/{subject_type}/{subject_id}/values` — values for entity

## Auth

- GET: viewer
- POST/PATCH/DELETE: editor

## Notes

- Values are manual in MVP; no automatic calculation engine.
- `subject_type` / `subject_id` are validated in the service layer.
- Project-scoped definitions also apply to internal projects for scorecards.
