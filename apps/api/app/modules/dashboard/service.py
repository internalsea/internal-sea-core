import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import DataProductType, ProjectType, WorkItemType
from app.models.catalog import DataProduct
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.dashboard.advanced_repository import AdvancedDashboardRepository
from app.modules.dashboard.gaps import OwnershipGapCandidate
from app.modules.dashboard.repository import DashboardRepository, ProjectWorkCounts
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

MAX_DASHBOARD_LIMIT = 20
MAX_ADVANCED_DASHBOARD_LIMIT = 50


def normalize_dashboard_limit(
    limit: int, default: int, *, max_limit: int = MAX_DASHBOARD_LIMIT
) -> int:
    if limit < 1:
        return default
    return min(limit, max_limit)


class DashboardService:
    def __init__(self, repository: DashboardRepository) -> None:
        self._repository = repository
        self._advanced = AdvancedDashboardRepository(repository._session, repository)

    async def get_summary(self) -> DashboardSummary:
        return await self._repository.get_summary()

    async def get_recent_data_products(self, limit: int = 8) -> list[RecentDataProductItem]:
        normalized_limit = normalize_dashboard_limit(limit, default=8)
        products = await self._repository.get_recent_data_products(limit=normalized_limit)
        return [_to_recent_data_product(product) for product in products]

    async def get_high_priority_work_items(self, limit: int = 10) -> list[HighPriorityWorkItem]:
        normalized_limit = normalize_dashboard_limit(limit, default=10)
        items = await self._repository.get_high_priority_work_items(limit=normalized_limit)
        return [_to_high_priority_work_item(item) for item in items]

    async def get_project_health(self, limit: int = 8) -> list[ProjectHealthItem]:
        normalized_limit = normalize_dashboard_limit(limit, default=8)
        projects = await self._repository.get_project_health(limit=normalized_limit)
        counts = await self._repository.get_project_work_counts(
            [project.id for project in projects]
        )
        return [_to_project_health_item(project, counts.get(project.id)) for project in projects]

    async def get_capability_workload(self) -> list[CapabilityWorkloadItem]:
        rows = await self._repository.get_capability_workload()
        return [CapabilityWorkloadItem.model_validate(row) for row in rows]

    async def get_ownership_gaps(self, limit: int = 10) -> list[OwnershipGapItem]:
        normalized_limit = normalize_dashboard_limit(limit, default=10)
        gaps = await self._repository.get_ownership_gaps(limit=normalized_limit)
        return [_to_ownership_gap(gap) for gap in gaps]

    async def get_executive_summary(self) -> ExecutiveSummary:
        return await self._advanced.get_executive_summary()

    async def get_operational_health(self) -> OperationalHealth:
        return await self._advanced.get_operational_health()

    async def get_data_product_health(self, limit: int = 10) -> DataProductHealthResponse:
        return await self._advanced.get_data_product_health(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_work_delivery(self) -> WorkDeliverySummary:
        return await self._advanced.get_work_delivery()

    async def get_project_insights(self, limit: int = 10) -> ProjectInsightsResponse:
        return await self._advanced.get_project_insights(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_compliance_insights(self, limit: int = 10) -> ComplianceInsights:
        return await self._advanced.get_compliance_insights(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_performance_insights(self, limit: int = 10) -> PerformanceInsights:
        return await self._advanced.get_performance_insights(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_automation_health(self, limit: int = 10) -> AutomationHealth:
        return await self._advanced.get_automation_health(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_notification_health(self, limit: int = 10) -> NotificationHealth:
        return await self._advanced.get_notification_health(
            limit=normalize_dashboard_limit(limit, 10, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_recent_activity(self, limit: int = 15) -> RecentActivityResponse:
        return await self._advanced.get_recent_activity(
            limit=normalize_dashboard_limit(limit, 15, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_actionable_insights(self, limit: int = 20) -> ActionableInsightsResponse:
        return await self._advanced.get_actionable_insights(
            limit=normalize_dashboard_limit(limit, 20, max_limit=MAX_ADVANCED_DASHBOARD_LIMIT)
        )

    async def get_advanced_dashboard(self) -> AdvancedDashboardResponse:
        return AdvancedDashboardResponse(
            executive_summary=await self.get_executive_summary(),
            operational_health=await self.get_operational_health(),
            data_product_health=await self.get_data_product_health(),
            work_delivery=await self.get_work_delivery(),
            project_insights=await self.get_project_insights(),
            compliance_insights=await self.get_compliance_insights(),
            performance_insights=await self.get_performance_insights(),
            automation_health=await self.get_automation_health(),
            notification_health=await self.get_notification_health(),
            recent_activity=await self.get_recent_activity(),
            actionable_insights=await self.get_actionable_insights(),
        )


def build_dashboard_service(
    session: AsyncSession,
    *,
    company_id: uuid.UUID | None = None,
) -> DashboardService:
    return DashboardService(DashboardRepository(session, company_id=company_id))


def _to_recent_data_product(product: DataProduct) -> RecentDataProductItem:
    return RecentDataProductItem(
        id=product.id,
        name=product.name,
        type=_enum_value(product.type),
        status=_enum_value(product.status),
        quality_status=_enum_value(product.quality_status),
        updated_at=product.updated_at,
    )


def _to_high_priority_work_item(item: WorkItem) -> HighPriorityWorkItem:
    return HighPriorityWorkItem(
        id=item.id,
        title=item.title,
        type=_enum_value(item.type),
        status=_enum_value(item.status),
        priority=_enum_value(item.priority),
        due_date=item.due_date,
        data_product_id=item.data_product_id,
        project_id=item.project_id,
        updated_at=item.updated_at,
    )


def _to_project_health_item(
    project: Project,
    counts: ProjectWorkCounts | None,
) -> ProjectHealthItem:
    open_work_items = 0
    overdue_work_items = 0
    if counts is not None:
        open_work_items = counts.open_work_items
        overdue_work_items = counts.overdue_work_items

    return ProjectHealthItem(
        id=project.id,
        name=project.name,
        project_type=_enum_value(project.project_type),
        status=_enum_value(project.status),
        health_status=project.health_status,
        client_name=project.client_name,
        target_end_date=project.target_end_date,
        open_work_items=open_work_items,
        overdue_work_items=overdue_work_items,
    )


def _to_ownership_gap(gap: OwnershipGapCandidate) -> OwnershipGapItem:
    return OwnershipGapItem(
        entity_type=gap.entity_type,
        entity_id=gap.entity_id,
        name=gap.name,
        gap_type=gap.gap_type,
        severity=gap.severity,
        description=gap.description,
    )


def _enum_value(value: DataProductType | ProjectType | WorkItemType | object) -> str:
    return str(value.value if hasattr(value, "value") else value)
