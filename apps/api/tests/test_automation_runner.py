import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.domain.enums import AutomationActionType, AutomationRunStatus, AutomationTargetType
from app.modules.automation.runner import AutomationRunner
from app.modules.automation.schemas import AutomationRunRead


def _make_trigger(**overrides):
    trigger = MagicMock()
    trigger.id = uuid.uuid4()
    trigger.name = "Test Trigger"
    trigger.action_type = AutomationActionType.CREATE_WORK_ITEM.value
    trigger.target_type = AutomationTargetType.DATA_PRODUCT.value
    trigger.target_id = uuid.uuid4()
    trigger.action_config = {}
    trigger.schedule_id = None
    for key, value in overrides.items():
        setattr(trigger, key, value)
    return trigger


@pytest.mark.asyncio
async def test_run_simulate_returns_simulated_status() -> None:
    session = AsyncMock()
    repository = AsyncMock()
    now = datetime.now(timezone.utc)
    run_id = uuid.uuid4()
    repository.create_run = AsyncMock(
        return_value=MagicMock(
            id=run_id,
            trigger_id=uuid.uuid4(),
            status=AutomationRunStatus.RUNNING.value,
            started_at=now,
            finished_at=None,
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="create_work_item",
            result_summary=None,
            result_details=None,
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    repository.update_run = AsyncMock(
        side_effect=lambda run, data: MagicMock(
            id=run_id,
            trigger_id=run.trigger_id if hasattr(run, "trigger_id") else uuid.uuid4(),
            status=data.get("status", AutomationRunStatus.SIMULATED.value),
            started_at=now,
            finished_at=data.get("finished_at"),
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="create_work_item",
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            error_message=data.get("error_message"),
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    repository.touch_trigger_run_times = AsyncMock()
    runner = AutomationRunner(session, repository)
    trigger = _make_trigger()

    result = await runner.run_trigger(trigger, executed_by_id=None, simulate=True)

    assert result.run.status == AutomationRunStatus.SIMULATED.value
    assert result.created_work_item_id is None
    assert "Simulation" in result.message


@pytest.mark.asyncio
async def test_unsupported_action_type_returns_skipped() -> None:
    session = AsyncMock()
    repository = AsyncMock()
    now = datetime.now(timezone.utc)
    run_id = uuid.uuid4()
    repository.create_run = AsyncMock(
        return_value=MagicMock(
            id=run_id,
            trigger_id=uuid.uuid4(),
            status=AutomationRunStatus.RUNNING.value,
            started_at=now,
            finished_at=None,
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="send_notification",
            result_summary=None,
            result_details=None,
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    repository.update_run = AsyncMock(
        side_effect=lambda run, data: MagicMock(
            id=run_id,
            trigger_id=uuid.uuid4(),
            status=data["status"],
            started_at=now,
            finished_at=data.get("finished_at"),
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="send_notification",
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            error_message=data.get("error_message"),
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    repository.touch_trigger_run_times = AsyncMock()
    runner = AutomationRunner(session, repository)
    trigger = _make_trigger(action_type=AutomationActionType.CREATE_COMPLIANCE_CHECK.value)

    result = await runner.run_trigger(trigger, executed_by_id=None, simulate=False)

    assert result.run.status == AutomationRunStatus.SKIPPED.value
    assert "not implemented" in result.message.lower()


@pytest.mark.asyncio
async def test_create_work_item_uses_defaults() -> None:
    session = AsyncMock()
    repository = AsyncMock()
    now = datetime.now(timezone.utc)
    work_item_id = uuid.uuid4()
    run_id = uuid.uuid4()

    async def fake_commit():
        return None

    session.commit = AsyncMock(side_effect=fake_commit)
    session.refresh = AsyncMock()
    session.add = MagicMock()

    repository.create_run = AsyncMock(
        return_value=MagicMock(
            id=run_id,
            trigger_id=uuid.uuid4(),
            status=AutomationRunStatus.RUNNING.value,
            started_at=now,
            finished_at=None,
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="create_work_item",
            result_summary=None,
            result_details=None,
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )
    )

    def update_run_side_effect(run, data):
        return MagicMock(
            id=run_id,
            trigger_id=uuid.uuid4(),
            status=data["status"],
            started_at=now,
            finished_at=data.get("finished_at"),
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="create_work_item",
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        )

    repository.update_run = AsyncMock(side_effect=update_run_side_effect)
    repository.touch_trigger_run_times = AsyncMock()

    with patch("app.modules.automation.runner.WorkItem") as work_item_cls:
        work_item_instance = MagicMock()
        work_item_instance.id = work_item_id
        work_item_instance.title = "Automation task: Test Trigger"
        work_item_cls.return_value = work_item_instance

        runner = AutomationRunner(session, repository)
        trigger = _make_trigger(action_config={})
        result = await runner.run_trigger(trigger, executed_by_id=None, simulate=False)

    assert result.run.status == AutomationRunStatus.SUCCEEDED.value
    assert result.created_work_item_id == work_item_id
    work_item_cls.assert_called_once()
