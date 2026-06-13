from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.main import create_app
from app.modules.dashboard.router import get_scoped_dashboard_service
from app.modules.dashboard.schemas import (
    ActionableInsightsResponse,
    ExecutiveSummary,
    OperationalHealth,
)
from app.modules.dashboard.service import MAX_ADVANCED_DASHBOARD_LIMIT, normalize_dashboard_limit
from fastapi.testclient import TestClient


@pytest.fixture
def mock_dashboard_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_dashboard_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_scoped_dashboard_service] = lambda: mock_dashboard_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_advanced_endpoints_registered(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    paths = response.json()["paths"]
    assert "/api/v1/dashboard/executive-summary" in paths
    assert "/api/v1/dashboard/actionable-insights" in paths
    assert "/api/v1/dashboard/advanced" in paths


def test_executive_summary_endpoint(
    api_client: TestClient, mock_dashboard_service: AsyncMock
) -> None:
    now = datetime.now(UTC)
    mock_dashboard_service.get_executive_summary.return_value = ExecutiveSummary(
        overall_status="good",
        overall_score=85,
        active_projects=2,
        active_internal_projects=1,
        active_data_products=4,
        open_work_items=5,
        overdue_work_items=1,
        compliance_open_checks=2,
        compliance_overdue_checks=0,
        average_performance_score=80.0,
        ownership_gaps=1,
        automation_due_triggers=0,
        notification_failed_messages=0,
        generated_at=now,
    )
    response = api_client.get("/api/v1/dashboard/executive-summary")
    assert response.status_code == 200
    assert response.json()["overall_score"] == 85


def test_actionable_insights_endpoint(
    api_client: TestClient, mock_dashboard_service: AsyncMock
) -> None:
    mock_dashboard_service.get_actionable_insights.return_value = ActionableInsightsResponse(
        items=[],
        total=0,
        critical_count=0,
        warning_count=0,
        info_count=0,
    )
    response = api_client.get("/api/v1/dashboard/actionable-insights?limit=100")
    assert response.status_code == 200
    mock_dashboard_service.get_actionable_insights.assert_awaited_once_with(
        normalize_dashboard_limit(100, 20, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
    )


def test_operational_health_endpoint(
    api_client: TestClient, mock_dashboard_service: AsyncMock
) -> None:
    now = datetime.now(UTC)
    mock_dashboard_service.get_operational_health.return_value = OperationalHealth(
        status="warning",
        work_health_score=75,
        project_health_score=80,
        compliance_health_score=70,
        performance_health_score=85,
        automation_health_score=90,
        risk_items_count=1,
        critical_work_items_count=1,
        overdue_items_count=2,
        blocked_or_warning_projects=1,
        generated_at=now,
    )
    response = api_client.get("/api/v1/dashboard/operational-health")
    assert response.status_code == 200
    assert response.json()["work_health_score"] == 75
