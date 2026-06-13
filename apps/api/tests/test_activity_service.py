import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import ActivityAction, ActivityEntityType
from app.modules.activity.helpers import get_updated_fields
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService


@pytest.mark.asyncio
async def test_service_records_event_with_expected_data() -> None:
    repository = AsyncMock()
    entity_id = uuid.uuid4()
    now = datetime.now(UTC)
    event = MagicMock()
    event.id = uuid.uuid4()
    event.entity_type = ActivityEntityType.WORK_ITEM.value
    event.entity_id = entity_id
    event.action = ActivityAction.CREATED.value
    event.actor_id = None
    event.title = "Work item created"
    event.description = None
    event.details = None
    event.created_at = now
    repository.create.return_value = event

    service = ActivityService(repository)
    payload = ActivityEventCreateInternal(
        entity_type=ActivityEntityType.WORK_ITEM,
        entity_id=entity_id,
        action=ActivityAction.CREATED,
        title="Work item created",
    )
    result = await service.record_event(payload)

    repository.create.assert_awaited_once_with(payload)
    assert result.entity_type == ActivityEntityType.WORK_ITEM
    assert result.action == ActivityAction.CREATED
    assert result.title == "Work item created"


def test_get_updated_fields_helper() -> None:
    assert get_updated_fields({"status": "active", "name": "Test"}) == ["name", "status"]
