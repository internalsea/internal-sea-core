# Notifications feature

MVP notification UI: channels, templates, messages, preferences and simulated sending.

## Routes

- `/notifications` — overview and management
- `/notifications/templates/*` — template CRUD and preview
- `/notifications/messages/*` — message CRUD and send simulation

## Components

- `NotificationsSection` — embed on entity detail pages
- `SendNotificationDialog` — simulation-first send flow

External email/Teams/Slack delivery is not implemented in MVP.
