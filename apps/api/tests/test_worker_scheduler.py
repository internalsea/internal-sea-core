from datetime import UTC, datetime
from unittest.mock import MagicMock

from app.worker.scheduler import calculate_next_run_at


def _schedule(frequency: str, next_run_at=None):
    schedule = MagicMock()
    schedule.frequency = frequency
    schedule.next_run_at = next_run_at
    return schedule


def test_calculate_next_run_at_daily() -> None:
    base = datetime(2026, 6, 12, 10, 0, tzinfo=UTC)
    result = calculate_next_run_at(_schedule("daily"), base)
    assert result == datetime(2026, 6, 13, 10, 0, tzinfo=UTC)


def test_calculate_next_run_at_weekly() -> None:
    base = datetime(2026, 6, 12, 10, 0, tzinfo=UTC)
    result = calculate_next_run_at(_schedule("weekly"), base)
    assert result == datetime(2026, 6, 19, 10, 0, tzinfo=UTC)


def test_calculate_next_run_at_monthly() -> None:
    base = datetime(2026, 6, 12, 10, 0, tzinfo=UTC)
    result = calculate_next_run_at(_schedule("monthly"), base)
    assert result == datetime(2026, 7, 12, 10, 0, tzinfo=UTC)


def test_calculate_next_run_at_once_returns_none() -> None:
    base = datetime(2026, 6, 12, 10, 0, tzinfo=UTC)
    assert calculate_next_run_at(_schedule("once"), base) is None


def test_calculate_next_run_at_custom_keeps_existing() -> None:
    base = datetime(2026, 6, 12, 10, 0, tzinfo=UTC)
    existing = datetime(2026, 7, 1, 8, 0, tzinfo=UTC)
    assert calculate_next_run_at(_schedule("custom", existing), base) == existing


def test_worker_cycle_result_schema() -> None:
    from app.worker.schemas import WorkerCycleResult

    now = datetime.now(UTC)
    result = WorkerCycleResult(
        worker_instance_id="test-worker",
        started_at=now,
        finished_at=now,
        due_triggers_found=1,
        automation_runs_created=1,
        notification_messages_found=2,
        notifications_processed=1,
        failures=[],
        summary="ok",
    )
    assert result.automation_runs_created == 1
