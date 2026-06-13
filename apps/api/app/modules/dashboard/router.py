import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import ViewerUser
from app.dependencies import get_db
from app.modules.dashboard.schemas import (
    ActionableInsightsResponse,
    AdvancedDashboardResponse,
    AutomationHealth,
    CapabilityWorkloadItem,
    ComplianceInsights,
    DashboardSummary,
    DataProductHealthResponse,
    ExecutiveSummary,
    HighPriorityWorkItem,
    NotificationHealth,
    OperationalHealth,
    OwnershipGapItem,
    PerformanceInsights,
    ProjectHealthItem,
    ProjectInsightsResponse,
    RecentActivityResponse,
    RecentDataProductItem,
    WorkDeliverySummary,
)
from app.modules.dashboard.service import DashboardService, build_dashboard_service
from app.modules.tenancy.dependencies import get_current_company_id

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    return build_dashboard_service(db)


def get_scoped_dashboard_service(
    db: AsyncSession = Depends(get_db),
    company_id: uuid.UUID = Depends(get_current_company_id),
) -> DashboardService:
    return build_dashboard_service(db, company_id=company_id)


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    _user: ViewerUser,
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardSummary:
    return await service.get_summary()


@router.get("/recent-data-products", response_model=list[RecentDataProductItem])
async def get_recent_data_products(
    _user: ViewerUser,
    limit: int = Query(8, ge=1),
    service: DashboardService = Depends(get_dashboard_service),
) -> list[RecentDataProductItem]:
    return await service.get_recent_data_products(limit)


@router.get("/high-priority-work-items", response_model=list[HighPriorityWorkItem])
async def get_high_priority_work_items(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_dashboard_service),
) -> list[HighPriorityWorkItem]:
    return await service.get_high_priority_work_items(limit)


@router.get("/project-health", response_model=list[ProjectHealthItem])
async def get_project_health(
    _user: ViewerUser,
    limit: int = Query(8, ge=1),
    service: DashboardService = Depends(get_dashboard_service),
) -> list[ProjectHealthItem]:
    return await service.get_project_health(limit)


@router.get("/capability-workload", response_model=list[CapabilityWorkloadItem])
async def get_capability_workload(
    _user: ViewerUser,
    service: DashboardService = Depends(get_dashboard_service),
) -> list[CapabilityWorkloadItem]:
    return await service.get_capability_workload()


@router.get("/ownership-gaps", response_model=list[OwnershipGapItem])
async def get_ownership_gaps(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_dashboard_service),
) -> list[OwnershipGapItem]:
    return await service.get_ownership_gaps(limit)


@router.get("/executive-summary", response_model=ExecutiveSummary)
async def get_executive_summary(
    _user: ViewerUser,
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> ExecutiveSummary:
    return await service.get_executive_summary()


@router.get("/operational-health", response_model=OperationalHealth)
async def get_operational_health(
    _user: ViewerUser,
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> OperationalHealth:
    return await service.get_operational_health()


@router.get("/data-product-health", response_model=DataProductHealthResponse)
async def get_data_product_health(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> DataProductHealthResponse:
    return await service.get_data_product_health(limit)


@router.get("/work-delivery", response_model=WorkDeliverySummary)
async def get_work_delivery(
    _user: ViewerUser,
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> WorkDeliverySummary:
    return await service.get_work_delivery()


@router.get("/project-insights", response_model=ProjectInsightsResponse)
async def get_project_insights(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> ProjectInsightsResponse:
    return await service.get_project_insights(limit)


@router.get("/compliance-insights", response_model=ComplianceInsights)
async def get_compliance_insights(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> ComplianceInsights:
    return await service.get_compliance_insights(limit)


@router.get("/performance-insights", response_model=PerformanceInsights)
async def get_performance_insights(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> PerformanceInsights:
    return await service.get_performance_insights(limit)


@router.get("/automation-health", response_model=AutomationHealth)
async def get_automation_health(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> AutomationHealth:
    return await service.get_automation_health(limit)


@router.get("/notification-health", response_model=NotificationHealth)
async def get_notification_health(
    _user: ViewerUser,
    limit: int = Query(10, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> NotificationHealth:
    return await service.get_notification_health(limit)


@router.get("/recent-activity", response_model=RecentActivityResponse)
async def get_recent_activity(
    _user: ViewerUser,
    limit: int = Query(15, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> RecentActivityResponse:
    return await service.get_recent_activity(limit)


@router.get("/actionable-insights", response_model=ActionableInsightsResponse)
async def get_actionable_insights(
    _user: ViewerUser,
    limit: int = Query(20, ge=1),
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> ActionableInsightsResponse:
    return await service.get_actionable_insights(limit)


@router.get("/advanced", response_model=AdvancedDashboardResponse)
async def get_advanced_dashboard(
    _user: ViewerUser,
    service: DashboardService = Depends(get_scoped_dashboard_service),
) -> AdvancedDashboardResponse:
    return await service.get_advanced_dashboard()
