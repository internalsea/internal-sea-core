import uuid
from datetime import UTC, date, datetime

from app.modules.dashboard.schemas import (
    CapabilityWorkloadItem,
    DashboardSummary,
    HighPriorityWorkItem,
    OwnershipGapItem,
    ProjectHealthItem,
    RecentDataProductItem,
)


def test_dashboard_summary_accepts_valid_counts() -> None:
    summary = DashboardSummary(
        data_products_total=6,
        data_products_active=5,
        data_products_with_quality_warning=2,
        data_products_with_quality_critical=0,
        work_items_total=10,
        work_items_open=7,
        work_items_overdue=2,
        work_items_technical_debt=1,
        work_items_risks=1,
        projects_total=3,
        projects_active=2,
        internal_projects_total=3,
        internal_projects_active=2,
        people_total=10,
        people_active=10,
        teams_total=5,
        capabilities_total=8,
    )

    assert summary.work_items_open == 7
    assert summary.capabilities_total == 8


def test_recent_data_product_item_schema() -> None:
    now = datetime.now(UTC)
    item = RecentDataProductItem(
        id=uuid.uuid4(),
        name="Executive Sales Dashboard",
        type="dashboard",
        status="active",
        quality_status="good",
        updated_at=now,
    )

    assert item.type == "dashboard"


def test_high_priority_work_item_schema() -> None:
    now = datetime.now(UTC)
    item = HighPriorityWorkItem(
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

    assert item.priority == "critical"


def test_project_health_item_schema() -> None:
    item = ProjectHealthItem(
        id=uuid.uuid4(),
        name="Finance Data Platform Migration",
        project_type="client_project",
        status="active",
        health_status="warning",
        client_name="Example Retail Group",
        target_end_date=date(2026, 9, 1),
        open_work_items=3,
        overdue_work_items=1,
    )

    assert item.overdue_work_items == 1


def test_capability_workload_item_schema() -> None:
    item = CapabilityWorkloadItem(
        capability_id=uuid.uuid4(),
        capability_name="Data Engineering",
        people_count=3,
        active_people_count=3,
        open_work_items=4,
        active_projects=2,
        active_data_products=2,
    )

    assert item.open_work_items == 4


def test_ownership_gap_item_schema() -> None:
    item = OwnershipGapItem(
        entity_type="data_product",
        entity_id=uuid.uuid4(),
        name="Inventory Health Dataset",
        gap_type="missing_business_owner",
        severity="high",
        description="Active catalog object without a business owner.",
    )

    assert item.severity == "high"
