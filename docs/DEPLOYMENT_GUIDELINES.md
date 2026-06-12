# Deployment Guidelines

How to deploy Internal Sea beyond local development.

## Overview

Internal Sea is a monorepo with:

- **API** — FastAPI (`apps/api`)
- **Web** — React/Vite static build (`apps/web`)
- **PostgreSQL** — required
- **Redis** — optional in MVP (configured but not required for core flows)

MVP deployment is **Docker-friendly** but does not include Kubernetes manifests.

## Prerequisites

1. PostgreSQL 16+
2. Reverse proxy with HTTPS (nginx, Caddy, Traefik, cloud load balancer)
3. Strong secrets for `JWT_SECRET_KEY` and database credentials
4. Node 22+ / pnpm for frontend production build (or CI artifact)

## Required environment variables

| Variable | Description |
|----------|-------------|
| `APP_ENV` | `production` or `staging` |
| `DEBUG` | `false` |
| `DATABASE_URL` | Async SQLAlchemy URL (`postgresql+asyncpg://...`) |
| `JWT_SECRET_KEY` | Long random secret (not `change_me_later`) |
| `AUTH_ENABLED` | `true` |
| `CORS_ORIGINS` | Exact frontend origin(s), comma-separated |
| `VITE_API_BASE_URL` | Public API URL used at **frontend build time** |

See root `.env.example` for the full list.

## Deployment steps

1. **Build frontend** with production API URL:
   ```bash
   cd apps/web
   VITE_API_BASE_URL=https://api.example.com/api/v1 pnpm build
   ```
2. **Build API image** (or run with uvicorn + gunicorn/uvicorn workers as needed).
3. **Run database migrations** (manual — not on API startup):
   ```bash
   make db-migrate
   ```
4. **Start API** behind HTTPS reverse proxy.
5. **Serve web** `dist/` as static files from CDN or web server.
6. **Verify health**:
   - `GET /api/v1/health/live`
   - `GET /api/v1/health/ready`

## Seed policy

- `make seed` is for **local demo only**.
- Do **not** run seed in production unless you intentionally want demo data.
- Remove or disable demo users before go-live.

## Docker deployment basics

Local/dev stack:

```bash
cp .env.example .env
make docker-up
make db-migrate
make seed   # optional, demo only
```

Example production-oriented Compose file: `infra/docker/docker-compose.prod.example.yml` (reference only).

## Reverse proxy notes

- Terminate TLS at the proxy.
- Forward `X-Forwarded-Proto` and `X-Forwarded-For` if needed.
- Allow `X-Request-ID` passthrough for traceability.
- Restrict admin endpoints to internal networks if possible.

## HTTPS

HTTPS is **required** in production. JWT in `localStorage` (MVP frontend) is vulnerable on plain HTTP.

## Backups

- Schedule PostgreSQL backups (daily minimum).
- Test restore periodically.
- Store backups encrypted and off-site.

## Rollback

1. Redeploy previous API/web artifacts.
2. If migration is backward-compatible, no DB action needed.
3. If migration is not reversible, restore DB from backup before redeploying old API.

## Healthcheck URLs

| Endpoint | Use |
|----------|-----|
| `/api/v1/health/live` | Process liveness |
| `/api/v1/health/ready` | DB readiness |
| `/api/v1/health` | Version/environment info |

## Background worker container

Run the worker as a **separate container/process** using the same API image and environment:

```bash
docker compose --profile worker up worker
```

Command: `python -m app.worker.main run-loop`

| Setting | Recommendation |
|---------|----------------|
| Instances | **One** worker initially (MVP) |
| Scaling | Not designed for high volume without external queue |
| API dependency | API must run independently; worker is optional |

Future: Redis/Celery or similar for horizontal scaling and durable queues.
