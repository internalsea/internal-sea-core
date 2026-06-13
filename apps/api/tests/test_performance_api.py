import uuid
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import (
    MetricDirection,
    MetricStatus,
    MetricValueType,
    PerformanceSubjectType,
)
from app.main import create_app
from app.modules.performance.router import get_performance_service
from app.modules.performance.schemas import (
    PerformanceMetricDefinitionListItem,
    PerformanceMetricDefinitionListResponse,
    PerformanceMetricDefinitionRead,
    PerformanceOverview,
)
from fastapi.testclient import TestClient


@pytest.fixture
def mock_performance_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_performance_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_performance_service] = lambda: mock_performance_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_definition() -> PerformanceMetricDefinitionRead:
    now = datetime.now(UTC)
    return PerformanceMetricDefinitionRead(
        id=uuid.uuid4(),
        name="Data Product Quality Score",
        code="DP_QUALITY_SCORE",
        description=None,
        subject_type=PerformanceSubjectType.DATA_PRODUCT,
        value_type=MetricValueType.SCORE,
        direction=MetricDirection.HIGHER_IS_BETTER,
        frequency=None,
        status=MetricStatus.ACTIVE,
        unit="points",
        target_value=Decimal("90"),
        warning_threshold=None,
        critical_threshold=None,
        owner_id=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_performance_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/performance/overview" in paths
    assert "/api/v1/performance/metrics" in paths
    assert "/api/v1/performance/values" in paths
    assert "/api/v1/performance/entity/{subject_type}/{subject_id}/scorecard" in paths


def test_list_metric_definitions(
    api_client: TestClient,
    mock_performance_service: AsyncMock,
) -> None:
    definition = _sample_definition()
    mock_performance_service.list_definitions.return_value = (
        PerformanceMetricDefinitionListResponse(
            items=[PerformanceMetricDefinitionListItem.model_validate(definition)],
            page=1,
            page_size=20,
            total=1,
            pages=1,
        )
    )

    response = api_client.get("/api/v1/performance/metrics")

    assert response.status_code == 200
    assert response.json()["items"][0]["code"] == "DP_QUALITY_SCORE"


def test_get_performance_overview(
    api_client: TestClient,
    mock_performance_service: AsyncMock,
) -> None:
    mock_performance_service.get_overview.return_value = PerformanceOverview(
        metric_definitions_total=7,
        metric_definitions_active=7,
        metric_values_total=14,
    )

    response = api_client.get("/api/v1/performance/overview")

    assert response.status_code == 200
    assert response.json()["metric_definitions_total"] == 7
