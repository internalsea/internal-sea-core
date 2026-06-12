# Background Worker

Optional separate process for scheduled automation and queued notification delivery.

## Commands

```bash
# One batch (automation triggers + queued notifications)
uv run python -m app.worker.main run-once

# Continuous loop
uv run python -m app.worker.main run-loop --interval 30
```

## Configuration

See root `.env.example` for `WORKER_*`, `AUTOMATION_*`, and `NOTIFICATION_*` settings.

## Design

- PostgreSQL is the source of truth; no external queue in MVP.
- Simple row-level locks (`locked_at`, `locked_by`, `lock_expires_at`) prevent duplicate processing.
- Worker actions use safe MVP automation paths only; external delivery remains simulated by default.
- API can trigger a single cycle via `POST /api/v1/worker/run-once` (editor/admin).

## Scaling

Run one worker instance initially. Multiple workers are safe for different rows but not optimized for high volume. Future prompts may add Redis/Celery or similar.
