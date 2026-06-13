import uuid
from datetime import UTC, datetime, timedelta

import pytest
from app.domain.enums import (
    AutomationActionType,
    AutomationStatus,
    AutomationTargetType,
    AutomationTriggerType,
    ScheduleFrequency,
)
from app.modules.automation.schemas import (
    AutomationScheduleCreate,
    AutomationScheduleUpdate,
    AutomationTriggerCreate,
)
from pydantic import ValidationError


def test_automation_schedule_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        AutomationScheduleCreate(name="   ", frequency=ScheduleFrequency.MONTHLY)


def test_schedule_date_validation_rejects_end_before_start() -> None:
    start = datetime.now(UTC)
    end = start - timedelta(days=1)
    with pytest.raises(ValidationError):
        AutomationScheduleCreate(
            name="Monthly Review",
            start_at=start,
            end_at=end,
        )


def test_schedule_cron_only_with_custom_frequency() -> None:
    with pytest.raises(ValidationError):
        AutomationScheduleCreate(
            name="Custom",
            frequency=ScheduleFrequency.MONTHLY,
            cron_expression="0 0 * * *",
        )


def test_automation_trigger_create_accepts_valid_schedule_trigger() -> None:
    schedule_id = uuid.uuid4()
    trigger = AutomationTriggerCreate(
        name="Review dashboard",
        status=AutomationStatus.ACTIVE,
        trigger_type=AutomationTriggerType.SCHEDULE,
        action_type=AutomationActionType.CREATE_WORK_ITEM,
        schedule_id=schedule_id,
        target_type=AutomationTargetType.DATA_PRODUCT,
        target_id=uuid.uuid4(),
        action_config={"title": "Review"},
    )
    assert trigger.schedule_id == schedule_id


def test_automation_trigger_requires_target_pair() -> None:
    with pytest.raises(ValidationError):
        AutomationTriggerCreate(
            name="Invalid",
            action_type=AutomationActionType.ADD_COMMENT,
            target_type=AutomationTargetType.DATA_PRODUCT,
        )


def test_automation_schedule_update_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        AutomationScheduleUpdate(name="  ")
