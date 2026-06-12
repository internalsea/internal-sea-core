# Tenancy (frontend)

SaaS multi-tenant context for Internal Sea: company, workspace, and membership.

- **`types.ts`** — mirrors backend tenancy schemas and enums
- **`api.ts`** — `/tenancy/*` REST client
- **`hooks.ts`** — React Query hooks for tenant data and mutations
- **`utils.ts`** — `internal_sea_core_company_id` / `internal_sea_core_workspace_id` localStorage helpers

Tenant IDs are sent on API requests via `X-Company-ID` and `X-Workspace-ID` (see `lib/apiClient.ts`). `TenancyProvider` loads `/tenancy/current` after authentication and keeps context in sync.
