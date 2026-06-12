# Production Readiness Checklist

Use before exposing Internal Sea beyond local/demo environments.

## Security

- [ ] `JWT_SECRET_KEY` changed from default
- [ ] `APP_ENV=production` (or staging) with `DEBUG=false`
- [ ] `AUTH_ENABLED=true`
- [ ] `CORS_ORIGINS` restricted to real frontend origin(s)
- [ ] HTTPS enabled end-to-end
- [ ] Demo users removed or deactivated
- [ ] Database passwords rotated from defaults
- [ ] Password policy reviewed (`PASSWORD_MIN_LENGTH`)

## Backend

- [ ] Alembic migrations run (`make db-migrate`)
- [ ] `/api/v1/health/live` returns 200
- [ ] `/api/v1/health/ready` returns 200
- [ ] Request IDs present (`X-Request-ID` header)
- [ ] Standard error responses (`error`, `message`, `request_id`)
- [ ] `make api-check` passes
- [ ] Logs collected from API stdout

## Frontend

- [ ] `VITE_API_BASE_URL` set at build time for production API
- [ ] `make web-check` passes
- [ ] Login/logout works
- [ ] 401 redirects to `/login` without loops
- [ ] Viewer cannot see editor write actions (UI + API verified)

## Database

- [ ] Backup strategy defined and tested
- [ ] Migration process documented
- [ ] Connection pool settings reviewed
- [ ] Seed **not** run in production (unless intentional)

## Operations

- [ ] [DEPLOYMENT_GUIDELINES.md](DEPLOYMENT_GUIDELINES.md) reviewed
- [ ] [OPERATIONS_RUNBOOK.md](OPERATIONS_RUNBOOK.md) accessible to on-call
- [ ] Rollback approach defined
- [ ] Monitoring approach defined (health endpoints minimum)

## Known MVP limitations

- No SSO / MFA
- No password reset flow
- No background worker execution
- No notification delivery
- No external file storage integration
- JWT stored in `localStorage` (frontend)
- No audit-grade immutable event log
- No advanced RBAC beyond viewer/editor/admin
- No rate limiting (unless enabled later)
- Redis configured but unused by core API paths
