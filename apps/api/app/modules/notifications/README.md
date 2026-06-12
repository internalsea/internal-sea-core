# Notifications module

MVP notification foundation: channels, templates, preferences, messages and delivery attempts.

## Scope

- Simulation-first sending (default `simulate=true`)
- Simple `{{placeholder}}` template rendering
- In-app delivery records when not simulating on in-app channels
- No external email, Teams, Slack or webhook calls
- No background delivery worker
- `provider_config` must not store secrets in plain text

## Key files

- `dispatcher.py` — safe send/simulate logic
- `renderer.py` — placeholder template rendering
- `validators.py` — entity and reference validation
