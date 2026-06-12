# Relationships Module

Generic EntityLink layer connecting data products, work items, projects, people, teams and capabilities.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/relationships` | List links with filters |
| POST | `/api/v1/relationships` | Create link |
| GET | `/api/v1/relationships/entity/{type}/{id}` | Outgoing + incoming view |
| GET | `/api/v1/relationships/{id}` | Get link |
| PATCH | `/api/v1/relationships/{id}` | Update link |
| DELETE | `/api/v1/relationships/{id}` | Delete link |

Entity existence is validated in the service layer. No hard foreign keys to all entity tables.
