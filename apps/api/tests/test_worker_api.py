from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.worker.schemas import DueWorkSummary, WorkerCycleResult, WorkerStatus


class _MockWorkerRunner:
    def __init__(self, db) -> None:
        self.db = db

    async def run_once(self) -> WorkerCycleResult:
        now = datetime.now(timezone.utc)
        return WorkerCycleResult(
            worker_instance_id="local-worker",
            started_at=now,
            finished_at=now,
            due_triggers_found=1,
            automation_runs_created=1,
            notification_messages_found=1,
            notifications_processed=1,
            failures=[],
            summary="Worker cycle complete",
        )


@pytest.fixture
def mock_worker_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.modules.worker.router.get_worker_status",
        AsyncMock(
            return_value=WorkerStatus(
                worker_enabled=False,
                worker_instance_id="local-worker",
                poll_interval_seconds=30,
                batch_size=10,
                automation_due_count=2,
                notification_due_count=1,
                last_checked_at=datetime.now(timezone.utc),
            )
        ),
    )
    monkeypatch.setattr(
        "app.modules.worker.router.get_due_work_summary",
        AsyncMock(
            return_value=DueWorkSummary(
                due_automation_triggers=2,
                due_notifications=1,
                locked_automation_triggers=0,
                locked_notifications=0,
            )
        ),
    )
    monkeypatch.setattr("app.modules.worker.router.WorkerRunner", _MockWorkerRunner)


def test_worker_routes_registered(mock_worker_deps: None) -> None:
    client = TestClient(create_app())
    status = client.get("/api/v1/worker/status")
    assert status.status_code == 200
    assert status.json()["automation_due_count"] == 2

    due = client.get("/api/v1/worker/due-work")
    assert due.status_code == 200
    assert due.json()["due_automation_triggers"] == 2

    run = client.post("/api/v1/worker/run-once")
    assert run.status_code == 200
    assert "Worker cycle complete" in run.json()["summary"]
