# Automation Feature

Schedules, triggers, manual runs and entity-linked automation sections.

## Routes

- `/automation` — overview, triggers, schedules, recent runs
- `/automation/triggers/new` — create trigger (supports `?target_type=&target_id=`)
- `/automation/triggers/:id` — trigger detail and run history
- `/automation/triggers/:id/edit` — edit trigger
- `/automation/schedules/new` — create schedule
- `/automation/schedules/:id/edit` — edit schedule

## AutomationSection

Embedded on entity detail pages for data products, work items, projects, internal projects, teams, capabilities and compliance checks.

## MVP limitations

- No background worker or cron execution
- Real runs limited to safe actions: create work item, add comment, create activity event
- Simulation is the default manual run mode
