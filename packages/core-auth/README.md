# core-auth

Authentication and authorization package for Internal Sea.

This package will contain:

- JWT creation and validation helpers
- Password hashing utilities (if local accounts are used)
- Role and permission checks for RBAC
- Dependencies usable from FastAPI routes

SSO integration may wrap or replace parts of this layer later. See [docs/SECURITY_GUIDELINES.md](../../docs/SECURITY_GUIDELINES.md).

Implementation begins after the backend foundation (Phase 2+).
