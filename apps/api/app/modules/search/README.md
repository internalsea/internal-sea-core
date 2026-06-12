# Search Module

Unified global search across catalog, work, projects, organization, files and compliance entities.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/search` | Search across supported entity types |
| GET | `/api/v1/search/entity/{entity_type}/{entity_id}` | Lookup single entity for display labels |

### Query parameters (`/search`)

| Param | Description |
|-------|-------------|
| `q` | Search text (min 2 characters, trimmed) |
| `types` | Optional repeated filter: `data_product`, `work_item`, `project`, `internal_project`, `person`, `team`, `capability`, `file`, `policy`, `compliance_check` |
| `limit` | Max results (default 20, max 50) |

### Examples

```bash
curl "http://localhost:8000/api/v1/search?q=sales"
curl "http://localhost:8000/api/v1/search?q=governance&types=policy"
curl "http://localhost:8000/api/v1/search?q=nikita&types=person&limit=10"
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/search/entity/person/{id}"
```

## Implementation

- **PostgreSQL `ilike`** pattern matching — no external search engine
- Per-entity queries merged in Python
- Simple ranking: exact title match → prefix → contains → other fields → `updated_at` desc
- Returns frontend-relative URLs (e.g. `/work-items/{id}`)
- Entity lookup maps database rows to `EntityLookupResult` for `EntityReference` UI

## Auth

Requires authenticated viewer (`Authorization: Bearer` JWT).
