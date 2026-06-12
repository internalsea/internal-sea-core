# Auth Module

JWT bearer authentication with email/password login and role-based access control.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | Public | Login and receive access token |
| GET | `/auth/me` | User | Current user profile |
| POST | `/auth/logout` | User | Client-side logout acknowledgement |
| GET | `/auth/users` | Admin | List users |
| POST | `/auth/users` | Admin | Create user |
| GET | `/auth/users/{id}` | Admin | Get user |
| PATCH | `/auth/users/{id}` | Admin | Update user |
| DELETE | `/auth/users/{id}` | Admin | Deactivate user |

## Roles

| Role | Read | Write business objects | Manage users |
|------|------|------------------------|--------------|
| viewer | Yes | No | No |
| editor | Yes | Yes | No |
| admin | Yes | Yes | Yes |
| superuser | Bypass | Bypass | Bypass |

## Demo users (local seed)

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin12345 | admin |
| editor@example.com | editor12345 | editor |
| viewer@example.com | viewer12345 | viewer |

## Configuration

- `JWT_SECRET_KEY` — required in production
- `AUTH_ENABLED=false` — bypasses auth for local/tests (returns dev admin user)
