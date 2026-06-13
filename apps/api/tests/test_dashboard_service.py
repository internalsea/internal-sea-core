import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import (
    DataProductStatus,
    DataProductType,
    ProjectStatus,
    ProjectType,
    QualityStatus,
)
from app.models.catalog import DataProduct
from app.models.projects import Project
from app.modules.dashboard.gaps import OwnershipGapCandidate, resolve_project_gap_severity
from app.modules.dashboard.gaps import (
    resolve_data_product_owner_gap_severity as resolve_dp_severity,
)
from app.modules.dashboard.repository import ProjectWorkCounts
from app.modules.dashboard.schemas import DashboardSummary
from app.modules.dashboard.service import DashboardService, normalize_dashboard_limit


def test_normalize_dashboard_limit_clamps_to_max() -> None:
    assert normalize_dashboard_limit(100, default=8) == 20
    assert normalize_dashboard_limit(5, default=8) == 5
    assert normalize_dashboard_limit(0, default=10) == 10


def test_resolve_data_product_owner_gap_severity_active_is_high() -> None:
    severity = resolve_dp_severity(
        gap_type="missing_business_owner",
        status=DataProductStatus.ACTIVE,
    )
    assert severity == "high"


def test_resolve_data_product_owner_gap_severity_draft_is_low() -> None:
    severity = resolve_dp_severity(
        gap_type="missing_technical_owner",
        status=DataProductStatus.DRAFT,
    )
    assert severity == "low"


def test_resolve_project_owner_gap_severity_active_is_high() -> None:
    severity = resolve_project_gap_severity(
        gap_type="missing_owner",
        status=ProjectStatus.ACTIVE,
    )
    assert severity == "high"


@pytest.mark.asyncio
async def test_service_get_summary_calls_repository() -> None:
    repository = AsyncMock()
    repository.get_summary.return_value = DashboardSummary(data_products_total=1)
    service = DashboardService(repository)

    result = await service.get_summary()

    repository.get_summary.assert_awaited_once()
    assert result.data_products_total == 1


@pytest.mark.asyncio
async def test_service_get_recent_data_products_normalizes_limit() -> None:
    now = datetime.now(UTC)
    product = DataProduct(
        id=uuid.uuid4(),
        name="Finance KPI Layer",
        type=DataProductType.METRIC,
        status=DataProductStatus.ACTIVE,
        quality_status=QualityStatus.GOOD,
        created_at=now,
        updated_at=now,
    )
    repository = AsyncMock()
    repository.get_recent_data_products.return_value = [product]
    service = DashboardService(repository)

    result = await service.get_recent_data_products(limit=50)

    repository.get_recent_data_products.assert_awaited_once_with(limit=20)
    assert len(result) == 1
    assert result[0].name == "Finance KPI Layer"


@pytest.mark.asyncio
async def test_service_get_project_health_merges_work_counts() -> None:
    project_id = uuid.uuid4()
    now = datetime.now(UTC)
    project = Project(
        id=project_id,
        name="Internal Sea MVP",
        project_type=ProjectType.INTERNAL_PROJECT,
        status=ProjectStatus.ACTIVE,
        health_status="healthy",
        created_at=now,
        updated_at=now,
    )
    repository = AsyncMock()
    repository.get_project_health.return_value = [project]
    repository.get_project_work_counts.return_value = {
        project_id: ProjectWorkCounts(open_work_items=4, overdue_work_items=1),
    }
    service = DashboardService(repository)

    result = await service.get_project_health(limit=8)

    assert result[0].open_work_items == 4
    assert result[0].overdue_work_items == 1


@pytest.mark.asyncio
async def test_service_get_ownership_gaps_maps_candidates() -> None:
    gap_id = uuid.uuid4()
    repository = AsyncMock()
    repository.get_ownership_gaps.return_value = [
        OwnershipGapCandidate(
            entity_type="work_item",
            entity_id=gap_id,
            name="Add Work Board",
            gap_type="missing_assignee",
            description="Open work item without an assignee.",
            severity="medium",
        )
    ]
    service = DashboardService(repository)

    result = await service.get_ownership_gaps(limit=25)

    repository.get_ownership_gaps.assert_awaited_once_with(limit=20)
    assert result[0].entity_id == gap_id
    assert result[0].severity == "medium"
