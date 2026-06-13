import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import NotificationChannelType
from app.modules.notifications.dispatcher import NotificationDispatcher


@pytest.mark.asyncio
async def test_dispatcher_simulate_does_not_call_external_provider() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    channel = MagicMock()
    channel.channel_type = NotificationChannelType.EMAIL.value
    channel.default_recipient = "team@example.com"

    message = MagicMock()
    message.id = uuid.uuid4()
    message.channel = channel
    message.recipient_value = "user@example.com"
    message.subject = "Test"
    message.body = "Body"
    message.delivery_attempts = []

    dispatcher = NotificationDispatcher()
    result = await dispatcher.send_message(session, message, simulate=True)

    assert result.simulated is True
    assert result.message.status == "simulated"
    assert result.delivery_attempt.status == "simulated"
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_dispatcher_external_non_simulated_fails_safely() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    channel = MagicMock()
    channel.channel_type = NotificationChannelType.EMAIL.value
    channel.default_recipient = None

    message = MagicMock()
    message.id = uuid.uuid4()
    message.channel = channel
    message.recipient_value = "user@example.com"
    message.subject = "Test"
    message.body = "Body"
    message.delivery_attempts = []

    dispatcher = NotificationDispatcher()
    result = await dispatcher.send_message(session, message, simulate=False)

    assert "not implemented" in result.result_summary.lower()
    assert result.message.status == "failed"
    assert result.delivery_attempt.status == "failed"
