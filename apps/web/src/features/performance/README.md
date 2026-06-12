# Performance Feature

Manual performance metrics and entity scorecards.

## Routes

- `/performance` — overview, definitions and values
- `/performance/metrics/new` — create metric definition
- `/performance/metrics/:id` — definition detail
- `/performance/metrics/:id/edit` — edit definition
- `/performance/values/new` — create metric value
- `/performance/values/:id/edit` — edit metric value

## PerformanceSection

Embedded on detail pages:

- Data products
- Projects and internal projects
- People
- Teams
- Capabilities

## API

Uses `/performance/*` endpoints via `features/performance/api.ts`.
