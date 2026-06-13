import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.domain.enums import AutomationActionType, AutomationRunStatus, AutomationTargetType
from app.modules.automation.runner import AutomationRunner


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


def _make_run_mock(
    *,
    run_id: uuid.UUID,
    trigger_id: uuid.UUID,
    now: datetime,
    status: str,
    **overrides: object,
) -> MagicMock:
    return MagicMock(
        id=run_id,
        trigger_id=trigger_id,
        status=status,
        started_at=now,
        finished_at=overrides.get("finished_at"),
        target_type=overrides.get("target_type", "data_product"),
        target_id=overrides.get("target_id", uuid.uuid4()),
        action_type=overrides.get("action_type", "create_work_item"),
        result_summary=overrides.get("result_summary"),
        result_details=overrides.get("result_details"),
        error_message=overrides.get("error_message"),
        executed_by_id=overrides.get("executed_by_id"),
        worker_instance_id=overrides.get("worker_instance_id"),
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_run_simulate_returns_simulated_status() -> None:
    session = AsyncMock()
    repository = AsyncMock()
    now = datetime.now(UTC)
    run_id = uuid.uuid4()
    repository.create_run = AsyncMock(
        return_value=_make_run_mock(
            run_id=run_id,
            trigger_id=uuid.uuid4(),
            now=now,
            status=AutomationRunStatus.RUNNING.value,
        )
    )
    repository.update_run = AsyncMock(
        side_effect=lambda run, data: _make_run_mock(
            run_id=run_id,
            trigger_id=run.trigger_id if hasattr(run, "trigger_id") else uuid.uuid4(),
            now=now,
            status=data.get("status", AutomationRunStatus.SIMULATED.value),
            finished_at=data.get("finished_at"),
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            error_message=data.get("error_message"),
            worker_instance_id=None,
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
    now = datetime.now(UTC)
    run_id = uuid.uuid4()
    repository.create_run = AsyncMock(
        return_value=_make_run_mock(
            run_id=run_id,
            trigger_id=uuid.uuid4(),
            now=now,
            status=AutomationRunStatus.RUNNING.value,
            action_type="send_notification",
        )
    )
    repository.update_run = AsyncMock(
        side_effect=lambda run, data: _make_run_mock(
            run_id=run_id,
            trigger_id=uuid.uuid4(),
            now=now,
            status=data["status"],
            finished_at=data.get("finished_at"),
            action_type="send_notification",
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            error_message=data.get("error_message"),
            worker_instance_id=None,
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
    now = datetime.now(UTC)
    work_item_id = uuid.uuid4()
    run_id = uuid.uuid4()

    async def fake_commit():
        return None

    session.commit = AsyncMock(side_effect=fake_commit)
    session.refresh = AsyncMock()
    session.add = MagicMock()

    repository.create_run = AsyncMock(
        return_value=_make_run_mock(
            run_id=run_id,
            trigger_id=uuid.uuid4(),
            now=now,
            status=AutomationRunStatus.RUNNING.value,
        )
    )

    def update_run_side_effect(run, data):
        return _make_run_mock(
            run_id=run_id,
            trigger_id=uuid.uuid4(),
            now=now,
            status=data["status"],
            finished_at=data.get("finished_at"),
            result_summary=data.get("result_summary"),
            result_details=data.get("result_details"),
            worker_instance_id=None,
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
