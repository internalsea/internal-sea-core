# Automation Module

Schedules, triggers and manual safe execution for Internal Sea.

## Scope (MVP)

- `AutomationSchedule` — recurrence definition (stored, not executed automatically yet)
- `AutomationTrigger` — condition, action and target binding
- `AutomationRun` — execution history
- Manual run with simulation (default) or safe real actions

## Safe action types

- `create_work_item`
- `add_comment`
- `create_activity_event`

Other action types exist in enums but are skipped or rejected on real runs.

## API

Base path: `/api/v1/automation`

See root `README.md` for curl examples.

## Future

- Background worker using `next_run_at`
- Notifications, webhooks, AI tool actions
- Cron execution
