import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import NotificationChannelType, NotificationEventType
from app.modules.notifications.errors import NotificationConflictError
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import NotificationPreferenceCreate
from app.modules.notifications.service import NotificationService


@pytest.mark.asyncio
async def test_preference_duplicate_raises_conflict() -> None:
    repository = AsyncMock(spec=NotificationRepository)
    repository.get_duplicate_preference = AsyncMock(return_value=MagicMock())
    session = AsyncMock()
    session.get = AsyncMock(return_value=MagicMock())
    service = NotificationService(repository, AsyncMock(), session)

    with pytest.raises(NotificationConflictError):
        await service.create_preference(
            NotificationPreferenceCreate(
                user_id=uuid.uuid4(),
                channel_type=NotificationChannelType.IN_APP,
                event_type=NotificationEventType.MANUAL,
            )
        )
