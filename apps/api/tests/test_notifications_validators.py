import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.notifications.errors import UnsupportedNotificationEntityTypeError
from app.modules.notifications.validators import (
    is_supported_notification_entity_type,
    validate_notification_entity_exists,
)


def test_supported_entity_types() -> None:
    assert is_supported_notification_entity_type("data_product")
    assert not is_supported_notification_entity_type("unknown_type")


@pytest.mark.asyncio
async def test_unsupported_entity_type_raises() -> None:
    session = AsyncMock()
    with pytest.raises(UnsupportedNotificationEntityTypeError):
        await validate_notification_entity_exists(session, "unknown_type", uuid.uuid4())


@pytest.mark.asyncio
async def test_validate_entity_exists_when_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    from app.modules.notifications.errors import NotificationEntityNotFoundError

    with pytest.raises(NotificationEntityNotFoundError):
        await validate_notification_entity_exists(session, "data_product", uuid.uuid4())
