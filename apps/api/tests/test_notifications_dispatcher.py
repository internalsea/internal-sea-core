import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.config import get_settings
from app.domain.enums import NotificationChannelType, NotificationMessageStatus
from app.modules.notifications.dispatcher import NotificationDispatcher


def _build_message() -> MagicMock:
    now = datetime.now(UTC)
    channel = MagicMock()
    channel.channel_type = NotificationChannelType.EMAIL.value
    channel.default_recipient = "team@example.com"

    message = MagicMock()
    message.id = uuid.uuid4()
    message.channel_id = uuid.uuid4()
    message.template_id = None
    message.status = NotificationMessageStatus.QUEUED.value
    message.priority = "normal"
    message.event_type = "test.event"
    message.subject = "Test"
    message.body = "Body"
    message.recipient_type = "email"
    message.recipient_value = "user@example.com"
    message.entity_type = None
    message.entity_id = None
    message.automation_run_id = None
    message.created_by_id = None
    message.scheduled_at = None
    message.sent_at = None
    message.simulated_at = None
    message.error_message = None
    message.message_metadata = None
    message.created_at = now
    message.updated_at = now
    message.channel = channel
    message.delivery_attempts = []
    return message


@pytest.mark.asyncio
async def test_dispatcher_simulate_does_not_call_external_provider() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    message = _build_message()

    dispatcher = NotificationDispatcher()
    result = await dispatcher.send_message(session, message, simulate=True)

    assert result.simulated is True
    assert result.message.status == "simulated"
    assert result.delivery_attempt.status == "simulated"
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_dispatcher_external_non_simulated_fails_safely(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NOTIFICATION_WORKER_SIMULATE_EXTERNAL", "false")
    monkeypatch.setenv("NOTIFICATION_EXTERNAL_DELIVERY_ENABLED", "false")
    get_settings.cache_clear()

    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    message = _build_message()
    message.channel.default_recipient = None

    dispatcher = NotificationDispatcher()
    result = await dispatcher.send_message(session, message, simulate=False)

    assert "not implemented" in result.result_summary.lower()
    assert result.message.status == "failed"
    assert result.delivery_attempt.status == "failed"
