# Global Search Feature

Top-bar search across catalog, work, projects and organization entities.

## API

`GET /search?q=...` via `searchGlobal()` in `api.ts`.

## Components

| Component | Purpose |
|-----------|---------|
| `GlobalSearch` | Top bar input with debounced query |
| `SearchResultsDropdown` | Result panel with loading/error/empty states |
| `SearchResultItem` | Single clickable result row |
| `SearchResultTypeBadge` | Entity type label |
| `SearchEmptyState` | Hint and empty messages |

## Behavior

- Minimum query length: 2 characters
- Debounce: 280ms (`useDebouncedValue` in `lib/hooks.ts`)
- TanStack Query `staleTime`: 30 seconds
- Click result navigates to backend-provided `url`
- Enter opens first result

## Supported types

`data_product`, `work_item`, `project`, `internal_project`, `person`, `team`, `capability`
