"""Simple safe placeholder template rendering.

Supports only ``{{key}}`` placeholders. Missing keys are replaced with an
empty string. No code execution, loops, or filters.
"""

from __future__ import annotations

import re
from typing import Any

from app.models.notifications import NotificationTemplate

PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

DEFAULT_CONTEXT_KEYS = (
    "app_name",
    "entity_type",
    "entity_id",
    "title",
    "status",
    "event_type",
)


def render_template_string(template: str, context: dict[str, Any] | None) -> str:
    """Replace ``{{key}}`` placeholders with stringified context values."""
    ctx = context or {}

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = ctx.get(key)
        if value is None:
            return ""
        return str(value)

    return PLACEHOLDER_PATTERN.sub(replace, template)


def render_notification_template(
    template: NotificationTemplate,
    context: dict[str, Any] | None = None,
) -> tuple[str | None, str]:
    subject = (
        render_template_string(template.subject_template, context)
        if template.subject_template
        else None
    )
    body = render_template_string(template.body_template, context)
    return subject, body
