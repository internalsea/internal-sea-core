# Technical Debt Register

This register consolidates known MVP limitations, deferred decisions and follow-up work extracted from existing documentation (`docs/`, root and module READMEs). It is **not** a bug list only — it includes architecture, security, product, operational and UX debt already logged or implied in those docs.

**Security review:** Findings from [LOCAL_TEST_AND_READINESS_REVIEW.md](LOCAL_TEST_AND_READINESS_REVIEW.md) (2026-06-12) are mapped below and to individual TD items. Items marked **Mitigated** in that review are documented controls, not open debt.

Items marked **(inferred)** were not stated verbatim but follow directly from documented architecture, partial implementations or contradictions between docs and code.

**Last reviewed:** 2026-06-12 (post Phase 29 SaaS tenant foundation; security review incorporated)

---

## Security review results (2026-06-12)

Source: [LOCAL_TEST_AND_READINESS_REVIEW.md](LOCAL_TEST_AND_READINESS_REVIEW.md) — branch `main`, commit `7fccb70`.

**Review conclusion:** No new critical vulnerabilities from the rename/readiness pass. Backend security checks (pytest, ruff, mypy) were **not executed** in the review environment (missing `uv`/Python); treat TD-011 as the CI follow-up for automated verification.

### Section 4 — Security findings

