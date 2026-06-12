# Tenancy Module

SaaS tenant hierarchy: Company, Workspace and CompanyMember.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/tenancy/onboarding/first-user` | Public | First user creates company, workspace and owner membership |
| GET | `/tenancy/current` | User | Current company/workspace/member context |
| GET | `/tenancy/companies` | User | Companies the current user belongs to |
| POST | `/tenancy/companies` | User | Create company with owner membership |
| GET/PATCH | `/tenancy/companies/{id}` | User / Admin+ | Company read/update |
| GET/POST | `/tenancy/companies/{id}/workspaces` | User / Admin+ | Workspace list/create |
| GET/PATCH | `/tenancy/workspaces/{id}` | User / Admin+ | Workspace read/update |
| GET/POST | `/tenancy/companies/{id}/members` | User / Admin+ | Member list/add |
| PATCH/DELETE | `/tenancy/members/{id}` | Admin+ | Update/remove member |

## Headers

- `X-Company-ID` — select company when user belongs to multiple
- `X-Workspace-ID` — select workspace (defaults to first active workspace)

## Roles

Company roles: owner, admin, editor, viewer. Global `User.role` remains as fallback for legacy endpoints.
