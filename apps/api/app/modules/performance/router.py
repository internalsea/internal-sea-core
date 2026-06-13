import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import (
    MetricStatus,
    MetricValueStatus,
    MetricValueType,
    PerformanceSubjectType,
)
from app.modules.activity.dependencies import build_activity_service
from app.modules.performance.repository import PerformanceRepository
from app.modules.performance.schemas import (
    PerformanceMetricDefinitionCreate,
    PerformanceMetricDefinitionListResponse,
    PerformanceMetricDefinitionRead,
    PerformanceMetricDefinitionUpdate,
    PerformanceMetricValueCreate,
    PerformanceMetricValueListResponse,
    PerformanceMetricValueRead,
    PerformanceMetricValueUpdate,
    PerformanceOverview,
    PerformanceScorecard,
)
from app.modules.performance.service import PerformanceService

router = APIRouter(prefix="/performance", tags=["Performance"])


def get_performance_service(db: AsyncSession = Depends(get_db)) -> PerformanceService:
    return PerformanceService(
        PerformanceRepository(db),
        build_activity_service(db),
        db,
    )


@router.get("/overview", response_model=PerformanceOverview)
async def get_performance_overview(
    _user: ViewerUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceOverview:
    return await service.get_overview()


@router.get("/metrics", response_model=PerformanceMetricDefinitionListResponse)
async def list_metric_definitions(
    _user: ViewerUser,
    search: str | None = None,
    subject_type: PerformanceSubjectType | None = None,
    value_type: MetricValueType | None = None,
    status: MetricStatus | None = None,
    owner_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricDefinitionListResponse:
    from app.modules.performance.schemas import PerformanceMetricDefinitionFilters

    filters = PerformanceMetricDefinitionFilters(
        search=search,
        subject_type=subject_type,
        value_type=value_type,
        status=status,
        owner_id=owner_id,
    )
    return await service.list_definitions(filters=filters, page=page, page_size=page_size)


@router.post(
    "/metrics", response_model=PerformanceMetricDefinitionRead, status_code=status.HTTP_201_CREATED
)
async def create_metric_definition(
    payload: PerformanceMetricDefinitionCreate,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricDefinitionRead:
    return await service.create_definition(payload)


@router.get("/metrics/{metric_definition_id}", response_model=PerformanceMetricDefinitionRead)
async def get_metric_definition(
    metric_definition_id: uuid.UUID,
    _user: ViewerUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricDefinitionRead:
    return await service.get_definition(metric_definition_id)


@router.patch("/metrics/{metric_definition_id}", response_model=PerformanceMetricDefinitionRead)
async def update_metric_definition(
    metric_definition_id: uuid.UUID,
    payload: PerformanceMetricDefinitionUpdate,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricDefinitionRead:
    return await service.update_definition(metric_definition_id, payload)


@router.delete("/metrics/{metric_definition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric_definition(
    metric_definition_id: uuid.UUID,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> None:
    await service.delete_definition(metric_definition_id)


@router.get("/values", response_model=PerformanceMetricValueListResponse)
async def list_metric_values(
    _user: ViewerUser,
    metric_definition_id: uuid.UUID | None = None,
    subject_type: PerformanceSubjectType | None = None,
    subject_id: uuid.UUID | None = None,
    status: MetricValueStatus | None = None,
    period_start_from: date | None = None,
    period_end_to: date | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricValueListResponse:
    from app.modules.performance.schemas import PerformanceMetricValueFilters

    filters = PerformanceMetricValueFilters(
        metric_definition_id=metric_definition_id,
        subject_type=subject_type,
        subject_id=subject_id,
        status=status,
        period_start_from=period_start_from,
        period_end_to=period_end_to,
    )
    return await service.list_values(filters=filters, page=page, page_size=page_size)


@router.post(
    "/values", response_model=PerformanceMetricValueRead, status_code=status.HTTP_201_CREATED
)
async def create_metric_value(
    payload: PerformanceMetricValueCreate,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricValueRead:
    return await service.create_value(payload)


@router.get("/values/{metric_value_id}", response_model=PerformanceMetricValueRead)
async def get_metric_value(
    metric_value_id: uuid.UUID,
    _user: ViewerUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricValueRead:
    return await service.get_value(metric_value_id)


@router.patch("/values/{metric_value_id}", response_model=PerformanceMetricValueRead)
async def update_metric_value(
    metric_value_id: uuid.UUID,
    payload: PerformanceMetricValueUpdate,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricValueRead:
    return await service.update_value(metric_value_id, payload)


@router.delete("/values/{metric_value_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric_value(
    metric_value_id: uuid.UUID,
    _user: EditorUser,
    service: PerformanceService = Depends(get_performance_service),
) -> None:
    await service.delete_value(metric_value_id)


@router.get(
    "/entity/{subject_type}/{subject_id}/scorecard",
    response_model=PerformanceScorecard,
)
async def get_entity_scorecard(
    subject_type: PerformanceSubjectType,
    subject_id: uuid.UUID,
    _user: ViewerUser,
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceScorecard:
    return await service.get_entity_scorecard(subject_type, subject_id)


@router.get(
    "/entity/{subject_type}/{subject_id}/values",
    response_model=PerformanceMetricValueListResponse,
)
async def get_entity_values(
    subject_type: PerformanceSubjectType,
    subject_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: PerformanceService = Depends(get_performance_service),
) -> PerformanceMetricValueListResponse:
    return await service.list_entity_values(
        subject_type,
        subject_id,
        page=page,
        page_size=page_size,
    )
