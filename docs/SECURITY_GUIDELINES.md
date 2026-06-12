# Security Guidelines

Security practices for Internal Sea from foundation through production.

## Secrets and configuration

### Never commit secrets

- No passwords, API keys, JWT secrets or connection strings in git.
- Use `.env` locally; copy from `.env.example` and replace placeholders.
- `.env` is gitignored; only `.env.example` with safe defaults belongs in the repo.
- Rotate `JWT_SECRET_KEY` before any shared or production deployment.

### Environment files

| File | Purpose |
|------|---------|
| `.env.example` | Documented template, safe placeholder values |
| `.env` | Local overrides, never committed |

## Current MVP security model

- JWT bearer authentication with role-based access (`viewer`, `editor`, `admin`).
- Backend enforces permissions on every protected route.
- Frontend `PermissionGate` is additive UX only.
- Secrets via environment variables; production-like envs reject insecure defaults.
- Request IDs for traceability; errors do not leak stack traces unless `DEBUG=true`.

## Authentication (MVP — implemented)

- JWT bearer tokens via `POST /api/v1/auth/login`.
- Password hashing with bcrypt (passlib); never store plain-text passwords.
- Access token expiry configured via `ACCESS_TOKEN_EXPIRE_MINUTES` (default 8 hours).
- `JWT_SECRET_KEY` must be overridden in production; rotate on compromise.
- Frontend stores token in `localStorage` for MVP — use secure cookies or server sessions in production.
- Logout is client-side for JWT MVP (token discard).

### Production recommendations (not yet implemented)

- SSO (OIDC/SAML)
- MFA
- Password reset and invitation flows
- Refresh tokens and shorter access token TTL
- Environment-specific secrets and secret rotation

## Authorization (MVP — implemented)

- Roles: `viewer`, `editor`, `admin`, plus `is_superuser` bypass.
- Viewers can read; editors can mutate business objects; admins can manage users.
- Backend enforces permissions on all protected endpoints — UI gates are additive only.
- Principle of least privilege for admin roles.

## Automation (MVP)

- Automation actions must be **permission-gated** — viewers cannot create, edit or run triggers.
- **Unsafe action types must not run in MVP** — webhooks and AI actions are enum-only until implemented with allowlists.
- Future webhooks and AI actions require allowlists, secrets management and audit logs before production use.
- Manual runs are explicit (`simulate: false`); default is simulation.
- `action_config` JSON must be validated server-side before execution.

## Background worker (MVP)

- Worker must **not bypass** unsafe action restrictions — only MVP-safe actions execute on scheduled runs.
- **External delivery disabled by default** — worker simulates external channels unless explicitly enabled.
- **Secrets must not be stored in DB** — channel `provider_config` is non-secret metadata only.
- Worker logs must **not include tokens or passwords**.
- `POST /api/v1/worker/run-once` requires **editor/admin** — not for high-volume production use.

## Audit log (later)

- Record who changed what on sensitive entities (ownership, permissions, deletion).
- Retain audit entries according to org policy.

## SSO (later)

- Enterprise SSO (OIDC/SAML) when moving beyond local dev.
- Map IdP groups to application roles explicitly.

## Local development security

- Default Postgres and Redis credentials in Compose are **for local use only**.
- Do not expose Docker ports on untrusted networks without firewall rules.
- Use `CORS_ORIGINS` to restrict browser origins once the API runs.
- Keep dependencies updated; review Dependabot or similar alerts.

## Performance metrics

- Performance metrics may contain sensitive delivery or people-related data.
- **Write access requires editor** role; viewers can read scorecards and definitions.
- Future role refinements may restrict people metrics to managers or HR-approved roles.
- **Do not use metrics for HR compensation decisions** without proper governance and legal review.

## JWT limitations (MVP)

- No refresh tokens — users re-login when access token expires.
- Logout is client-side (token discarded).
- Tokens are not revocable server-side except by deactivating the user.
- `JWT_SECRET_KEY` rotation invalidates all outstanding tokens.

## Password storage

- bcrypt via passlib.
- Minimum length from `PASSWORD_MIN_LENGTH` (default 8).
- Passwords never logged or returned in API responses.

## SaaS tenant isolation

- **Tenant isolation is mandatory** — list and get operations must filter by `company_id` where the column exists.
- **`company_id` is server-assigned** on create — do not trust values from the request body.
- Frontend `X-Company-ID` / `X-Workspace-ID` headers are **context hints**; backend validates `CompanyMember` membership.
- Global `User.role` is not sufficient for SaaS tenant access — use `CompanyMember.role` for tenant objects.

## Secret management

- Set `JWT_SECRET_KEY`, database passwords and other secrets via environment.
- `APP_ENV=production` rejects `change_me_later` JWT secret and `DEBUG=true`.
- Use a secrets manager in hosted environments.

## CORS configuration

- `CORS_ORIGINS` is a comma-separated allowlist.
- Wildcard `*` is rejected in production-like environments.
- Must match the exact browser origin of the web app.

## Production checklist

See [PRODUCTION_READINESS_CHECKLIST.md](PRODUCTION_READINESS_CHECKLIST.md).

## Known limitations

- No SSO or MFA
- No password reset or invitation flows
- No audit-grade immutable logging
- `localStorage` token storage in frontend MVP
- No rate limiting by default (`RATE_LIMIT_ENABLED=false`)
- Redis configured but unused by core API paths

## Notifications

- Do not store provider secrets (tokens, API keys, passwords) in `provider_config` or the database.
- Do not log notification bodies if they may contain sensitive content.
- Do not log recipient secrets or webhook tokens.
- External webhook delivery requires allowlists and secret handling (future scope).
- Notification sending requires editor permission (or higher).

## API hygiene

- Validate and sanitize all input (Pydantic + ORM parameterization).
- Rate limiting on auth endpoints recommended for production (not enabled by default).
- HTTPS in production; HTTP acceptable on localhost only.
- Security headers on API and static responses (CSP, HSTS in production).

## Reporting

Report suspected vulnerabilities through internal channels defined by your organization. Do not open public issues with exploit details.

## Related docs

- [TECHNICAL_GUIDELINES.md](TECHNICAL_GUIDELINES.md) — implementation conventions
- [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md) — pre-commit checks
