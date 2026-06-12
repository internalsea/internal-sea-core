# Local Test and Readiness Review

**Date:** 2026-06-12  
**Branch:** `main` (commit `7fccb70` at time of review)  
**Product name:** Internal Sea  
**Overall status:** **Ready with issues** — frontend checks pass; backend checks not executed in this environment (missing `uv`/Python); Docker/DB checks skipped.

---

## 1. Summary

This review prepared the repository for local testing by:

- Renaming user-facing product text from **Internal Sea Core** → **Internal Sea**
- Fixing frontend TypeScript errors (`apiPost` optional body)
- Running available frontend lint, typecheck, and build
- Documenting security/performance posture and follow-ups

The application behavior is unchanged except for display names and the `apiPost` default empty body (safe for no-payload POST endpoints).

**Technical names intentionally unchanged:**

| Identifier | Value | Reason |
|------------|-------|--------|
| Repository folder | `internal-sea-core` | Avoid breaking paths and CI |
| Python package | `internal-sea-core-api` | PyPI/project identity |
| Database | `internal_sea_core` | Avoid migration/connection breakage |
| localStorage keys | `internal_sea_core_*` | Avoid losing tenant/token state |

---

## 2. Commands executed

| Command | Result | Notes |
|---------|--------|-------|
| `pnpm install` (apps/web) | **Pass** | Dependencies up to date |
| `pnpm lint` (apps/web) | **Pass** | 4 warnings (react-refresh/only-export-components), 0 errors |
| `pnpm typecheck` (apps/web) | **Pass** | After `apiPost` body default fix |
| `pnpm build` (apps/web) | **Pass** | Bundle ~624 kB (chunk size warning) |
| `make api-check` | **Skipped** | `make` and `uv` not on PATH in review environment |
| `make web-check` | **Partial** | Equivalent: lint + typecheck + build all passed |
| `make check` | **Skipped** | Requires `make` + backend toolchain |
| `docker compose up` | **Skipped** | Docker not installed/available |
| `make db-migrate` / `make seed` | **Skipped** | Requires Docker/Postgres + `uv` |
| Backend pytest/ruff/mypy | **Skipped** | `uv` and working Python not available |

---

## 3. Issues fixed

| Area | Issue | Fix | Files changed |
|------|-------|-----|---------------|
| Product rename | Display name "Internal Sea Core" | Renamed to "Internal Sea" / "Internal Sea API" | README, docs, config, UI, tests, `.env.example`, etc. |
| Frontend TS | `apiPost` required body; queue/run-once calls had 1 arg | Default `body = {}` on `apiPost` | `apps/web/src/lib/apiClient.ts` |
| Config | Default API app name | `app_name = "Internal Sea API"` | `apps/api/app/config.py`, `.env.example` |
| Frontend config | Default APP_NAME | `'Internal Sea'` | `apps/web/src/lib/config.ts`, `apps/web/.env.example` |
| Health tests | Expected old service name | Updated assertions | `apps/api/tests/test_health.py` |
| Makefile help | Old product name in help text | Updated | `Makefile` |

---

## 4. Security findings

| Severity | Finding | Recommendation | Status |
|----------|---------|----------------|--------|
| Medium | Demo users with known passwords in seed | Local/demo only; never seed production | **Accepted for MVP** |
| Medium | JWT in localStorage | Accept for MVP; use HTTPS in production | **Accepted for MVP** |
| Medium | Tenant scoping partial (files, compliance, automation, etc.) | Extend `company_id` filters to remaining modules | **Follow-up required** |
| Low | Default `JWT_SECRET_KEY=change_me_later` | Rejected in production-like env via settings validator | **Fixed** (existing) |
| Low | CORS wildcard in production | Rejected in production-like env | **Fixed** (existing) |
| Low | `provider_config` secret keys | Validated in notification schemas | **Fixed** (existing) |
| Low | External notification delivery | Disabled by default (`NOTIFICATION_EXTERNAL_DELIVERY_ENABLED=false`) | **Fixed** (existing) |
| Low | Password hashes in API | `UserRead` excludes `hashed_password` | **Fixed** (existing) |
| Info | `AUTH_ENABLED=false` dev bypass | Documented; tests use bypass | **Accepted for MVP** |

