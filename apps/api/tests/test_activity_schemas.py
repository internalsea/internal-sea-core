import uuid
from datetime import UTC, datetime

from app.domain.enums import ActivityAction, ActivityEntityType
from app.modules.activity.schemas import ActivityEventRead


def test_activity_event_read_schema_works() -> None:
    event_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    now = datetime.now(UTC)
    event = ActivityEventRead(
        id=event_id,
        entity_type=ActivityEntityType.DATA_PRODUCT,
        entity_id=entity_id,
        action=ActivityAction.CREATED,
        actor_id=None,
        title="Data product created",
        description=None,
        details=None,
        created_at=now,
    )
    assert event.id == event_id
    assert event.entity_type == ActivityEntityType.DATA_PRODUCT
    assert event.action == ActivityAction.CREATED
