import uuid
from datetime import UTC
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import AutomationActionType, AutomationTargetType
from app.modules.automation.errors import (
    AutomationScheduleNotFoundError,
    AutomationTriggerNotFoundError,
)
from app.modules.automation.schemas import (
    AutomationRunRequest,
    AutomationScheduleCreate,
)
from app.modules.automation.service import AutomationService


@pytest.fixture
def service() -> tuple[AutomationService, AsyncMock]:
    repository = AsyncMock()
    activity = AsyncMock()
    session = AsyncMock()
    svc = AutomationService(repository, activity, session)
    return svc, repository


@pytest.mark.asyncio
async def test_get_schedule_not_found(service: tuple[AutomationService, AsyncMock]) -> None:
    svc, repository = service
    repository.get_schedule_by_id.return_value = None
    with pytest.raises(AutomationScheduleNotFoundError):
        await svc.get_schedule(uuid.uuid4())


@pytest.mark.asyncio
async def test_get_trigger_not_found(service: tuple[AutomationService, AsyncMock]) -> None:
    svc, repository = service
    repository.get_trigger_by_id.return_value = None
    with pytest.raises(AutomationTriggerNotFoundError):
        await svc.get_trigger(uuid.uuid4())


@pytest.mark.asyncio
async def test_run_trigger_not_found(service: tuple[AutomationService, AsyncMock]) -> None:
    svc, repository = service
    repository.get_trigger_by_id.return_value = None
    with pytest.raises(AutomationTriggerNotFoundError):
        await svc.run_trigger(uuid.uuid4(), AutomationRunRequest(simulate=True))


@pytest.mark.asyncio
async def test_create_schedule(service: tuple[AutomationService, AsyncMock]) -> None:
    svc, repository = service
    schedule = MagicMock()
    schedule.id = uuid.uuid4()
    schedule.name = "Monthly"
    schedule.description = None
    schedule.frequency = "monthly"
    schedule.timezone = "UTC"
    schedule.start_at = None
    schedule.end_at = None
    schedule.next_run_at = None
    schedule.last_run_at = None
    schedule.cron_expression = None
    schedule.is_active = True
    schedule.created_by_id = None
    from datetime import datetime

    schedule.created_at = datetime.now(UTC)
    schedule.updated_at = datetime.now(UTC)
    repository.create_schedule.return_value = schedule

    result = await svc.create_schedule(AutomationScheduleCreate(name="Monthly"))
    assert result.name == "Monthly"


@pytest.mark.asyncio
async def test_run_trigger_delegates_to_runner(
    service: tuple[AutomationService, AsyncMock],
) -> None:
    svc, repository = service
    trigger = MagicMock()
    trigger.id = uuid.uuid4()
    trigger.name = "T"
    trigger.target_type = AutomationTargetType.DATA_PRODUCT.value
    trigger.target_id = uuid.uuid4()
    trigger.action_type = AutomationActionType.CREATE_WORK_ITEM.value
    repository.get_trigger_by_id.return_value = trigger

    from datetime import datetime

    from app.modules.automation.schemas import AutomationRunRead, AutomationRunResult

    now = datetime.now(UTC)
    run_result = AutomationRunResult(
        run=AutomationRunRead(
            id=uuid.uuid4(),
            trigger_id=trigger.id,
            status="simulated",
            started_at=now,
            finished_at=now,
            target_type="data_product",
            target_id=trigger.target_id,
            action_type="create_work_item",
            result_summary="ok",
            result_details=None,
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        ),
        message="done",
    )
    svc._runner.run_trigger = AsyncMock(return_value=run_result)  # type: ignore[method-assign]

    result = await svc.run_trigger(trigger.id, AutomationRunRequest(simulate=True))
    assert result.run.status == "simulated"
