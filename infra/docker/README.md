# Docker Infrastructure

This folder will contain Docker-related assets for Internal Sea beyond the root `docker-compose.yml`.

Planned contents (later phases):

- Dockerfiles for `apps/api` and `apps/web`
- Production-oriented Compose overrides
- Init scripts or seed containers if needed

For local development, use the root `docker-compose.yml` to start Postgres and Redis:

```bash
make docker-up
```

See [docs/IMPLEMENTATION_ROADMAP.md](../../docs/IMPLEMENTATION_ROADMAP.md) Phase 3 for API container wiring.