No new critical vulnerabilities were introduced by the rename or review fixes.

**Tech debt:** All follow-up and mitigated findings are tracked in [TECH_DEBT_REGISTER.md](TECH_DEBT_REGISTER.md#security-review-results-2026-06-12).

---

## 5. Performance findings

| Severity | Finding | Recommendation | Status |
|----------|---------|----------------|--------|
| Low | Dashboard loads 11 independent API sections | Acceptable for MVP; `/dashboard/advanced` exists if combined load needed later | **Accepted for MVP** |
| Low | Frontend bundle > 500 kB | Code-splitting in future; not blocking local test | **Follow-up** |
| Low | Global React Query `staleTime: 30s` | Reduces refetch churn | **Fixed** (existing) |
| Low | Search debounce 280ms + max limit 50 | Adequate for MVP | **Fixed** (existing) |
| Low | Pagination max `page_size=100` | Enforced in `normalize_pagination` | **Fixed** (existing) |
| Info | `company_id` indexes in migration 0013 | Present on tenant-scoped tables | **Fixed** (existing) |

No risky caching or materialized views were added in this review.

---

## 6. Remaining risks before real production

- Demo users and seed data must not run in production
- JWT/localStorage auth — no SSO, MFA, or refresh tokens
- Tenant isolation needs deeper audit on non-priority modules
- No external monitoring, alerting, or backup automation documented as implemented
- External notification providers remain disabled/simulated
- Background worker is MVP-only (single instance, DB locks)
- Global unique constraints on Team/Capability names (not per-company)
- `company_id` nullable at database level

---

## 7. How to run tests locally

**Prerequisites:** [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/), Docker (for Postgres).

```bash
# Full check (recommended)
make install
make check

# Backend only
make api-check
# equivalent:
cd apps/api && uv run ruff check app tests alembic
cd apps/api && uv run mypy app
cd apps/api && uv run pytest tests/ -v

# Frontend only
make web-check
# equivalent:
cd apps/web && pnpm install
cd apps/web && pnpm lint
cd apps/web && pnpm typecheck
cd apps/web && pnpm build
```

**With database (integration):**

```bash
make docker-up
make db-migrate
make seed
cd apps/api && uv run pytest tests/integration/ -v
```

---

## 8. How to run the product locally

```bash
cp .env.example .env
cp apps/web/.env.example apps/web/.env   # optional; defaults work for localhost

make docker-up      # Postgres + Redis (+ API + Web in Compose)
make db-migrate
make seed

make api-dev        # terminal 1 — http://localhost:8000
make web-dev        # terminal 2 — http://localhost:5173
```

Open http://localhost:5173 — login or first-user onboarding.

---

## 9. Demo login

After `make seed`:

| Email | Password | Global role | Company role (demo) |
|-------|----------|-------------|---------------------|
| admin@example.com | admin12345 | admin | owner |
| editor@example.com | editor12345 | editor | editor |
| viewer@example.com | viewer12345 | viewer | viewer |

Demo company: **Internal Sea Demo** / **Default Workspace**

---

## 10. Recommended next fixes

### P0 (before production)

1. Complete tenant scoping on files, compliance, automation, performance, notifications modules
2. Change all secrets and disable seed in production
3. Enforce HTTPS and restrict CORS to production frontend origin

### P1 (should fix)

1. Make `company_id` NOT NULL after full backfill + enforcement
2. Per-company unique constraints for Team/Capability names
3. Run full integration test suite in CI with Postgres service
4. Frontend bundle code-splitting for dashboard routes

### P2 (later)

1. SSO / MFA
2. Refresh tokens or server-side session revocation
3. Import/export foundation (Prompt 30)
4. External monitoring and backup strategy

---

## 11. Smoke test checklist (manual)

After local run:

- [ ] Login page shows **Internal Sea**
- [ ] `admin@example.com` login works
- [ ] Top bar shows company + workspace
- [ ] Dashboard loads sections (some may show errors if API partial)
- [ ] Global search returns results
- [ ] Editor can create data product; viewer cannot
- [ ] `/onboarding/first-user` works on empty DB only
