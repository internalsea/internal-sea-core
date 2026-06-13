from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from typing import Any

from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import (
    AutomationRunStatus,
    AutomationStatus,
    ComplianceStatus,
    DataProductStatus,
    ProjectStatus,
    ProjectType,
    QualityStatus,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.models.automation import AutomationRun, AutomationTrigger
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck
from app.models.notifications import NotificationMessage
from app.models.people import Capability, Person, Team
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.dashboard.gaps import (
    OwnershipGapCandidate,
    collect_data_product_gaps,
    collect_project_gaps,
    collect_work_item_gaps,
    sort_ownership_gaps,
)
from app.modules.dashboard.schemas import DashboardSummary

COMPLETED_WORK_ITEM_STATUSES = (WorkItemStatus.DONE, WorkItemStatus.CLOSED)
OPEN_WORK_ITEM_FILTER = WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES)
HIGH_PRIORITY_VALUES = (WorkItemPriority.HIGH, WorkItemPriority.CRITICAL)

HEALTH_SEVERITY_ORDER = case(
    (Project.health_status == "critical", 0),
    (Project.health_status == "warning", 1),
    (Project.health_status == "healthy", 2),
    else_=3,
)

PRIORITY_SEVERITY_ORDER = case(
    (WorkItem.priority == WorkItemPriority.CRITICAL, 0),
    (WorkItem.priority == WorkItemPriority.HIGH, 1),
    else_=2,
)


@dataclass
class ProjectWorkCounts:
    open_work_items: int = 0
    overdue_work_items: int = 0


