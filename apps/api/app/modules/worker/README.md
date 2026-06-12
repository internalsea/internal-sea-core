# Worker API

Admin endpoints for background worker visibility and manual cycle execution.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/worker/status` | viewer | Worker config and due counts |
| GET | `/worker/due-work` | viewer | Due and locked work summary |
| POST | `/worker/run-once` | editor | Run one in-process worker cycle |

`POST /worker/run-once` requires `WORKER_ENABLED=true`. Intended for local/admin use, not high-volume production.
