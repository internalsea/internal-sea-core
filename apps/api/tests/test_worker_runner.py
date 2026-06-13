import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.worker.runner import WorkerRunner


@pytest.mark.asyncio
async def test_worker_runner_passes_worker_instance_id_to_automation() -> None:
    session = AsyncMock()
    trigger = MagicMock()
    trigger.id = uuid.uuid4()
    trigger.schedule_id = None
    trigger.action_type = "create_work_item"

    with (
        patch("app.worker.runner.find_due_automation_triggers", AsyncMock(return_value=[trigger])),
        patch("app.worker.runner.find_due_notification_messages", AsyncMock(return_value=[])),
        patch("app.worker.runner.acquire_automation_trigger_lock", AsyncMock(return_value=True)),
        patch("app.worker.runner.release_automation_trigger_lock", AsyncMock()),
        patch("app.worker.runner.update_trigger_next_run", AsyncMock()),
    ):
        runner = WorkerRunner(session, instance_id="test-worker", batch_size=5)
        mock_result = MagicMock()
        mock_result.run.finished_at = datetime.now(UTC)
        runner._automation_runner.run_trigger = AsyncMock(return_value=mock_result)

        result = await runner.run_once()

        runner._automation_runner.run_trigger.assert_awaited_once()
        call_kwargs = runner._automation_runner.run_trigger.await_args.kwargs
        assert call_kwargs["worker_instance_id"] == "test-worker"
        assert result.worker_instance_id == "test-worker"


@pytest.mark.asyncio
async def test_worker_runner_processes_notifications_with_worker_id() -> None:
    session = AsyncMock()
    message_id = uuid.uuid4()
    message = MagicMock(id=message_id)

    with (
        patch(
            "app.worker.runner.find_due_notification_messages",
            AsyncMock(return_value=[message]),
        ),
        patch(
            "app.worker.runner.acquire_notification_message_lock",
            AsyncMock(return_value=True),
        ),
        patch("app.worker.runner.release_notification_message_lock", AsyncMock()),
    ):
        runner = WorkerRunner(session, instance_id="notify-worker", batch_size=5)
        runner._notification_service.process_queued_message = AsyncMock()
        processed = await runner.process_due_notifications()

    runner._notification_service.process_queued_message.assert_awaited_once_with(
        message_id,
        worker_instance_id="notify-worker",
    )
    assert processed == 1