class DashboardRepository:
    def __init__(self, session: AsyncSession, *, company_id: uuid.UUID | None = None) -> None:
        self._session = session
        self._company_id = company_id

    def _apply_company_scope(self, query: Any, model: type[object]) -> Any:
        if self._company_id is not None and hasattr(model, "company_id"):
            query = query.where(model.company_id == self._company_id)
        return query

    async def get_summary(self) -> DashboardSummary:
        today = date.today()

        data_products_total = await self._count(DataProduct)
        data_products_active = await self._count(
            DataProduct,
            DataProduct.status == DataProductStatus.ACTIVE,
        )
        data_products_with_quality_warning = await self._count(
            DataProduct,
            DataProduct.quality_status == QualityStatus.WARNING,
        )
        data_products_with_quality_critical = await self._count(
            DataProduct,
            DataProduct.quality_status == QualityStatus.CRITICAL,
        )

        work_items_total = await self._count(WorkItem)
        work_items_open = await self._count(WorkItem, OPEN_WORK_ITEM_FILTER)
        work_items_overdue = await self._count(
            WorkItem,
            and_(
                WorkItem.due_date.is_not(None),
                WorkItem.due_date < today,
                OPEN_WORK_ITEM_FILTER,
            ),
        )
        work_items_technical_debt = await self._count(
            WorkItem,
            WorkItem.type == WorkItemType.TECHNICAL_DEBT,
        )
        work_items_risks = await self._count(WorkItem, WorkItem.type == WorkItemType.RISK)

        projects_total = await self._count(
            Project,
            Project.project_type != ProjectType.INTERNAL_PROJECT,
        )
        projects_active = await self._count(
            Project,
            and_(
                Project.project_type != ProjectType.INTERNAL_PROJECT,
                Project.status == ProjectStatus.ACTIVE,
            ),
        )
        internal_projects_total = await self._count(
            Project,
            Project.project_type == ProjectType.INTERNAL_PROJECT,
        )
        internal_projects_active = await self._count(
            Project,
            and_(
                Project.project_type == ProjectType.INTERNAL_PROJECT,
                Project.status == ProjectStatus.ACTIVE,
            ),
        )

        people_total = await self._count(Person)
        people_active = await self._count(Person, Person.is_active.is_(True))
        teams_total = await self._count(Team)
        capabilities_total = await self._count(Capability)

        compliance_checks_total = await self._count(ComplianceCheck)
        compliance_checks_open = await self._count(
            ComplianceCheck,
            ComplianceCheck.status.in_(
                [
                    ComplianceStatus.NOT_STARTED.value,
                    ComplianceStatus.IN_PROGRESS.value,
                ]
            ),
        )
        compliance_checks_non_compliant = await self._count(
            ComplianceCheck,
            ComplianceCheck.status == ComplianceStatus.NON_COMPLIANT.value,
        )
        compliance_checks_overdue = await self._count(
            ComplianceCheck,
            and_(
                ComplianceCheck.due_date < today,
                ComplianceCheck.status.in_(
                    [
                        ComplianceStatus.NOT_STARTED.value,
                        ComplianceStatus.IN_PROGRESS.value,
                    ]
                ),
            ),
        )

        automation_triggers_active = await self._count(
            AutomationTrigger,
            AutomationTrigger.status == AutomationStatus.ACTIVE.value,
        )
        automation_runs_failed = await self._count(
            AutomationRun,
            AutomationRun.status == AutomationRunStatus.FAILED.value,
        )
        automation_next_runs = await self._count(
            AutomationTrigger,
            and_(
                AutomationTrigger.next_run_at.is_not(None),
                AutomationTrigger.status == AutomationStatus.ACTIVE.value,
            ),
        )

        performance_metrics_total = await self._count(PerformanceMetricDefinition)
        performance_values_total = await self._count(PerformanceMetricValue)

        notification_messages_total = await self._count(NotificationMessage)
        notification_messages_failed = await self._count(
            NotificationMessage,
            NotificationMessage.status == "failed",
        )

        return DashboardSummary(
            data_products_total=data_products_total,
            data_products_active=data_products_active,
            data_products_with_quality_warning=data_products_with_quality_warning,
            data_products_with_quality_critical=data_products_with_quality_critical,
            work_items_total=work_items_total,
            work_items_open=work_items_open,
            work_items_overdue=work_items_overdue,
            work_items_technical_debt=work_items_technical_debt,
            work_items_risks=work_items_risks,
            projects_total=projects_total,
            projects_active=projects_active,
            internal_projects_total=internal_projects_total,
            internal_projects_active=internal_projects_active,
            people_total=people_total,
            people_active=people_active,
            teams_total=teams_total,
            capabilities_total=capabilities_total,
            compliance_checks_total=compliance_checks_total,
            compliance_checks_open=compliance_checks_open,
            compliance_checks_non_compliant=compliance_checks_non_compliant,
            compliance_checks_overdue=compliance_checks_overdue,
            automation_triggers_active=automation_triggers_active,
            automation_runs_failed=automation_runs_failed,
            automation_next_runs=automation_next_runs,
            performance_metrics_total=performance_metrics_total,
            performance_values_total=performance_values_total,
            notification_messages_total=notification_messages_total,
            notification_messages_failed=notification_messages_failed,
        )

    async def get_recent_data_products(self, *, limit: int) -> list[DataProduct]:
        query = self._apply_company_scope(select(DataProduct), DataProduct)
        result = await self._session.scalars(
            query.order_by(DataProduct.updated_at.desc()).limit(limit)
        )
        return list(result.all())

    async def get_high_priority_work_items(self, *, limit: int) -> list[WorkItem]:
        query = self._apply_company_scope(select(WorkItem), WorkItem)
        result = await self._session.scalars(
            query.where(
                WorkItem.priority.in_(HIGH_PRIORITY_VALUES),
                OPEN_WORK_ITEM_FILTER,
            )
            .order_by(
                PRIORITY_SEVERITY_ORDER,
                WorkItem.due_date.asc().nulls_last(),
                WorkItem.updated_at.desc(),
            )
            .limit(limit)
        )
        return list(result.all())

    async def get_project_health(self, *, limit: int) -> list[Project]:
        query = self._apply_company_scope(select(Project), Project)
        result = await self._session.scalars(
            query.where(
                or_(
                    Project.status == ProjectStatus.ACTIVE,
                    Project.health_status.in_(("warning", "critical")),
                )
            )
            .order_by(
                HEALTH_SEVERITY_ORDER,
                Project.target_end_date.asc().nulls_last(),
                Project.name.asc(),
            )
            .limit(limit)
        )
        return list(result.all())

    async def get_project_work_counts(
        self,
        project_ids: list[uuid.UUID],
    ) -> dict[uuid.UUID, ProjectWorkCounts]:
        if not project_ids:
            return {}

        today = date.today()
        query = self._apply_company_scope(
            select(
                WorkItem.project_id,
                func.count(WorkItem.id).filter(OPEN_WORK_ITEM_FILTER).label("open_work_items"),
                func.count(WorkItem.id)
                .filter(
                    and_(
                        WorkItem.due_date.is_not(None),
                        WorkItem.due_date < today,
                        OPEN_WORK_ITEM_FILTER,
                    )
                )
                .label("overdue_work_items"),
            ),
            WorkItem,
        )
        result = await self._session.execute(
            query.where(WorkItem.project_id.in_(project_ids)).group_by(WorkItem.project_id)
        )

        counts: dict[uuid.UUID, ProjectWorkCounts] = {}
        for row in result.all():
            if row.project_id is None:
                continue
            counts[row.project_id] = ProjectWorkCounts(
                open_work_items=int(row.open_work_items or 0),
                overdue_work_items=int(row.overdue_work_items or 0),
            )
        return counts

    async def get_capability_workload(self) -> list[CapabilityWorkloadRow]:
        capability_query = self._apply_company_scope(select(Capability), Capability)
        capabilities = list(
            (await self._session.scalars(capability_query.order_by(Capability.name))).all()
        )
        people_counts = await self._counts_by_capability_id(Person, Person.capability_id)
        active_people_counts = await self._counts_by_capability_id(
            Person,
            Person.capability_id,
            Person.is_active.is_(True),
        )
        open_work_counts = await self._counts_by_capability_id(
            WorkItem,
            WorkItem.capability_id,
            OPEN_WORK_ITEM_FILTER,
        )
        active_project_counts = await self._counts_by_capability_id(
            Project,
            Project.capability_id,
            Project.status == ProjectStatus.ACTIVE,
        )
        active_product_counts = await self._counts_by_capability_id(
            DataProduct,
            DataProduct.capability_id,
            DataProduct.status == DataProductStatus.ACTIVE,
        )

        rows = [
            CapabilityWorkloadRow(
                capability_id=capability.id,
                capability_name=capability.name,
                people_count=people_counts.get(capability.id, 0),
                active_people_count=active_people_counts.get(capability.id, 0),
                open_work_items=open_work_counts.get(capability.id, 0),
                active_projects=active_project_counts.get(capability.id, 0),
                active_data_products=active_product_counts.get(capability.id, 0),
            )
            for capability in capabilities
        ]
        rows.sort(
            key=lambda row: (
                -row.open_work_items,
                -row.active_projects,
                row.capability_name.lower(),
            )
        )
        return rows

    async def get_ownership_gaps(self, *, limit: int) -> list[OwnershipGapCandidate]:
        gaps: list[OwnershipGapCandidate] = []

        data_product_query = self._apply_company_scope(select(DataProduct), DataProduct)
        data_products = await self._session.scalars(data_product_query)
        for product in data_products.all():
            gaps.extend(collect_data_product_gaps(product))

        project_query = self._apply_company_scope(select(Project), Project)
        projects = await self._session.scalars(project_query)
        for project in projects.all():
            gaps.extend(collect_project_gaps(project))

        work_item_query = self._apply_company_scope(select(WorkItem), WorkItem)
        work_items = await self._session.scalars(
            work_item_query.where(OPEN_WORK_ITEM_FILTER, WorkItem.assignee_id.is_(None))
        )
        for work_item in work_items.all():
            gaps.extend(collect_work_item_gaps(work_item))

        return sort_ownership_gaps(gaps)[:limit]

    async def _count(self, model: type[object], *criteria: object) -> int:
        query = select(func.count()).select_from(model)
        query = self._apply_company_scope(query, model)
        for criterion in criteria:
            query = query.where(criterion)
        return int(await self._session.scalar(query) or 0)

    async def _counts_by_capability_id(
        self,
        model: type[object],
        capability_column: object,
        *criteria: object,
    ) -> dict[uuid.UUID, int]:
        query = select(capability_column, func.count()).group_by(capability_column)
        query = self._apply_company_scope(query, model)
        for criterion in criteria:
            query = query.where(criterion)
        result = await self._session.execute(query)
        return {
            capability_id: int(count)
            for capability_id, count in result.all()
            if capability_id is not None
        }


@dataclass
class CapabilityWorkloadRow:
    capability_id: uuid.UUID
    capability_name: str
    people_count: int
    active_people_count: int
    open_work_items: int
    active_projects: int
    active_data_products: int
