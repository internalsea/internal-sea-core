import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app
from app.modules.automation.router import get_automation_service
from app.modules.automation.schemas import (
    AutomationOverview,
    AutomationRunRead,
    AutomationRunResult,
    AutomationScheduleListItem,
    AutomationScheduleListResponse,
    AutomationScheduleRead,
    AutomationTriggerListItem,
    AutomationTriggerListResponse,
    AutomationTriggerRead,
)


@pytest.fixture
def mock_automation_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_automation_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_automation_service] = lambda: mock_automation_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_schedule() -> AutomationScheduleRead:
    now = datetime.now(timezone.utc)
    return AutomationScheduleRead(
        id=uuid.uuid4(),
        name="Monthly Review",
        description=None,
        frequency="monthly",
        timezone="UTC",
        start_at=None,
        end_at=None,
        next_run_at=None,
        last_run_at=None,
        cron_expression=None,
        is_active=True,
        created_by_id=None,
        created_at=now,
        updated_at=now,
    )


def _sample_trigger() -> AutomationTriggerRead:
    now = datetime.now(timezone.utc)
    return AutomationTriggerRead(
        id=uuid.uuid4(),
        name="Review Dashboard",
        description=None,
        status="active",
        trigger_type="schedule",
        action_type="create_work_item",
        schedule_id=uuid.uuid4(),
        target_type="data_product",
        target_id=uuid.uuid4(),
        conditions=None,
        action_config={"title": "Review"},
        created_by_id=None,
        last_run_at=None,
        next_run_at=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_automation_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/automation/overview" in paths
    assert "/api/v1/automation/schedules" in paths
    assert "/api/v1/automation/triggers" in paths
    assert "/api/v1/automation/triggers/{trigger_id}/run" in paths


def test_list_schedules(api_client: TestClient, mock_automation_service: AsyncMock) -> None:
    schedule = _sample_schedule()
    mock_automation_service.list_schedules.return_value = AutomationScheduleListResponse(
        items=[AutomationScheduleListItem.model_validate(schedule)],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )
    response = api_client.get("/api/v1/automation/schedules")
    assert response.status_code == 200
    assert response.json()["items"][0]["name"] == "Monthly Review"


def test_run_trigger_simulate(api_client: TestClient, mock_automation_service: AsyncMock) -> None:
    trigger_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    run = AutomationRunRead(
        id=uuid.uuid4(),
        trigger_id=trigger_id,
        status="simulated",
        started_at=now,
        finished_at=now,
        target_type="data_product",
        target_id=uuid.uuid4(),
        action_type="create_work_item",
        result_summary="Simulated",
        result_details={"simulate": True},
        error_message=None,
        executed_by_id=None,
        created_at=now,
        updated_at=now,
    )
    mock_automation_service.run_trigger.return_value = AutomationRunResult(
        run=run,
        message="Simulation completed",
    )
    response = api_client.post(
        f"/api/v1/automation/triggers/{trigger_id}/run",
        json={"simulate": True},
    )
    assert response.status_code == 200
    assert response.json()["run"]["status"] == "simulated"


def test_get_overview(api_client: TestClient, mock_automation_service: AsyncMock) -> None:
    mock_automation_service.get_overview.return_value = AutomationOverview(
        schedules_total=3,
        triggers_active=2,
    )
    response = api_client.get("/api/v1/automation/overview")
    assert response.status_code == 200
    assert response.json()["schedules_total"] == 3


@pytest.fixture
def auth_enabled_client(mock_automation_service: AsyncMock) -> TestClient:
    get_settings.cache_clear()
    import os

    os.environ["AUTH_ENABLED"] = "true"
    get_settings.cache_clear()
    app = create_app()
    app.dependency_overrides[get_automation_service] = lambda: mock_automation_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    os.environ["AUTH_ENABLED"] = "false"
    get_settings.cache_clear()


def test_viewer_cannot_run_trigger(auth_enabled_client: TestClient) -> None:
    login = auth_enabled_client.post(
        "/api/v1/auth/login",
        json={"email": "viewer@example.com", "password": "viewer12345"},
    )
    if login.status_code != 200:
        pytest.skip("Auth seed users not available in unit test DB")
    token = login.json()["access_token"]
    response = auth_enabled_client.post(
        f"/api/v1/automation/triggers/{uuid.uuid4()}/run",
        headers={"Authorization": f"Bearer {token}"},
        json={"simulate": True},
    )
    assert response.status_code == 403


def test_editor_can_run_trigger(
    auth_enabled_client: TestClient,
    mock_automation_service: AsyncMock,
) -> None:
    login = auth_enabled_client.post(
        "/api/v1/auth/login",
        json={"email": "editor@example.com", "password": "editor12345"},
    )
    if login.status_code != 200:
        pytest.skip("Auth seed users not available in unit test DB")
    token = login.json()["access_token"]
    trigger_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    mock_automation_service.run_trigger.return_value = AutomationRunResult(
        run=AutomationRunRead(
            id=uuid.uuid4(),
            trigger_id=trigger_id,
            status="simulated",
            started_at=now,
            finished_at=now,
            target_type="data_product",
            target_id=uuid.uuid4(),
            action_type="create_work_item",
            result_summary="Simulated",
            result_details=None,
            error_message=None,
            executed_by_id=None,
            created_at=now,
            updated_at=now,
        ),
        message="Simulation completed",
    )
    response = auth_enabled_client.post(
        f"/api/v1/automation/triggers/{trigger_id}/run",
        headers={"Authorization": f"Bearer {token}"},
        json={"simulate": True},
    )
    assert response.status_code == 200
