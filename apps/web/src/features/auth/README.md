# Auth Feature

JWT bearer authentication with login, session bootstrap and role-based UI gating.

## Routes

| Route | Access |
|-------|--------|
| `/login` | Public |
| All other app routes | Authenticated users only |

## Token storage

Access token is stored in `localStorage` under `internal_sea_core_access_token` for MVP. Production should use secure cookies or session storage strategy.

## Hooks

- `useAuth()` — user, login, logout, canWrite, canAdmin
- `useCanWrite()` — editor/admin/superuser
- `useCanAdmin()` — admin/superuser

## Components

- `ProtectedRoute` — redirects unauthenticated users to `/login`
- `PermissionGate` — hides children when role insufficient
- `CurrentUserMenu` — top bar user display and logout

## Demo credentials

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin12345 | admin |
| editor@example.com | editor12345 | editor |
| viewer@example.com | viewer12345 | viewer |