| Review severity | Finding | Review status | Tech debt |
|-----------------|---------|---------------|-----------|
| Medium | Demo users with known passwords in seed | Accepted for MVP | [TD-002](#td-002-production-misconfiguration-risk-secrets-seed-demo-users) (P0) |
| Medium | JWT in `localStorage` | Accepted for MVP | [TD-005](#td-005-jwt-access-tokens-stored-in-localstorage) (P1) |
| Medium | Tenant scoping partial (files, compliance, automation, etc.) | **Follow-up required** | [TD-001](#td-001-incomplete-tenant-api-scoping-on-deferred-modules) (P0), [TD-008](#td-008-companymember-tenant-roles-not-enforced-on-all-modules) (P1) |
| Low | Default `JWT_SECRET_KEY=change_me_later` | **Fixed** (existing) | Mitigated — settings validator rejects in production-like env |
| Low | CORS wildcard in production | **Fixed** (existing) | Mitigated — validator rejects `*` in production-like env; deploy must set real origins ([TD-061](#td-061-production-https-and-cors-not-enforced-beyond-config-validation) (P0)) |
| Low | `provider_config` secret keys in DB | **Fixed** (existing) | Mitigated — schema validation; [TD-029](#td-029-no-notification-secret-manager-for-provider-credentials) (P2) for secret manager |
| Low | External notification delivery | **Fixed** (existing) | Mitigated — disabled by default; [TD-028](#td-028-external-notification-delivery-disabledsimulated-only) (P2) for real delivery |
| Low | Password hashes exposed in API | **Fixed** (existing) | Mitigated — `UserRead` excludes `hashed_password` |
| Info | `AUTH_ENABLED=false` dev bypass | Accepted for MVP | [TD-060](#td-060-auth_enabledfalse-dev-bypass-accepted-in-localtest-only) (P3) |

### Section 6 — Remaining risks before real production

| Risk | Tech debt |
|------|-----------|
| Demo users and seed data must not run in production | [TD-002](#td-002-production-misconfiguration-risk-secrets-seed-demo-users) (P0) |
| JWT/`localStorage` — no SSO, MFA, or refresh tokens | [TD-005](#td-005-jwt-access-tokens-stored-in-localstorage) (P1), [TD-014](#td-014-no-sso-oidcsaml)–[TD-016](#td-016-no-refresh-tokens-limited-server-side-revocation) (P2) |
| Tenant isolation needs deeper audit on non-priority modules | [TD-001](#td-001-incomplete-tenant-api-scoping-on-deferred-modules) (P0), [TD-003](#td-003-nullable-company_id-at-database-level) (P1) |
| No external monitoring, alerting, or backup automation | [TD-009](#td-009-no-production-monitoring-or-external-observability) (P1), [TD-010](#td-010-backup-and-restore-not-automated) (P1) |
| External notification providers disabled/simulated | [TD-028](#td-028-external-notification-delivery-disabledsimulated-only) (P2) |
| Background worker MVP-only (single instance, DB locks) | [TD-030](#td-030-worker-is-mvp-only-db-locks-single-instance-no-external-queue) (P2) |
| Global unique Team/Capability names (not per-company) | [TD-004](#td-004-global-unique-teamcapability-names-not-per-company) (P1) |
| `company_id` nullable at database level | [TD-003](#td-003-nullable-company_id-at-database-level) (P1) |

### Section 10 — Recommended next fixes

| Review priority | Recommendation | Tech debt |
|-----------------|----------------|-----------|
| P0 | Complete tenant scoping on deferred modules | [TD-001](#td-001-incomplete-tenant-api-scoping-on-deferred-modules) |
| P0 | Change all secrets and disable seed in production | [TD-002](#td-002-production-misconfiguration-risk-secrets-seed-demo-users) |
| P0 | Enforce HTTPS and restrict CORS to production frontend origin | [TD-061](#td-061-production-https-and-cors-not-enforced-beyond-config-validation) |
| P1 | Make `company_id` NOT NULL after backfill + enforcement | [TD-003](#td-003-nullable-company_id-at-database-level) |
| P1 | Per-company unique constraints for Team/Capability | [TD-004](#td-004-global-unique-teamcapability-names-not-per-company) |
| P1 | Run full integration test suite in CI with Postgres | [TD-011](#td-011-integration-tests-excluded-from-default-ci) |
| P1 | Frontend bundle code-splitting | [TD-012](#td-012-frontend-bundle-500-kb-without-route-code-splitting) |
| P2 | SSO / MFA | [TD-014](#td-014-no-sso-oidcsaml), [TD-015](#td-015-no-mfa) |
| P2 | Refresh tokens or server-side session revocation | [TD-016](#td-016-no-refresh-tokens-limited-server-side-revocation) |
| P2 | Import/export foundation | [TD-019](#td-019-importexport-foundation-not-implemented) |
| P2 | External monitoring and backup strategy | [TD-009](#td-009-no-production-monitoring-or-external-observability), [TD-010](#td-010-backup-and-restore-not-automated) |

---

## Summary

| ID | Title | Category | Severity | Priority | Area | Status |
|----|-------|----------|----------|----------|------|--------|
| TD-001 | Incomplete tenant API scoping on deferred modules | Tenancy | Critical | P0 | Tenancy | Open |
| TD-002 | Production misconfiguration risk (secrets, seed, demo users) | Security | Critical | P0 | Auth | Open |
| TD-061 | Production HTTPS and CORS not enforced beyond config validation | Security | High | P0 | Auth | Open |
| TD-003 | Nullable `company_id` at database level | Data Model | High | P1 | Tenancy | Open |
| TD-004 | Global unique Team/Capability names (not per-company) | Tenancy | High | P1 | Tenancy | Open |
| TD-005 | JWT access tokens stored in `localStorage` | Security | High | P1 | Auth | Open |
| TD-006 | No password reset or user invitation flows | Security | High | P1 | Auth | Open |
| TD-007 | Activity feed is not audit-grade; no immutable audit trail | Security | High | P1 | Compliance | Open |
| TD-008 | CompanyMember tenant roles not enforced on all modules | Tenancy | High | P1 | Tenancy | Open |
| TD-009 | No production monitoring or external observability | Operations | High | P1 | General | Open |
| TD-010 | Backup and restore not automated | Operations | High | P1 | General | Open |
| TD-011 | Integration tests excluded from default CI | DevEx | High | P1 | General | Open |
| TD-012 | Frontend bundle >500 kB without route code-splitting | Performance | Medium | P1 | General | Open |
| TD-013 | No rate limiting on auth or API endpoints | Security | Medium | P2 | Auth | Open |
| TD-014 | No SSO (OIDC/SAML) | Security | Medium | P2 | Auth | Open |
| TD-015 | No MFA | Security | Medium | P2 | Auth | Open |
| TD-016 | No refresh tokens; limited server-side revocation | Security | Medium | P2 | Auth | Open |
| TD-017 | RBAC limited to viewer/editor/admin global roles | Security | Medium | P2 | Auth | Open |
| TD-018 | Generic entity references without database FKs | Architecture | Medium | P2 | General | Open |
| TD-019 | Import/export foundation not implemented | Product | Medium | P2 | General | Open |
| TD-020 | No binary file upload, download or preview | Backend | Medium | P2 | Files | Open |
| TD-021 | No cloud storage provider integration (S3, SharePoint, etc.) | Backend | Medium | P2 | Files | Open |
| TD-022 | File sensitivity and evidence flags are metadata only | Product | Medium | P2 | Files | Open |
| TD-023 | Compliance checks are manual only | Product | Medium | P2 | Compliance | Open |
| TD-024 | No automated compliance rule execution or schedules | Product | Medium | P2 | Compliance | Open |
| TD-025 | No compliance approval workflows or audit export | Product | Medium | P2 | Compliance | Open |
| TD-026 | Manual performance metrics only; no calculation engine | Product | Medium | P2 | Performance | Open |
| TD-027 | People metrics readable by all viewers; no HR role refinement | Security | Medium | P2 | Performance | Open |
| TD-028 | External notification delivery disabled/simulated only | Product | Medium | P2 | Notifications | Open |
| TD-029 | No notification secret manager for provider credentials | Security | Medium | P2 | Notifications | Open |
| TD-030 | Worker is MVP-only (DB locks, single instance, no external queue) | Architecture | Medium | P2 | Worker | Open |
| TD-031 | Unsafe automation actions (webhooks, AI) blocked/skipped | Security | Medium | P2 | Worker | Open |
| TD-032 | No complex cron parser; manual `next_run_at` for custom schedules | Backend | Medium | P2 | Worker | Open |
| TD-033 | Dashboard loads many independent API sections | Performance | Medium | P2 | Dashboard | Open |
| TD-034 | Dashboard aggregates computed at request time (no materialized views) | Performance | Medium | P2 | Dashboard | Open |
| TD-035 | PostgreSQL `ilike` search only; no full-text or fuzzy ranking | Performance | Medium | P2 | Search | Open |
| TD-036 | Rollback and disaster recovery process is manual | Operations | Medium | P2 | General | Open |
| TD-037 | No billing, subscriptions or plan limits | Product | Medium | P2 | Tenancy | Open |
| TD-038 | Multi-company and deep workspace switching UI incomplete | UX | Medium | P2 | Tenancy | Open |
| TD-039 | Single primary team and capability per person | Data Model | Medium | P2 | General | Open |
| TD-040 | Limited frontend automated test coverage | DevEx | Medium | P2 | General | Open |
| TD-041 | Stale or contradictory module documentation | Documentation | Medium | P2 | General | Open |
| TD-042 | Redis configured but unused by core API paths | Architecture | Low | P3 | General | Open |
| TD-043 | Monorepo package coupling risk if boundaries ignored | Architecture | Low | P3 | General | Open |
| TD-044 | Manual TypeScript/Python type sharing (no codegen) | DevEx | Low | P3 | General | Open |
| TD-046 | No Kubernetes manifests; Docker Compose reference only | Operations | Low | P3 | General | Open |
| TD-047 | Work board has no drag-and-drop | UX | Low | P3 | General | Open |
| TD-048 | Manual UUID fallbacks remain in advanced form sections | UX | Low | P3 | General | Open |
| TD-049 | Comments are plain text only (no rich text, mentions, attachments) | UX | Low | P3 | General | Open |
| TD-050 | Activity events use placeholder actors; `actor_id` optional | Backend | Low | P3 | General | Open |
| TD-051 | No dedicated global search results page | UX | Low | P3 | Search | Open |
| TD-052 | No chart library; tables and badges only for metrics/dashboard | UX | Low | P3 | Dashboard | Open |
| TD-053 | EntityLink types for governance entities not yet supported | Product | Low | P3 | General | Open |
| TD-054 | Target commercial/ops modules not implemented (deals, meetings, tools) | Product | Low | P3 | General | Open |
| TD-055 | No virus scanning or antivirus pipeline for files | Security | Low | P3 | Files | Open |
| TD-056 | No notification digest or subscription preference engine | Product | Low | P3 | Notifications | Open |
| TD-057 | Dashboard health scores are transparent heuristics, not official KPIs | Product | Low | P3 | Dashboard | Open |
| TD-058 | No AI-generated insights or assistant layer | Product | Low | P3 | Dashboard | Open |
| TD-059 | Skills, allocations and many-to-many team membership not modeled | Product | Low | P3 | General | Open |
| TD-060 | `AUTH_ENABLED=false` dev bypass accepted in local/test only | Security | Low | P3 | Auth | Open |

**Totals:** 61 items — P0: 3 · P1: 10 · P2: 29 · P3: 19

---

## P0 — Must Fix Before Real Usage

### TD-001: Incomplete tenant API scoping on deferred modules

Category: Tenancy  
Severity: Critical  
Priority: P0  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md, docs/IMPLEMENTATION_ROADMAP.md (Phase 29), docs/SECURITY_GUIDELINES.md, inferred (router audit)  
Area: Tenancy

Description:
Phase 29 added `company_id` / `workspace_id` columns and tenant scoping to **priority modules** (data products, work items, projects, people, teams, capabilities, dashboard, search). Modules such as **files, compliance, automation, performance, notifications, relationships, comments and activity** do not yet filter by tenant in their API layers.

Why it matters:
Cross-company data exposure is possible if two tenants share a deployment and unscoped modules return or mutate rows without `company_id` filtering.

Current workaround:
Single-tenant local/demo usage with one seeded company (Internal Sea Demo). Priority modules are scoped.

Recommended fix:
Add `CurrentTenant` dependencies and repository-level `company_id` filters to every module with tenant columns. Add cross-tenant isolation tests per module.

Suggested prompt:
Tenant Isolation Hardening (complete module scoping)

---

### TD-002: Production misconfiguration risk (secrets, seed, demo users)

Category: Security  
Severity: Critical  
Priority: P0  
Status: Open  
Source: docs/PRODUCTION_READINESS_CHECKLIST.md, docs/LOCAL_TEST_AND_READINESS_REVIEW.md, docs/DEPLOYMENT_GUIDELINES.md, docs/DEVELOPMENT_GUIDELINES.md  
Area: Auth

Description:
Demo users with known passwords are created by `make seed`. Default Compose credentials and documented demo logins are acceptable locally but dangerous if seed or defaults reach a shared or production environment. Settings validation rejects some insecure defaults in production-like envs, but operational discipline is required.

Why it matters:
Known credentials and demo data in production expose all tenant data and undermine audit trust.

Current workaround:
Documentation warns not to seed production; `APP_ENV=production` rejects default JWT secret and `DEBUG=true`.

Recommended fix:
Add deploy-time guardrails (seed blocked when `APP_ENV=production`, startup check for demo user emails, runbook checklist automation). Rotate all secrets before go-live.

Suggested prompt:
Production Operations and Monitoring (deploy guardrails)

---

### TD-061: Production HTTPS and CORS not enforced beyond config validation

Category: Security  
Severity: High  
Priority: P0  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md (§4 Low CORS, §10 P0 #3), docs/DEPLOYMENT_GUIDELINES.md, docs/SECURITY_GUIDELINES.md  
Area: Auth

Description:
The security review flagged production HTTPS and restricted CORS as P0 before real usage. Settings validation rejects CORS wildcard `*` in production-like environments, but **HTTPS termination, HSTS and origin alignment depend entirely on reverse-proxy and deploy configuration**. The application does not redirect HTTP→HTTPS or fail startup when served over plain HTTP.

Why it matters:
JWT in `localStorage` (TD-005) is exposed on unencrypted connections. Misconfigured CORS or HTTP deploy defeats auth and tenant isolation for browser clients.

Current workaround:
Documentation requires HTTPS in production; `CORS_ORIGINS` must list exact frontend origin(s); JWT localStorage acceptable only with HTTPS per security guidelines.

Recommended fix:
Add production security headers (HSTS, CSP baseline); deploy checklist automation verifying TLS and `CORS_ORIGINS`; optional startup warning when `APP_ENV=production` and proxy headers indicate non-HTTPS.

Suggested prompt:
Production Operations and Monitoring (HTTPS/CORS hardening)

---

## P1 — Must Fix Before Team Pilot

### TD-003: Nullable `company_id` at database level

Category: Data Model  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, docs/IMPLEMENTATION_ROADMAP.md (Phase 29), docs/LOCAL_TEST_AND_READINESS_REVIEW.md  
Area: Tenancy

Description:
Migration `0013` added nullable `company_id` / `workspace_id` for safe backfill. Database constraints do not yet enforce tenant presence on business rows.

Why it matters:
Orphan or cross-tenant rows can be inserted if application validation is bypassed or a module omits tenant assignment.

Current workaround:
Seed backfill (`app/seed/tenant.py`) and service-layer assignment on create in scoped modules.

Recommended fix:
After full module scoping (TD-001), backfill NULLs, add NOT NULL constraints and indexes, verify with migration tests.

Suggested prompt:
Tenant Isolation Hardening (NOT NULL migration)

---

### TD-004: Global unique Team/Capability names (not per-company)

Category: Tenancy  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md, inferred  
Area: Tenancy

Description:
Team and Capability name uniqueness appears to be global, not scoped per company, causing collisions when multiple companies exist in one deployment.

Why it matters:
Second tenant cannot create teams/capabilities with common names; seed and onboarding may fail unpredictably.

Current workaround:
Single demo company in local use.

Recommended fix:
Replace global unique constraints with composite `(company_id, name)` uniqueness; update seed and tests.

Suggested prompt:
Tenant Isolation Hardening (per-company uniqueness)

---

### TD-005: JWT access tokens stored in `localStorage`

Category: Security  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md (§4 Medium), docs/SECURITY_GUIDELINES.md, apps/web/src/features/auth/README.md, docs/PRODUCTION_READINESS_CHECKLIST.md, ADR-0027  
Area: Auth

Description:
Frontend stores bearer tokens in `localStorage` (`internal_sea_core_access_token`). Tokens are accessible to any script on the page.

Why it matters:
XSS or malicious extensions can exfiltrate tokens. Production guidance requires HTTPS but storage pattern remains vulnerable.

Current workaround:
MVP JWT with short-ish TTL (default 8 hours); HTTPS required in production docs.

Recommended fix:
Move to HttpOnly secure cookies or BFF session pattern; add CSP headers; shorten access token TTL when refresh flow exists.

Suggested prompt:
Auth Security Hardening (secure token storage)

---

### TD-006: No password reset or user invitation flows

Category: Security  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md, docs/PRODUCT_REQUIREMENTS.md (SaaS foundation)  
Area: Auth

Description:
Users cannot reset passwords or receive invite links. New company members require manual user creation by an admin.

Why it matters:
Blocks self-service team onboarding for any pilot beyond a handful of manually provisioned accounts.

Current workaround:
Admin creates users via API; demo credentials documented for local use.

Recommended fix:
Add password reset tokens, email delivery (depends on TD-028), and company invite flow tied to CompanyMember.

Suggested prompt:
Auth Security Hardening (password reset and invites)

---

### TD-007: Activity feed is not audit-grade; no immutable audit trail

Category: Security  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md, docs/DATA_MODEL.md, docs/TECHNICAL_GUIDELINES.md  
Area: Compliance

Description:
`ActivityEvent` records operational history but is not tamper-evident, security-focused or exportable for compliance. `AuditEvent` is documented as target-only.

Why it matters:
Cannot prove who changed permissions, ownership or sensitive records for governance or incident response.

Current workaround:
Activity timeline on detail pages; request IDs in API logs.

Recommended fix:
Introduce append-only audit log (separate table or external store), wire auth actor on all mutations, retention and export API.

Suggested prompt:
Production Operations and Monitoring (audit trail foundation)

---

### TD-008: CompanyMember tenant roles not enforced on all modules

Category: Tenancy  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, apps/api/app/modules/tenancy/README.md, inferred  
Area: Tenancy

Description:
Global `User.role` remains the primary gate on many endpoints. `CompanyMember.role` (owner/admin/editor/viewer) is documented as required for tenant objects but is not consistently applied outside tenancy and priority modules.

Why it matters:
A viewer in one company who is editor globally could exceed intended tenant permissions.

Current workaround:
Single demo company; global roles align with company roles in seed data.

Recommended fix:
Replace or augment `EditorUser`/`ViewerUser` with tenant-aware dependencies that check CompanyMember role per request.

Suggested prompt:
Tenant Isolation Hardening (CompanyMember RBAC)

---

### TD-009: No production monitoring or external observability

Category: Operations  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md, docs/PRODUCTION_READINESS_CHECKLIST.md, docs/DEPLOYMENT_GUIDELINES.md, ADR (request ID only)  
Area: General

Description:
Only health endpoints and stdout logging exist. No metrics, alerting, APM or log aggregation is documented as implemented.

Why it matters:
Team pilot failures (DB saturation, worker stalls, 5xx spikes) will be invisible until users report them.

Current workaround:
Manual health checks (`/health/live`, `/health/ready`); `X-Request-ID` for correlation.

Recommended fix:
Define minimum observability stack (metrics for latency/errors, structured log shipping, alert rules on health and worker queue depth).

Suggested prompt:
Production Operations and Monitoring

---

### TD-010: Backup and restore not automated

Category: Operations  
Severity: High  
Priority: P1  
Status: Open  
Source: docs/DEPLOYMENT_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md, docs/LOCAL_TEST_AND_READINESS_REVIEW.md  
Area: General

Description:
Backup strategy is documented as a requirement but no scripts, schedules or restore drills are part of the repo.

Why it matters:
Data loss or bad migration without tested backups blocks recovery.

Current workaround:
Manual PostgreSQL backup guidance in deployment docs.

Recommended fix:
Add documented backup/restore scripts, encrypted off-site storage, and quarterly restore test checklist.

Suggested prompt:
Production Operations and Monitoring (backup automation)

---

### TD-011: Integration tests excluded from default CI

Category: DevEx  
Severity: High  
Priority: P1  
Status: Open  
Source: apps/api/pyproject.toml, docs/DEVELOPMENT_GUIDELINES.md, docs/LOCAL_TEST_AND_READINESS_REVIEW.md, `.github/workflows/ci.yml`  
Area: General

Description:
Pytest defaults exclude `@pytest.mark.integration`. CI runs migration-check against Postgres but does not run integration tests (seed, dashboard, search) in the default pipeline.

Why it matters:
Tenant scoping, migrations and cross-module regressions may ship undetected.

Current workaround:
Developers run `pytest tests/integration/` locally with Docker Postgres.

Recommended fix:
Add CI job running integration tests after `alembic upgrade head` on Postgres service; include tenancy isolation cases.

Suggested prompt:
Production Operations and Monitoring (CI hardening)

---

### TD-012: Frontend bundle >500 kB without route code-splitting

Category: Performance  
Severity: Medium  
Priority: P1  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md  
Area: General

Description:
Production build emits a single large JS chunk (~624 kB) with Vite chunk-size warning.

Why it matters:
Slower first load for pilot users on typical corporate networks; affects perceived quality.

Current workaround:
Acceptable for local demo; app functions correctly.

Recommended fix:
Lazy-load heavy routes (dashboard, compliance, automation) via `React.lazy` and manual chunks.

Suggested prompt:
Dashboard Performance Optimization (frontend splitting)

---

## P2 — Should Fix Before Production Scale

### TD-013: No rate limiting on auth or API endpoints

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md  
Area: Auth

Description:
`RATE_LIMIT_ENABLED=false` by default. Auth endpoints are vulnerable to brute-force attempts at scale.

Why it matters:
Increased risk when API is internet-exposed beyond trusted network.

Current workaround:
Network-level restrictions; low user count in pilot.

Recommended fix:
Enable rate limiting middleware on `/auth/login` and sensitive write endpoints; configure per-IP thresholds.

Suggested prompt:
Auth Security Hardening (rate limiting)

---

### TD-014: No SSO (OIDC/SAML)

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md, ADR-0027  
Area: Auth

Description:
Enterprise SSO is explicitly deferred. Only email/password JWT login exists.

Why it matters:
Many organizations require IdP-managed identities for internal tools.

Current workaround:
Local/demo JWT auth with bcrypt passwords.

Recommended fix:
Add OIDC provider integration; map IdP groups to CompanyMember roles.

Suggested prompt:
Auth Security Hardening (SSO)

---

### TD-015: No MFA

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md, ADR-0027  
Area: Auth

Description:
Multi-factor authentication is not implemented.

Why it matters:
Password-only auth is insufficient for many security policies.

Current workaround:
Strong passwords; HTTPS; limited user base.

Recommended fix:
Add TOTP or WebAuthn as optional second factor post-SSO or standalone.

Suggested prompt:
Auth Security Hardening (MFA)

---

### TD-016: No refresh tokens; limited server-side revocation

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, ADR-0027  
Area: Auth

Description:
Access tokens expire; no refresh token flow. Logout is client-side token discard. Revocation requires deactivating the user.

Why it matters:
Stolen tokens remain valid until expiry; no session management for admins.

Current workaround:
Deactivate user via admin API; rotate JWT secret to invalidate all tokens.

Recommended fix:
Add refresh tokens with rotation, token blocklist or session store in Redis.

Suggested prompt:
Auth Security Hardening (sessions)

---

### TD-017: RBAC limited to viewer/editor/admin global roles

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCTION_READINESS_CHECKLIST.md, docs/SECURITY_GUIDELINES.md  
Area: Auth

Description:
No fine-grained permissions (per-module, per-resource). Three global roles plus `is_superuser`.

Why it matters:
Cannot express data-owner vs compliance-officer vs HR-only access patterns.

Current workaround:
CompanyMember roles at tenant level (partial); PermissionGate hides UI actions.

Recommended fix:
Design permission matrix; extend backend enforcement beyond coarse roles.

Suggested prompt:
Auth Security Hardening (advanced RBAC)

---

### TD-018: Generic entity references without database FKs

Category: Architecture  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, docs/TECHNICAL_GUIDELINES.md  
Area: General

Description:
EntityLink, FileAttachment, ComplianceCheck, PerformanceMetricValue and AutomationTrigger use `entity_type` + `entity_id` with service-layer validation instead of FKs.

Why it matters:
Orphan references and inconsistent validation if a module forgets checks; harder DB-level integrity.

Current workaround:
Explicit `SUPPORTED_*_TYPES` lists and service validation.

Recommended fix:
Keep pattern for flexibility but add referential integrity tests, periodic orphan scans and shared validation library.

Suggested prompt:
Tenant Isolation Hardening (reference validation audit)

---

### TD-019: Import/export foundation not implemented

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/IMPLEMENTATION_ROADMAP.md (Phase 30), docs/PROJECT_VISION.md, docs/LOCAL_TEST_AND_READINESS_REVIEW.md  
Area: General

Description:
No CSV/JSON export, backup from UI or import templates. Phase 30 is planned but not started.

Why it matters:
Teams cannot migrate data, produce offline reports or recover from bulk editing mistakes.

Current workaround:
Direct database access for admins; manual copy.

Recommended fix:
Implement Phase 30 import/export API and UI for core entities.

Suggested prompt:
Import/Export Foundation

---

### TD-020: No binary file upload, download or preview

Category: Backend  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, docs/DATA_MODEL.md, docs/TECHNICAL_GUIDELINES.md, apps/api/app/modules/files/README.md  
Area: Files

Description:
Files module stores metadata and external URLs only. No upload endpoint, preview or download streaming.

Why it matters:
Evidence and document workflows require users to host files elsewhere manually.

Current workaround:
Register external links; attach by file UUID from metadata records.

Recommended fix:
Add upload API with size limits, storage backend abstraction and signed download URLs.

Suggested prompt:
File Handling and Storage Hardening (upload)

---

### TD-021: No cloud storage provider integration (S3, SharePoint, etc.)

Category: Backend  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, docs/PRODUCT_REQUIREMENTS.md, docs/PRODUCTION_READINESS_CHECKLIST.md  
Area: Files

Description:
`FileStorage` model exists but provider integration and `storage_path` / `checksum` population are future scope.

Why it matters:
Enterprise files live in governed storage; metadata-only links do not enforce retention or access policy.

Current workaround:
External URL field on FileAsset.

Recommended fix:
Implement S3-compatible adapter first; optional SharePoint connector.

Suggested prompt:
File Handling and Storage Hardening (providers)

---

### TD-022: File sensitivity and evidence flags are metadata only

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, apps/api/app/modules/files/README.md  
Area: Files

Description:
Sensitivity labels and evidence flags do not enforce download restrictions or compliance policy.

Why it matters:
UI suggests governance but backend does not block unauthorized access to linked external URLs.

Current workaround:
Role-based API access only at record level.

Recommended fix:
 Tie sensitivity to permission checks and audit events when evidence is accessed.

Suggested prompt:
File Handling and Storage Hardening (policy enforcement)

---

### TD-023: Compliance checks are manual only

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, docs/TECHNICAL_GUIDELINES.md, apps/api/app/modules/compliance/README.md  
Area: Compliance

Description:
Compliance checks are created and evaluated manually. No runner evaluates rules against live data.

Why it matters:
Governance scale requires automation; manual checks do not scale past pilot.

Current workaround:
Compliance officers record check outcomes and attach evidence files.

Recommended fix:
Add scheduled check runner against rule definitions with result history.

Suggested prompt:
Compliance Automation (future — not in current prompt set)

---

### TD-024: No automated compliance rule execution or schedules

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, docs/DATA_MODEL.md  
Area: Compliance

Description:
Policies and rules exist but automated evaluation, schedules and exceptions are target-only.

Why it matters:
Cannot detect drift continuously; relies on human discipline.

Current workaround:
Manual checks linked to policies/rules.

Recommended fix:
Integrate compliance engine with automation worker (TD-030) when rules stabilize.

Suggested prompt:
Worker and Notification Reliability (compliance jobs)

---

### TD-025: No compliance approval workflows or audit export

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, docs/PRODUCT_REQUIREMENTS.md, apps/web/src/features/compliance/README.md  
Area: Compliance

Description:
Exception, Approval entities and regulatory mapping are documented but not implemented. No export of compliance evidence pack.

Why it matters:
Regulated teams need sign-off trails and auditor-ready exports.

Current workaround:
Evidence links and activity timeline partially document changes.

Recommended fix:
Add approval workflow model and CSV/PDF export of checks and evidence.

Suggested prompt:
Import/Export Foundation (compliance export)

---

### TD-026: Manual performance metrics only; no calculation engine

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, apps/api/app/modules/performance/README.md, docs/TECHNICAL_GUIDELINES.md  
Area: Performance

Description:
Metric values are entered manually. Scorecards aggregate latest values but nothing computes metrics from work/project data.

Why it matters:
Dashboard performance insights show gaps but teams must maintain metrics by hand.

Current workaround:
Seeded demo scorecards; manual entry UI.

Recommended fix:
Define calculation rules per metric code; optional scheduled recomputation job.

Suggested prompt:
Dashboard Performance Optimization (metric engine)

---

### TD-027: People metrics readable by all viewers; no HR role refinement

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md  
Area: Performance

Description:
Viewers can read all performance scorecards including people metrics. Future manager/HR restrictions documented but not built.

Why it matters:
People-related delivery data may be sensitive; over-sharing in pilot.

Current workaround:
Documentation warns against compensation use; trust model.

Recommended fix:
Add scoped read permissions for `subject_type=person` metrics.

Suggested prompt:
Auth Security Hardening (metrics ACL)

---

### TD-028: External notification delivery disabled/simulated only

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, docs/PRODUCT_REQUIREMENTS.md, README.md, apps/api/app/worker/README.md  
Area: Notifications

Description:
Email, Teams, Slack and webhook delivery are future scope. `NOTIFICATION_EXTERNAL_DELIVERY_ENABLED=false` by default; worker simulates delivery.

Why it matters:
Automations cannot notify users outside the app; pilot relies on in-app records only.

Current workaround:
Simulation mode; in-app message status updates for in-app channels.

Recommended fix:
Implement provider adapters with env-based secrets and allowlisted endpoints.

Suggested prompt:
Worker and Notification Reliability (external delivery)

---

### TD-029: No notification secret manager for provider credentials

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, docs/SECURITY_GUIDELINES.md  
Area: Notifications

Description:
`provider_config` must not store secrets; credentials expected via environment variables. No integrated secret manager.

Why it matters:
Multi-tenant SaaS eventually needs per-tenant provider credentials safely.

Current workaround:
Global env vars for single deployment.

Recommended fix:
Integrate with host secret manager; reference secret IDs in channel config only.

Suggested prompt:
Worker and Notification Reliability (secrets)

---

### TD-030: Worker is MVP-only (DB locks, single instance, no external queue)

Category: Architecture  
Severity: Medium  
Priority: P2  
Status: Open  
Source: apps/api/app/worker/README.md, docs/DEPLOYMENT_GUIDELINES.md, docs/TECHNICAL_GUIDELINES.md, ADR-0026  
Area: Worker

Description:
Background worker uses PostgreSQL row locks, single recommended instance, no Redis/Celery/Temporal. Due work accumulates if worker is down.

Why it matters:
Not horizontally scalable; crash mid-cycle relies on lock expiry (default 300s).

Current workaround:
Optional worker container; manual `run-once` from Automation UI; SQL to clear stale locks documented in runbook.

Recommended fix:
Introduce durable queue (Redis/Celery) when notification/automation volume requires it.

Suggested prompt:
Worker and Notification Reliability (queue upgrade)

---

### TD-031: Unsafe automation actions (webhooks, AI) blocked/skipped

Category: Security  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/SECURITY_GUIDELINES.md, apps/api/app/modules/automation/README.md  
Area: Worker

Description:
Webhook and AI action types exist in enums but are rejected or skipped on real runs until allowlists, secrets and audit exist.

Why it matters:
Limits automation value but is intentional security posture.

Current workaround:
Safe actions only: create work item, comment, activity event, simulated notification.

Recommended fix:
Implement webhook allowlist, signing and audit before enabling.

Suggested prompt:
Worker and Notification Reliability (safe webhooks)

---

### TD-032: No complex cron parser; manual `next_run_at` for custom schedules

Category: Backend  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, apps/web/README.md, docs/DESIGN_GUIDELINES.md  
Area: Worker

Description:
Schedules store `cron_expression` but MVP worker uses simple frequency and manual `next_run_at` updates for custom cases.

Why it matters:
Operators must manually maintain schedule times for complex cron patterns.

Current workaround:
Preset frequencies; editor sets `next_run_at` via API/UI.

Recommended fix:
Add standards-compliant cron evaluation in worker cycle.

Suggested prompt:
Worker and Notification Reliability (cron parser)

---

### TD-033: Dashboard loads many independent API sections

Category: Performance  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md, docs/DESIGN_GUIDELINES.md, apps/web/src/features/dashboard/README.md  
Area: Dashboard

Description:
Dashboard UI issues ~11 separate TanStack Query calls (one per section). Combined `/dashboard/advanced` exists but UI loads sections independently.

Why it matters:
Latency and connection overhead grow with user count and section count.

Current workaround:
Independent loading isolates failures; 30s staleTime reduces refetch.

Recommended fix:
Optional aggregated fetch for initial paint; parallelize with HTTP/2; cache aggregates briefly server-side.

Suggested prompt:
Dashboard Performance Optimization

---

### TD-034: Dashboard aggregates computed at request time (no materialized views)

Category: Performance  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, docs/TECHNICAL_GUIDELINES.md  
Area: Dashboard

Description:
Advanced dashboard is a read model over live tables with dynamic scoring. No materialized views or snapshot tables.

Why it matters:
Query cost increases linearly with data volume; risk of slow dashboard under load.

Current workaround:
Section limits (max 50); indexes on tenant columns; acceptable for MVP data sizes.

Recommended fix:
Add materialized views or scheduled snapshot job when p95 dashboard latency exceeds SLO.

Suggested prompt:
Dashboard Performance Optimization (read model caching)

---

### TD-035: PostgreSQL `ilike` search only; no full-text or fuzzy ranking

Category: Performance  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, docs/PRODUCT_REQUIREMENTS.md, apps/web/README.md  
Area: Search

Description:
Global search uses simple `ilike` per entity type merged in Python. No PostgreSQL FTS, fuzzy match or external search engine.

Why it matters:
Poor relevance and performance on large catalogs; typos miss results.

Current workaround:
Debounce 280ms; max 50 results; seed-sized datasets.

Recommended fix:
Add PostgreSQL `tsvector` indexes or dedicated search service when needed.

Suggested prompt:
Dashboard Performance Optimization (search upgrade)

---

### TD-036: Rollback and disaster recovery process is manual

Category: Operations  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DEPLOYMENT_GUIDELINES.md, docs/PRODUCTION_READINESS_CHECKLIST.md  
Area: General

Description:
Rollback steps are documented (redeploy artifacts, restore DB if migration irreversible) but not automated or tested in CI.

Why it matters:
Slow recovery during failed deploys.

Current workaround:
Manual runbook steps.

Recommended fix:
Document and test blue/green or migration compatibility matrix; automate artifact rollback.

Suggested prompt:
Production Operations and Monitoring (rollback runbook)

---

### TD-037: No billing, subscriptions or plan limits

Category: Product  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, docs/DECISION_LOG.md (ADR-0029)  
Area: Tenancy

Description:
SaaS tenant foundation excludes billing, subscriptions, plan tiers and usage limits.

Why it matters:
Required for external SaaS commercialization; acceptable for internal pilot.

Current workaround:
Single org internal deployment model.

Recommended fix:
Defer until product commercialization; add plan limits on seats and storage when needed.

Suggested prompt:
SaaS Billing Foundation (future — out of TD prompt set)

---

### TD-038: Multi-company and deep workspace switching UI incomplete

Category: UX  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, apps/api/app/modules/tenancy/README.md, inferred  
Area: Tenancy

Description:
Headers support multi-company selection but UI focuses on current company badge and settings. Deep workspace switching and org lifecycle management are limited.

Why it matters:
Users in multiple companies need clearer switcher UX for pilot.

Current workaround:
`X-Company-ID` header from localStorage; first workspace default.

Recommended fix:
Add company/workspace switcher dropdown in TopBar; persist last selection.

Suggested prompt:
Tenant Isolation Hardening (multi-company UX)

---

### TD-039: Single primary team and capability per person

Category: Data Model  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/DATA_MODEL.md, ADR-0012  
Area: General

Description:
Person model allows one `team_id` and one `capability_id`. Skills and allocations deferred.

Why it matters:
Real org structures are many-to-many; limits capacity planning accuracy.

Current workaround:
Primary team/capability for MVP linking and dashboards.

Recommended fix:
Add junction tables and allocation time ranges in a dedicated phase.

Suggested prompt:
Organization Model Expansion (future)

---

### TD-040: Limited frontend automated test coverage

Category: DevEx  
Severity: Medium  
Priority: P2  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, docs/DEVELOPMENT_GUIDELINES.md  
Area: General

Description:
Backend has pytest coverage; frontend relies on lint, typecheck and build without systematic component or E2E tests.

Why it matters:
UI regressions in pilot may reach users undetected.

Current workaround:
Manual smoke checklist in LOCAL_TEST_AND_READINESS_REVIEW.md.

Recommended fix:
Add Playwright smoke tests for login, dashboard, CRUD happy paths.

Suggested prompt:
Production Operations and Monitoring (E2E tests)

---

### TD-041: Stale or contradictory module documentation

Category: Documentation  
Severity: Medium  
Priority: P2  
Status: Open  
Source: apps/api/app/modules/dashboard/README.md, apps/web/src/features/work-items/README.md, apps/web/src/features/compliance/README.md, apps/web/README.md, docs/COMPONENT_ARCHITECTURE.md, docs/PRODUCTION_READINESS_CHECKLIST.md, inferred  
Area: General

Description:
Several READMEs contradict current implementation (e.g. dashboard auth "not implemented", work-items "no auth", compliance "no entity picker", web README "paste UUIDs", PRODUCTION_CHECKLIST claims no worker/notifications, COMPONENT_ARCHITECTURE says worker not in scope).

Why it matters:
Misleading docs cause wrong security assumptions and wasted implementation effort.

Current workaround:
IMPLEMENTATION_ROADMAP and PRODUCT_REQUIREMENTS are more current.

Recommended fix:
Documentation cleanup pass to align module READMEs with Phase 27–29 state.

Suggested prompt:
Documentation Sync Pass (future)

---

## P3 — Cleanup and Future Enhancements

### TD-042: Redis configured but unused by core API paths

Category: Architecture  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/PRODUCTION_READINESS_CHECKLIST.md, docs/TECHNICAL_GUIDELINES.md, ADR  
Area: General

Description:
Redis is in Docker Compose but core API does not use it for cache, sessions or queues.

Why it matters:
Unused infrastructure adds ops surface without benefit until worker queue ships.

Current workaround:
Redis optional; API runs without it.

Recommended fix:
Use Redis when refresh tokens or job queue implemented; or remove from minimal deploy profile.

Suggested prompt:
Worker and Notification Reliability

---

### TD-043: Monorepo package coupling risk if boundaries ignored

Category: Architecture  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DECISION_LOG.md, docs/COMPONENT_ARCHITECTURE.md  
Area: General

Description:
Single-repo monolith is intentional but ADR notes tight coupling risk if `packages/` boundaries are bypassed.

Why it matters:
Long-term maintainability if teams grow.

Current workaround:
Documented dependency direction API → packages.

Recommended fix:
Periodic architecture review; lint import boundaries when pain appears.

Suggested prompt:
Architecture Review (future)

---

### TD-044: Manual TypeScript/Python type sharing (no codegen)

Category: DevEx  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DECISION_LOG.md, docs/TECHNICAL_GUIDELINES.md  
Area: General

Description:
Frontend types mirror backend schemas manually; drift possible on API changes.

Why it matters:
Subtle UI/API mismatches after schema updates.

Current workaround:
Disciplined parallel updates per feature; typecheck catches some issues.

Recommended fix:
OpenAPI codegen for types when API surface stabilizes.

Suggested prompt:
DevEx Tooling (OpenAPI codegen)

---

### TD-046: No Kubernetes manifests; Docker Compose reference only

Category: Operations  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DEPLOYMENT_GUIDELINES.md  
Area: General

Description:
MVP deployment is Docker-friendly; `docker-compose.prod.example.yml` is reference only. No K8s Helm charts.

Why it matters:
Enterprise ops teams may require K8s-native deploys at scale.

Current workaround:
Manual container deploy behind reverse proxy.

Recommended fix:
Add Helm chart when deployment target is chosen.

Suggested prompt:
Production Operations and Monitoring (K8s manifests)

---

### TD-047: Work board has no drag-and-drop

Category: UX  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DESIGN_GUIDELINES.md, apps/web/README.md, apps/web/src/features/work-items/README.md  
Area: General

Description:
Board status changes use explicit "Move to …" buttons per DESIGN_GUIDELINES MVP constraint.

Why it matters:
Lower interaction speed for power users.

Current workaround:
PATCH status via buttons; server-driven board refetch.

Recommended fix:
Add drag-and-drop with optimistic updates when pilot feedback demands it.

Suggested prompt:
Work Board UX Enhancement

---

### TD-048: Manual UUID fallbacks remain in advanced form sections

Category: UX  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DESIGN_GUIDELINES.md, apps/web/src/features/entity-picker/README.md  
Area: General

Description:
Collapsible "manual ID" sections allow UUID paste for edge cases (unsupported types, debugging).

Why it matters:
Power users ok; normal users should rarely see raw UUIDs.

Current workaround:
EntityPicker covers primary flows; advanced mode hidden.

Recommended fix:
Expand EntityPicker types rather than removing fallback.

Suggested prompt:
Entity Picker Expansion

---

### TD-049: Comments are plain text only (no rich text, mentions, attachments)

Category: UX  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, docs/DESIGN_GUIDELINES.md  
Area: General

Description:
Comments lack markdown, @mentions, attachments and notifications on reply.

Why it matters:
Collaboration depth limited vs modern tools.

Current workaround:
Plain-text comments with activity events.

Recommended fix:
Incremental rich text when collaboration becomes pilot priority.

Suggested prompt:
Collaboration Enhancement

---

### TD-050: Activity events use placeholder actors; `actor_id` optional

Category: Backend  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DATA_MODEL.md, docs/TECHNICAL_GUIDELINES.md, docs/DESIGN_GUIDELINES.md  
Area: General

Description:
Activity timeline may show "System" or short user id; not all services pass authenticated actor on mutations.

Why it matters:
Weaker accountability in activity feed (distinct from TD-007 audit trail).

Current workaround:
Partial actor wiring where auth context available.

Recommended fix:
Require actor from auth dependency in all write services.

Suggested prompt:
Activity Actor Wiring

---

### TD-051: No dedicated global search results page

Category: UX  
Severity: Low  
Priority: P3  
Status: Open  
Source: apps/web/README.md, docs/DESIGN_GUIDELINES.md  
Area: Search

Description:
Search is top-bar dropdown only; no `/search?q=` full results page.

Why it matters:
Harder to scan many results or share search links.

Current workaround:
Dropdown with navigate-on-click; Enter selects first result.

Recommended fix:
Add search results page with filters and pagination.

Suggested prompt:
Search UX Enhancement

---

### TD-052: No chart library; tables and badges only for metrics/dashboard

Category: UX  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DESIGN_GUIDELINES.md, docs/PRODUCT_REQUIREMENTS.md, apps/web/src/features/dashboard/README.md  
Area: Dashboard

Description:
MVP explicitly avoids chart libraries. Health visualization uses mini progress bars and tables.

Why it matters:
Leadership may want trend charts at scale.

Current workaround:
MiniProgressBar and MetricCard components.

Recommended fix:
Introduce chart library when metric time-series views are prioritized.

Suggested prompt:
Dashboard Performance Optimization (charts)

---

### TD-053: EntityLink types for governance entities not yet supported

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DATA_MODEL.md, docs/PRODUCT_REQUIREMENTS.md  
Area: General

Description:
Enum includes policy, rule, compliance_check link types but validation rejects them until modules mature.

Why it matters:
Relationship graph incomplete for governance objects.

Current workaround:
Compliance linked via dedicated check records, not EntityLink.

Recommended fix:
Enable types when compliance/relationship picker extended.

Suggested prompt:
Relationship Layer Extension

---

### TD-054: Target commercial/ops modules not implemented (deals, meetings, tools)

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/PRODUCT_REQUIREMENTS.md, apps/api/app/modules/deals/README.md, apps/api/README.md  
Area: General

Description:
Deals, pilots, MVPs, meetings, tools, reports, schedules, rules and policies modules are placeholders with README only.

Why it matters:
Full operating model vision not yet delivered; expected per roadmap.

Current workaround:
Project types cover poc/pilot/mvp via `project_type` discriminator.

Recommended fix:
Implement per IMPLEMENTATION_ROADMAP when prioritized.

Suggested prompt:
Commercial Pipeline Module (future)

---

### TD-055: No virus scanning or antivirus pipeline for files

Category: Security  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DATA_MODEL.md, inferred  
Area: Files

Description:
When upload arrives (TD-020), no scanning step is planned in MVP docs.

Why it matters:
Malware upload risk for internal file storage.

Current workaround:
External links only — user responsible for host security.

Recommended fix:
Integrate ClamAV or cloud scanning on upload path.

Suggested prompt:
File Handling and Storage Hardening (antivirus)

---

### TD-056: No notification digest or subscription preference engine

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/TECHNICAL_GUIDELINES.md, docs/PRODUCT_REQUIREMENTS.md  
Area: Notifications

Description:
Preferences exist per channel/event but no digest batching or smart subscription rules.

Why it matters:
Notification fatigue if external delivery enabled without digests.

Current workaround:
Per-message records; manual preference CRUD.

Recommended fix:
Add digest scheduler and unsubscribe tokens with external delivery.

Suggested prompt:
Worker and Notification Reliability (digests)

---

### TD-057: Dashboard health scores are transparent heuristics, not official KPIs

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DATA_MODEL.md, docs/PRODUCT_REQUIREMENTS.md, docs/DESIGN_GUIDELINES.md  
Area: Dashboard

Description:
Scoring formulas in `scoring.py` are explicit but not calibrated against business KPIs or compliance frameworks.

Why it matters:
Misinterpretation as official executive metrics.

Current workaround:
Documented as heuristics; empty insights message when none found.

Recommended fix:
Configurable weights and labels; disclaimer in UI.

Suggested prompt:
Dashboard Configuration (future)

---

### TD-058: No AI-generated insights or assistant layer

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/PROJECT_VISION.md, docs/PRODUCT_REQUIREMENTS.md, packages/core-ai/README.md  
Area: Dashboard

Description:
Actionable insights are deterministic rules only. AI assistant, summarization and embeddings deferred.

Why it matters:
Vision includes AI-ready structure but no AI features yet.

Current workaround:
Rule-based insights in `insights.py`.

Recommended fix:
Implement when data quality and audit foundation (TD-007) exist.

Suggested prompt:
AI Assistant Layer (future)

---

### TD-059: Skills, allocations and many-to-many team membership not modeled

Category: Product  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/DATA_MODEL.md, ADR-0012, apps/web/src/features/people/README.md  
Area: General

Description:
Target model includes Skill and Allocation entities; MVP uses single team/capability FKs.

Why it matters:
Capacity planning and skill matrix views unavailable.

Current workaround:
Primary team/capability and availability_percent field.

Recommended fix:
Phase dedicated organization expansion.

Suggested prompt:
Organization Model Expansion

---

### TD-060: `AUTH_ENABLED=false` dev bypass accepted in local/test only

Category: Security  
Severity: Low  
Priority: P3  
Status: Open  
Source: docs/LOCAL_TEST_AND_READINESS_REVIEW.md, docs/TECHNICAL_GUIDELINES.md  
Area: Auth

Description:
Auth can be disabled for local development and tests. Documented as acceptable but dangerous if mis-set in deploy.

Why it matters:
Accidental disable opens all endpoints.

Current workaround:
Production validator requires auth enabled in production-like envs (inferred from guidelines).

Recommended fix:
Hard-fail startup when `AUTH_ENABLED=false` and `APP_ENV=production`.

Suggested prompt:
Auth Security Hardening (startup guards)

---

## Recommended Fix Roadmap

Grouped prompts for planning next implementation work. Each prompt should reference related TD IDs above.

### Prompt TD-01: Tenant Isolation Hardening

**Related IDs:** TD-001, TD-003, TD-004, TD-008, TD-018, TD-038

Complete tenant scoping on all modules with `company_id`, enforce CompanyMember RBAC, per-company uniqueness, NOT NULL migration, multi-company UX and shared reference validation audit.

### Prompt TD-02: Auth Security Hardening

**Related IDs:** TD-005, TD-006, TD-013, TD-014, TD-015, TD-016, TD-017, TD-027, TD-060

Secure token storage, password reset and invites, rate limiting, optional SSO/MFA/sessions path, metrics ACL and production auth guards.

### Prompt TD-03: File Handling and Storage Hardening

**Related IDs:** TD-020, TD-021, TD-022, TD-055

Binary upload/download, storage provider integration, sensitivity policy enforcement and antivirus on upload.

### Prompt TD-04: Worker and Notification Reliability

**Related IDs:** TD-028, TD-029, TD-030, TD-031, TD-032, TD-042, TD-056, TD-024

External notification delivery, secret management, cron parser, optional Redis queue, safe webhooks, compliance job hooks and digests.

### Prompt TD-05: Dashboard Performance Optimization

**Related IDs:** TD-012, TD-033, TD-034, TD-035, TD-052

Frontend code-splitting, aggregated dashboard fetch, read-model caching, search upgrade and optional charts.

### Prompt TD-06: Production Operations and Monitoring

**Related IDs:** TD-002, TD-007, TD-009, TD-010, TD-011, TD-036, TD-040, TD-046, **TD-061**

Deploy guardrails, audit trail, monitoring/alerting, backup automation, CI integration tests, E2E smoke tests, rollback runbook, HTTPS/CORS production hardening and optional K8s manifests.

### Prompt TD-07: Import/Export Foundation

**Related IDs:** TD-019, TD-025

CSV/JSON export and import for core entities; compliance evidence export pack.

---

## Sources reviewed

| Path | Notes |
|------|-------|
| docs/PROJECT_VISION.md | Vision, AI-ready, manual exports |
| docs/PRODUCT_REQUIREMENTS.md | MVP vs target scope |
| docs/IMPLEMENTATION_ROADMAP.md | Phase status, Phase 30 planned |
| docs/COMPONENT_ARCHITECTURE.md | Stale worker/module status |
| docs/DATA_MODEL.md | Generic refs, audit, files, tenancy columns |
| docs/TECHNICAL_GUIDELINES.md | Tenancy, worker, compliance, search conventions |
| docs/DESIGN_GUIDELINES.md | MVP UX constraints |
| docs/SECURITY_GUIDELINES.md | Auth, tenant, notification security |
| docs/DEVELOPMENT_GUIDELINES.md | Seed, integration tests |
| docs/DEPLOYMENT_GUIDELINES.md | Backups, worker, HTTPS |
| docs/OPERATIONS_RUNBOOK.md | Worker locks, demo creds |
| docs/PRODUCTION_READINESS_CHECKLIST.md | Known MVP limitations (partially stale) |
| docs/LOCAL_TEST_AND_READINESS_REVIEW.md | **Security review source** — §4 findings, §6 production risks, §10 P0/P1/P2 |
| docs/DECISION_LOG.md | ADRs on auth, worker, tenancy |
| README.md | Demo, notifications future scope |
| apps/api/README.md | Module status, simulation |
| apps/web/README.md | Known limitations per feature |
| apps/api/app/modules/*/README.md | Module scope (31 files) |
| apps/web/src/features/*/README.md | Feature limitations (25 files) |
| apps/api/app/worker/README.md | Worker MVP design |
| .github/workflows/ci.yml | CI scope (no integration pytest) |

---

## Related documents

- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — feature phases and Technical Debt Roadmap section
- [PRODUCTION_READINESS_CHECKLIST.md](PRODUCTION_READINESS_CHECKLIST.md)
- [LOCAL_TEST_AND_READINESS_REVIEW.md](LOCAL_TEST_AND_READINESS_REVIEW.md)
- [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md)
