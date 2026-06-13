import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import PerformanceSubjectType
from app.modules.performance.errors import PerformanceMetricConflictError
from app.modules.performance.schemas import PerformanceMetricValueCreate
from app.modules.performance.service import PerformanceService


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_activity() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def performance_service(
    mock_repository: AsyncMock,
    mock_activity: AsyncMock,
    mock_session: AsyncMock,
) -> PerformanceService:
    return PerformanceService(mock_repository, mock_activity, mock_session)


@pytest.mark.asyncio
async def test_create_value_raises_conflict_on_duplicate(
    performance_service: PerformanceService,
    mock_repository: AsyncMock,
    mock_session: AsyncMock,
) -> None:
    definition_id = uuid.uuid4()
    subject_id = uuid.uuid4()
    definition = MagicMock()
    definition.id = definition_id
    definition.subject_type = PerformanceSubjectType.DATA_PRODUCT.value
    definition.name = "Quality Score"
    mock_repository.get_definition_by_id.return_value = definition
    mock_repository.get_duplicate_value.return_value = MagicMock()
    mock_session.get.return_value = MagicMock()

    payload = PerformanceMetricValueCreate(
        metric_definition_id=definition_id,
        subject_type=PerformanceSubjectType.DATA_PRODUCT,
        subject_id=subject_id,
        value_numeric=Decimal("92"),
    )

    with pytest.raises(PerformanceMetricConflictError):
        await performance_service.create_value(payload)


@pytest.mark.asyncio
async def test_get_overview(
    performance_service: PerformanceService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_overview.return_value = {
        "metric_definitions_total": 7,
        "metric_definitions_active": 7,
        "metric_values_total": 14,
        "scorecards_available": 10,
        "people_metrics_count": 2,
        "team_metrics_count": 2,
        "capability_metrics_count": 2,
        "project_metrics_count": 4,
        "data_product_metrics_count": 4,
    }
    overview = await performance_service.get_overview()
    assert overview.metric_definitions_total == 7
    assert overview.metric_values_total == 14
