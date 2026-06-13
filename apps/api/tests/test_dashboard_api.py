import uuid
from datetime import UTC, date, datetime
from unittest.mock import AsyncMock

import pytest
from app.main import create_app
from app.modules.dashboard.router import get_dashboard_service
from app.modules.dashboard.schemas import (
    CapabilityWorkloadItem,
    DashboardSummary,
    HighPriorityWorkItem,
    OwnershipGapItem,
    ProjectHealthItem,
    RecentDataProductItem,
)
from fastapi.testclient import TestClient


@pytest.fixture
def mock_dashboard_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_dashboard_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_dashboard_service] = lambda: mock_dashboard_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_openapi_includes_dashboard_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/dashboard/summary" in paths
    assert "/api/v1/dashboard/recent-data-products" in paths
    assert "/api/v1/dashboard/high-priority-work-items" in paths
    assert "/api/v1/dashboard/project-health" in paths
    assert "/api/v1/dashboard/capability-workload" in paths
    assert "/api/v1/dashboard/ownership-gaps" in paths


def test_get_dashboard_summary(api_client: TestClient, mock_dashboard_service: AsyncMock) -> None:
    mock_dashboard_service.get_summary.return_value = DashboardSummary(
        data_products_total=6,
        work_items_open=7,
        projects_active=2,
    )

    response = api_client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    data = response.json()
    assert data["data_products_total"] == 6
    assert data["work_items_open"] == 7


def test_get_recent_data_products(
    api_client: TestClient, mock_dashboard_service: AsyncMock
) -> None:
    now = datetime.now(UTC)
    mock_dashboard_service.get_recent_data_products.return_value = [
        RecentDataProductItem(
            id=uuid.uuid4(),
            name="Executive Sales Dashboard",
            type="dashboard",
            status="active",
            quality_status="good",
            updated_at=now,
        )
    ]

    response = api_client.get("/api/v1/dashboard/recent-data-products?limit=5")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Executive Sales Dashboard"
    mock_dashboard_service.get_recent_data_products.assert_awaited_once_with(5)


def test_get_high_priority_work_items(
    api_client: TestClient,
    mock_dashboard_service: AsyncMock,
) -> None:
    now = datetime.now(UTC)
    mock_dashboard_service.get_high_priority_work_items.return_value = [
        HighPriorityWorkItem(
            id=uuid.uuid4(),
            title="Missing auth and permissions",
            type="risk",
            status="ready",
            priority="critical",
            due_date=date(2026, 6, 20),
            data_product_id=None,
            project_id=uuid.uuid4(),
            updated_at=now,
        )
    ]

    response = api_client.get("/api/v1/dashboard/high-priority-work-items")

    assert response.status_code == 200
    assert response.json()[0]["priority"] == "critical"


def test_get_project_health(api_client: TestClient, mock_dashboard_service: AsyncMock) -> None:
    mock_dashboard_service.get_project_health.return_value = [
        ProjectHealthItem(
            id=uuid.uuid4(),
            name="Finance Data Platform Migration",
            project_type="client_project",
            status="active",
            health_status="warning",
            client_name="Example Retail Group",
            target_end_date=date(2026, 9, 1),
            open_work_items=2,
            overdue_work_items=1,
        )
    ]

    response = api_client.get("/api/v1/dashboard/project-health")

    assert response.status_code == 200
    assert response.json()[0]["health_status"] == "warning"


def test_get_capability_workload(api_client: TestClient, mock_dashboard_service: AsyncMock) -> None:
    mock_dashboard_service.get_capability_workload.return_value = [
        CapabilityWorkloadItem(
            capability_id=uuid.uuid4(),
            capability_name="Data Engineering",
            people_count=3,
            active_people_count=3,
            open_work_items=4,
            active_projects=2,
            active_data_products=2,
        )
    ]

    response = api_client.get("/api/v1/dashboard/capability-workload")

    assert response.status_code == 200
    assert response.json()[0]["capability_name"] == "Data Engineering"


def test_get_ownership_gaps(api_client: TestClient, mock_dashboard_service: AsyncMock) -> None:
    mock_dashboard_service.get_ownership_gaps.return_value = [
        OwnershipGapItem(
            entity_type="data_product",
            entity_id=uuid.uuid4(),
            name="AI Report Generator",
            gap_type="missing_business_owner",
            severity="low",
            description="Catalog object without a business owner.",
        )
    ]

    response = api_client.get("/api/v1/dashboard/ownership-gaps")

    assert response.status_code == 200
    assert response.json()[0]["gap_type"] == "missing_business_owner"
