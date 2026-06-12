# Operations Runbook

Day-2 operations for Internal Sea (MVP).

## Startup checks

1. Postgres is running and reachable.
2. Migrations applied: `make db-current` shows head revision.
3. API starts without config validation errors.
4. `GET /api/v1/health/live` → 200
5. `GET /api/v1/health/ready` → 200 (database connected)
6. Web loads and login works.

## Database migration check

```bash
make db-current
make db-history
```

Migrations are **not** run automatically on API startup. Run `make db-migrate` after deploy.

## Seed / demo check

```bash
make seed
```

Idempotent — safe to repeat locally. Do not use in production.

Full local reset:

```bash
make demo-reset
```

## Login check

Demo credentials (local seed only):

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin12345 | admin |
| editor@example.com | editor12345 | editor |
| viewer@example.com | viewer12345 | viewer |

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin12345"}'
```

## Healthcheck

```bash
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8000/api/v1/health/ready
curl http://localhost:8000/api/v1/health
```

## Common errors

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| API won't start in production env | Default JWT secret or `DEBUG=true` | Fix `.env`, rotate secrets |
| 503 on `/health/ready` | DB down or wrong `DATABASE_URL` | Check Postgres, credentials, network |
| 401 on all API calls | Missing/expired token | Login again; check `AUTH_ENABLED` |
| 403 on writes as viewer | Expected RBAC | Use editor/admin account |
| CORS errors in browser | Origin not in `CORS_ORIGINS` | Add frontend URL to env |
| Frontend calls localhost API in prod | `VITE_API_BASE_URL` not set at build | Rebuild web with correct URL |

## Reset local environment

```bash
make demo-reset
# or
make docker-reset
make db-migrate
make seed
```

## Rotate JWT secret

1. Generate new secret.
2. Update `JWT_SECRET_KEY` in environment.
3. Restart API.
4. All users must log in again (existing tokens invalid).

## Deactivate a user

Admin: `PATCH /api/v1/auth/users/{id}` with `{"is_active": false}`.

Inactive users cannot authenticate; existing tokens are rejected on next request.

## Inspect logs

API logs go to stdout with format:

```
timestamp | LEVEL | logger | request_id=... | message
```

Request logging middleware logs method, path, status and duration.

**Never log passwords or JWT tokens.**

## Request tracing

Each response includes `X-Request-ID`. Pass the same header on retries to correlate client/server logs.

## Background worker

The worker is **optional**. The API runs without it; scheduled automation and queued notifications accumulate until processed.

### Run worker once (local)

```bash
make worker-once
# or
cd apps/api && uv run python -m app.worker.main run-once
```

### Run worker loop (local)

```bash
make worker-dev
# or
cd apps/api && uv run python -m app.worker.main run-loop --interval 30
```

### Docker worker profile

```bash
docker compose --profile worker up worker
# or
make docker-up-worker
```

### Check worker status

```bash
curl http://localhost:8000/api/v1/worker/status \
  -H "Authorization: Bearer PASTE_TOKEN"

curl http://localhost:8000/api/v1/worker/due-work \
  -H "Authorization: Bearer PASTE_TOKEN"
```

Or open **Automation** in the web UI (worker status cards).

### Clear expired locks

Locks expire automatically after `WORKER_LOCK_TIMEOUT_SECONDS` (default 300s). If a worker crashes mid-cycle, wait for expiry or manually clear:

```sql
UPDATE automation_triggers SET locked_at = NULL, locked_by = NULL, lock_expires_at = NULL
WHERE lock_expires_at < NOW();

UPDATE notification_messages SET locked_at = NULL, locked_by = NULL, lock_expires_at = NULL
WHERE lock_expires_at < NOW();
```

### Inspect failed automation runs

```bash
curl "http://localhost:8000/api/v1/automation/runs?status=failed" \
  -H "Authorization: Bearer PASTE_TOKEN"
```

Or use the Automation page run history.

### Inspect failed notification attempts

```bash
curl "http://localhost:8000/api/v1/notifications/delivery-attempts" \
  -H "Authorization: Bearer PASTE_TOKEN"
```

Or use the Notifications page delivery attempts table.
