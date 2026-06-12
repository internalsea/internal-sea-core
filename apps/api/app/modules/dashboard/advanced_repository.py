"""Advanced dashboard read queries over existing domain tables."""

from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta, timezone
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums import (
    AutomationRunStatus,
    AutomationStatus,
    ComplianceStatus,
    PolicyStatus,
    DataProductStatus,
    MetricStatus,
    ProjectStatus,
    ProjectType,
    QualityStatus,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.models.activity import ActivityEvent
from app.models.automation import AutomationRun, AutomationSchedule, AutomationTrigger
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck, ComplianceRule, Control, Policy
from app.models.notifications import (
    NotificationChannel,
    NotificationDeliveryAttempt,
    NotificationMessage,
    NotificationTemplate,
)
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.dashboard.gaps import sort_ownership_gaps
from app.modules.dashboard.insights import InsightContext, build_actionable_insights, is_project_at_risk, is_stale_technical_debt
from app.modules.dashboard.repository import (
    COMPLETED_WORK_ITEM_STATUSES,
    OPEN_WORK_ITEM_FILTER,
    DashboardRepository,
)
from app.modules.dashboard.scoring import (
    calculate_automation_health_score,
    calculate_compliance_health_score,
    calculate_overall_score,
    calculate_performance_health_score,
    calculate_project_health_score,
    calculate_status_from_score,
    calculate_work_health_score,
)
from app.modules.dashboard.schemas import (
    ActionableInsightsResponse,
    AutomationHealth,
    AutomationRunInsightItem,
    ComplianceCheckInsightItem,
    ComplianceInsights,
    DataProductHealthItem,
    DataProductHealthResponse,
    ExecutiveSummary,
    MetricGapItem,
    NotificationHealth,
    NotificationMessageInsightItem,
    OperationalHealth,
    PerformanceInsights,
    ProjectInsightItem,
    ProjectInsightsResponse,
    RecentActivityItem,
    RecentActivityResponse,
    WorkDeliverySummary,
)
from app.modules.performance.scoring import calculate_metric_score
from app.worker.locks import count_locked_automation_triggers
from app.worker.scheduler import count_due_automation_triggers

OPEN_COMPLIANCE_STATUSES = (
    ComplianceStatus.NOT_STARTED.value,
    ComplianceStatus.IN_PROGRESS.value,
)


def _enum_str(value: object) -> str:
    return str(value.value if hasattr(value, "value") else value)


class AdvancedDashboardRepository:
    def __init__(self, session: AsyncSession, base: DashboardRepository) -> None:
        self._session = session
        self._base = base

    async def get_executive_summary(self) -> ExecutiveSummary:
        summary = await self._base.get_summary()
        ownership_gaps = await self._base.get_ownership_gaps(limit=500)
        due_triggers = await count_due_automation_triggers(self._session)
        avg_perf = await self._average_performance_score()

        work_score = calculate_work_health_score(
            open_work_items=summary.work_items_open,
            overdue_work_items=summary.work_items_overdue,
            critical_items=await self._count_critical_open_work(),
            risks=summary.work_items_risks,
        )
        compliance_score = calculate_compliance_health_score(
            checks_open=summary.compliance_checks_open,
            checks_non_compliant=summary.compliance_checks_non_compliant,
            checks_overdue=summary.compliance_checks_overdue,
            evidence_missing=await self._count_missing_evidence_checks(),
        )
        automation_score = calculate_automation_health_score(
            runs_failed=summary.automation_runs_failed,
            due_triggers=due_triggers,
            locked_triggers=await count_locked_automation_triggers(self._session),
        )
        perf_score = calculate_performance_health_score(avg_perf)
        project_insights = await self.get_project_insights(limit=100)
        project_score = calculate_project_health_score(
            active_projects=summary.projects_active + summary.internal_projects_active,
            warning_or_critical=project_insights.warning_or_critical,
            overdue_or_at_risk=project_insights.overdue_or_at_risk,
        )
        overall = calculate_overall_score(
            work_score, compliance_score, automation_score, perf_score, project_score
        )

        return ExecutiveSummary(
            overall_status=calculate_status_from_score(overall),
            overall_score=overall,
            active_projects=summary.projects_active,
            active_internal_projects=summary.internal_projects_active,
            active_data_products=summary.data_products_active,
            open_work_items=summary.work_items_open,
            overdue_work_items=summary.work_items_overdue,
            compliance_open_checks=summary.compliance_checks_open,
            compliance_overdue_checks=summary.compliance_checks_overdue,
            average_performance_score=avg_perf,
            ownership_gaps=len(ownership_gaps),
            automation_due_triggers=due_triggers,
            notification_failed_messages=summary.notification_messages_failed,
            generated_at=datetime.now(timezone.utc),
        )

    async def get_operational_health(self) -> OperationalHealth:
        summary = await self._base.get_summary()
        due_triggers = await count_due_automation_triggers(self._session)
        locked_triggers = await count_locked_automation_triggers(self._session)
        avg_perf = await self._average_performance_score()
        project_insights = await self.get_project_insights(limit=100)
        evidence_missing = await self._count_missing_evidence_checks()
        critical_count = await self._count_critical_open_work()

        work_score = calculate_work_health_score(
            open_work_items=summary.work_items_open,
            overdue_work_items=summary.work_items_overdue,
            critical_items=critical_count,
            risks=summary.work_items_risks,
        )
        compliance_score = calculate_compliance_health_score(
            checks_open=summary.compliance_checks_open,
            checks_non_compliant=summary.compliance_checks_non_compliant,
            checks_overdue=summary.compliance_checks_overdue,
            evidence_missing=evidence_missing,
        )
        automation_score = calculate_automation_health_score(
            runs_failed=summary.automation_runs_failed,
            due_triggers=due_triggers,
            locked_triggers=locked_triggers,
        )
        perf_score = calculate_performance_health_score(avg_perf)
        project_score = calculate_project_health_score(
            active_projects=summary.projects_active + summary.internal_projects_active,
            warning_or_critical=project_insights.warning_or_critical,
            overdue_or_at_risk=project_insights.overdue_or_at_risk,
        )
        overall = calculate_overall_score(
            work_score, compliance_score, automation_score, perf_score, project_score
        )

        return OperationalHealth(
            status=calculate_status_from_score(overall),
            work_health_score=work_score,
            project_health_score=project_score,
            compliance_health_score=compliance_score,
            performance_health_score=perf_score,
            automation_health_score=automation_score,
            risk_items_count=summary.work_items_risks,
            critical_work_items_count=critical_count,
            overdue_items_count=summary.work_items_overdue,
            blocked_or_warning_projects=project_insights.warning_or_critical,
            generated_at=datetime.now(timezone.utc),
        )

    async def get_data_product_health(self, *, limit: int) -> DataProductHealthResponse:
        products = list(
            (await self._session.scalars(select(DataProduct).order_by(DataProduct.name))).all()
        )
        active = [p for p in products if p.status == DataProductStatus.ACTIVE]
        good_q = sum(1 for p in products if p.quality_status == QualityStatus.GOOD)
        warn_q = sum(1 for p in products if p.quality_status == QualityStatus.WARNING)
        crit_q = sum(1 for p in products if p.quality_status == QualityStatus.CRITICAL)
        missing_owner = sum(
            1
            for p in active
            if p.business_owner_id is None or p.technical_owner_id is None
        )

        work_counts = await self._open_work_by_data_product()
        compliance_counts = await self._open_compliance_by_subject("data_product")
        perf_scores = await self._latest_product_performance_scores()

        items: list[DataProductHealthItem] = []
        for product in active[:limit]:
            reasons: list[str] = []
            health = "good"
            if product.quality_status == QualityStatus.CRITICAL:
                health = "critical"
                reasons.append("Critical quality status")
            elif product.quality_status == QualityStatus.WARNING:
                health = "warning"
                reasons.append("Warning quality status")
            if product.business_owner_id is None:
                health = "critical" if health != "critical" else health
                if health == "critical":
                    reasons.append("Missing business owner")
                else:
                    health = "critical"
                    reasons.append("Missing business owner")
            elif product.technical_owner_id is None:
                if health == "good":
                    health = "warning"
                reasons.append("Missing technical owner")

            open_work = work_counts.get(product.id, 0)
            open_checks = compliance_counts.get(product.id, 0)
            if open_checks > 0 and health == "good":
                health = "warning"
                reasons.append(f"{open_checks} open compliance check(s)")

            items.append(
                DataProductHealthItem(
                    id=product.id,
                    name=product.name,
                    status=_enum_str(product.status),
                    quality_status=_enum_str(product.quality_status),
                    business_owner_id=product.business_owner_id,
                    technical_owner_id=product.technical_owner_id,
                    team_id=product.team_id,
                    capability_id=product.capability_id,
                    open_work_items=open_work,
                    compliance_open_checks=open_checks,
                    latest_performance_score=perf_scores.get(product.id),
                    health_status=health,
                    health_reasons=reasons,
                )
            )
        items.sort(key=lambda i: ({"critical": 0, "warning": 1, "good": 2}.get(i.health_status, 3), i.name))

        return DataProductHealthResponse(
            total=len(products),
            active=len(active),
            good_quality=good_q,
            warning_quality=warn_q,
            critical_quality=crit_q,
            missing_owner_count=missing_owner,
            items=items,
        )

    async def get_work_delivery(self) -> WorkDeliverySummary:
        summary = await self._base.get_summary()
        done = summary.work_items_total - summary.work_items_open
        critical = await self._count_critical_open_work()
        by_status = await self._group_count(WorkItem, WorkItem.status)
        by_priority = await self._group_count(WorkItem, WorkItem.priority)
        by_type = await self._group_count(WorkItem, WorkItem.type)
        return WorkDeliverySummary(
            total_work_items=summary.work_items_total,
            open_work_items=summary.work_items_open,
            done_work_items=done,
            overdue_work_items=summary.work_items_overdue,
            critical_items=critical,
            risks=summary.work_items_risks,
            technical_debt=summary.work_items_technical_debt,
            by_status={_enum_str(k): v for k, v in by_status.items()},
            by_priority={_enum_str(k): v for k, v in by_priority.items()},
            by_type={_enum_str(k): v for k, v in by_type.items()},
        )

    async def get_project_insights(self, *, limit: int) -> ProjectInsightsResponse:
        today = date.today()
        projects = list((await self._session.scalars(select(Project))).all())
        active = [p for p in projects if p.status == ProjectStatus.ACTIVE]
        work_counts = await self._base.get_project_work_counts([p.id for p in projects])
        risk_counts = await self._risk_count_by_project()
        compliance_counts = await self._open_compliance_by_all_subjects()
        perf_scores = await self._latest_project_performance_scores()

        warning_or_critical = 0
        overdue_or_at_risk = 0
        items: list[ProjectInsightItem] = []

        for project in projects:
            counts = work_counts.get(project.id)
            open_wi = counts.open_work_items if counts else 0
            overdue_wi = counts.overdue_work_items if counts else 0
            reasons: list[str] = []
            insight_status = "good"

            if project.health_status == "critical":
                insight_status = "critical"
                reasons.append("Critical health status")
            elif project.health_status == "warning":
                insight_status = "warning"
                reasons.append("Warning health status")

            if overdue_wi > 0:
                if insight_status != "critical":
                    insight_status = "warning"
                reasons.append(f"{overdue_wi} overdue work item(s)")
                overdue_or_at_risk += 1

            if project.target_end_date and project.target_end_date < today and project.status == ProjectStatus.ACTIVE:
                insight_status = "critical"
                reasons.append("Past target end date")
                overdue_or_at_risk += 1

            if project.health_status in ("warning", "critical"):
                warning_or_critical += 1

            entity_key = str(project.id)
            open_checks = compliance_counts.get(entity_key, 0)

            items.append(
                ProjectInsightItem(
                    id=project.id,
                    name=project.name,
                    project_type=_enum_str(project.project_type),
                    status=_enum_str(project.status),
                    health_status=project.health_status,
                    target_end_date=project.target_end_date,
                    open_work_items=open_wi,
                    overdue_work_items=overdue_wi,
                    risks=risk_counts.get(project.id, 0),
                    compliance_open_checks=open_checks,
                    performance_score=perf_scores.get(project.id),
                    insight_status=insight_status,
                    insight_reasons=reasons,
                )
            )

        severity_order = {"critical": 0, "warning": 1, "good": 2}
        items.sort(key=lambda i: (severity_order.get(i.insight_status, 3), i.name.lower()))

        return ProjectInsightsResponse(
            total=len(projects),
            active=len(active),
            warning_or_critical=warning_or_critical,
            overdue_or_at_risk=overdue_or_at_risk,
            items=items[:limit],
        )

    async def get_compliance_insights(self, *, limit: int) -> ComplianceInsights:
        today = date.today()
        policies_active = await self._count(Policy, Policy.status == PolicyStatus.ACTIVE.value)
        active_rules = await self._count(ComplianceRule, ComplianceRule.is_active.is_(True))
        active_controls = await self._count(Control, Control.status == "active")
        checks_total = await self._count(ComplianceCheck)
        checks_open = await self._count(ComplianceCheck, ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES))
        checks_compliant = await self._count(
            ComplianceCheck, ComplianceCheck.status == ComplianceStatus.COMPLIANT.value
        )
        checks_non_compliant = await self._count(
            ComplianceCheck, ComplianceCheck.status == ComplianceStatus.NON_COMPLIANT.value
        )
        checks_overdue = await self._count(
            ComplianceCheck,
            and_(
                ComplianceCheck.due_date.is_not(None),
                ComplianceCheck.due_date < today,
                ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES),
            ),
        )
        evidence_missing = await self._count_missing_evidence_checks()
        by_status = await self._group_count(ComplianceCheck, ComplianceCheck.status)

        overdue_result = await self._session.scalars(
            select(ComplianceCheck)
            .where(
                ComplianceCheck.due_date.is_not(None),
                ComplianceCheck.due_date < today,
                ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES),
            )
            .order_by(ComplianceCheck.due_date.asc())
            .limit(limit)
        )
        top_overdue = [
            ComplianceCheckInsightItem(
                id=check.id,
                title=check.title,
                subject_type=check.subject_type,
                subject_id=check.subject_id,
                status=check.status,
                due_date=check.due_date,
                owner_id=check.owner_id,
            )
            for check in overdue_result.all()
        ]

        return ComplianceInsights(
            policies_active=policies_active,
            active_rules=active_rules,
            active_controls=active_controls,
            checks_total=checks_total,
            checks_open=checks_open,
            checks_compliant=checks_compliant,
            checks_non_compliant=checks_non_compliant,
            checks_overdue=checks_overdue,
            evidence_missing=evidence_missing,
            by_status=by_status,
            top_overdue_checks=top_overdue,
        )

    async def get_performance_insights(self, *, limit: int) -> PerformanceInsights:
        definitions = list(
            (
                await self._session.scalars(
                    select(PerformanceMetricDefinition).where(
                        PerformanceMetricDefinition.status == MetricStatus.ACTIVE.value
                    )
                )
            ).all()
        )
        values_total = await self._count(PerformanceMetricValue)
        gaps: list[MetricGapItem] = []
        subject_scores: dict[tuple[str, uuid.UUID], list[float]] = {}

        for definition in definitions:
            latest = await self._session.scalar(
                select(PerformanceMetricValue)
                .where(PerformanceMetricValue.metric_definition_id == definition.id)
                .order_by(PerformanceMetricValue.period_end.desc())
                .limit(1)
            )
            if latest is None:
                continue
            score = calculate_metric_score(definition, latest)
            if score is None:
                continue
            score_f = float(score)
            key = (latest.subject_type, latest.subject_id)
            subject_scores.setdefault(key, []).append(score_f)
            target = float(definition.target_value) if definition.target_value else None
            current = float(latest.value_numeric) if latest.value_numeric else None
            if score_f < 85:
                gaps.append(
                    MetricGapItem(
                        subject_type=latest.subject_type,
                        subject_id=latest.subject_id,
                        metric_definition_id=definition.id,
                        metric_name=definition.name,
                        current_value=current,
                        target_value=target,
                        score=score_f,
                        trend=None,
                    )
                )

        gaps.sort(key=lambda g: (g.score or 100))
        averages = [
            sum(scores) / len(scores) for scores in subject_scores.values() if scores
        ]
        avg_score = sum(averages) / len(averages) if averages else None
        weak = sum(1 for a in averages if a < 70)

        return PerformanceInsights(
            metric_definitions_active=len(definitions),
            metric_values_total=values_total,
            average_score=round(avg_score, 2) if avg_score is not None else None,
            scorecards_with_values=len(subject_scores),
            weak_scorecards_count=weak,
            top_metric_gaps=gaps[:limit],
        )

    async def get_automation_health(self, *, limit: int) -> AutomationHealth:
        schedules_active = await self._count(
            AutomationSchedule, AutomationSchedule.is_active.is_(True)
        )
        triggers_active = await self._count(
            AutomationTrigger, AutomationTrigger.status == AutomationStatus.ACTIVE.value
        )
        due_triggers = await count_due_automation_triggers(self._session)
        locked_triggers = await count_locked_automation_triggers(self._session)
        runs_total = await self._count(AutomationRun)
        runs_failed = await self._count(
            AutomationRun, AutomationRun.status == AutomationRunStatus.FAILED.value
        )
        runs_succeeded = await self._count(
            AutomationRun, AutomationRun.status == AutomationRunStatus.SUCCEEDED.value
        )
        runs_simulated = await self._count(
            AutomationRun, AutomationRun.status == AutomationRunStatus.SIMULATED.value
        )

        failed_runs = list(
            (
                await self._session.scalars(
                    select(AutomationRun)
                    .where(AutomationRun.status == AutomationRunStatus.FAILED.value)
                    .order_by(AutomationRun.created_at.desc())
                    .limit(limit)
                )
            ).all()
        )

        return AutomationHealth(
            schedules_active=schedules_active,
            triggers_active=triggers_active,
            due_triggers=due_triggers,
            locked_triggers=locked_triggers,
            runs_total=runs_total,
            runs_failed=runs_failed,
            runs_succeeded=runs_succeeded,
            runs_simulated=runs_simulated,
            recent_failed_runs=[
                AutomationRunInsightItem(
                    id=run.id,
                    trigger_id=run.trigger_id,
                    status=run.status,
                    action_type=run.action_type,
                    target_type=run.target_type,
                    target_id=run.target_id,
                    error_message=run.error_message,
                    created_at=run.created_at,
                )
                for run in failed_runs
            ],
        )

    async def get_notification_health(self, *, limit: int) -> NotificationHealth:
        channels_active = await self._count(
            NotificationChannel, NotificationChannel.status == "active"
        )
        templates_active = await self._count(
            NotificationTemplate, NotificationTemplate.status == "active"
        )
        messages_total = await self._count(NotificationMessage)
        messages_queued = await self._count(NotificationMessage, NotificationMessage.status == "queued")
        messages_failed = await self._count(
            NotificationMessage, NotificationMessage.status == "failed"
        )
        delivery_attempts_failed = await self._count(
            NotificationDeliveryAttempt,
            NotificationDeliveryAttempt.status == "failed",
        )

        failed_messages = list(
            (
                await self._session.scalars(
                    select(NotificationMessage)
                    .where(NotificationMessage.status == "failed")
                    .order_by(NotificationMessage.updated_at.desc())
                    .limit(limit)
                )
            ).all()
        )

        return NotificationHealth(
            channels_active=channels_active,
            templates_active=templates_active,
            messages_total=messages_total,
            messages_queued=messages_queued,
            messages_failed=messages_failed,
            delivery_attempts_failed=delivery_attempts_failed,
            recent_failed_messages=[
                NotificationMessageInsightItem(
                    id=msg.id,
                    status=msg.status,
                    priority=msg.priority,
                    event_type=msg.event_type,
                    subject=msg.subject,
                    recipient_value=msg.recipient_value,
                    error_message=msg.error_message,
                    updated_at=msg.updated_at,
                )
                for msg in failed_messages
            ],
        )

    async def get_recent_activity(self, *, limit: int) -> RecentActivityResponse:
        total = await self._count(ActivityEvent)
        result = await self._session.scalars(
            select(ActivityEvent).order_by(ActivityEvent.created_at.desc()).limit(limit)
        )
        items = [
            RecentActivityItem(
                id=event.id,
                entity_type=event.entity_type,
                entity_id=event.entity_id,
                action=event.action,
                title=event.title,
                description=event.description,
                actor_id=event.actor_id,
                created_at=event.created_at,
            )
            for event in result.all()
        ]
        return RecentActivityResponse(items=items, total=total)

    async def get_actionable_insights(self, *, limit: int) -> ActionableInsightsResponse:
        today = date.today()
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        ownership_gaps = sort_ownership_gaps(await self._base.get_ownership_gaps(limit=100))

        overdue_work = list(
            (
                await self._session.scalars(
                    select(WorkItem).where(
                        WorkItem.due_date.is_not(None),
                        WorkItem.due_date < today,
                        OPEN_WORK_ITEM_FILTER,
                    )
                )
            ).all()
        )
        old_debt = [
            item
            for item in (
                await self._session.scalars(
                    select(WorkItem).where(WorkItem.type == WorkItemType.TECHNICAL_DEBT)
                )
            ).all()
            if is_stale_technical_debt(item, cutoff=cutoff)
        ]

        projects = list((await self._session.scalars(select(Project))).all())
        at_risk = [p for p in projects if is_project_at_risk(p, today=today)]

        overdue_checks = list(
            (
                await self._session.scalars(
                    select(ComplianceCheck)
                    .options(selectinload(ComplianceCheck.evidence_items))
                    .where(
                        ComplianceCheck.due_date.is_not(None),
                        ComplianceCheck.due_date < today,
                        ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES),
                    )
                )
            ).all()
        )
        non_compliant = list(
            (
                await self._session.scalars(
                    select(ComplianceCheck).where(
                        ComplianceCheck.status == ComplianceStatus.NON_COMPLIANT.value
                    )
                )
            ).all()
        )
        missing_evidence = list(
            (
                await self._session.scalars(
                    select(ComplianceCheck)
                    .options(selectinload(ComplianceCheck.evidence_items))
                    .where(ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES))
                )
            ).all()
        )
        missing_evidence = [c for c in missing_evidence if len(c.evidence_items) == 0]

        perf = await self.get_performance_insights(limit=20)
        weak_perf = [
            (g.subject_type, g.subject_id, g.metric_name, g.score or 0)
            for g in perf.top_metric_gaps
            if g.score is not None and g.score < 70
        ]

        summary = await self._base.get_summary()
        due_triggers = await count_due_automation_triggers(self._session)

        ctx = InsightContext(
            ownership_gaps=ownership_gaps,
            overdue_work_items=overdue_work,
            old_technical_debt=old_debt,
            at_risk_projects=at_risk,
            overdue_compliance_checks=overdue_checks,
            non_compliant_checks=non_compliant,
            missing_evidence_checks=missing_evidence,
            weak_performance=weak_perf,
            failed_automation_count=summary.automation_runs_failed,
            due_automation_triggers=due_triggers,
            failed_notification_count=summary.notification_messages_failed,
        )
        items = build_actionable_insights(ctx, limit=limit)
        return ActionableInsightsResponse(
            items=items,
            total=len(items),
            critical_count=sum(1 for i in items if i.severity == "critical"),
            warning_count=sum(1 for i in items if i.severity == "warning"),
            info_count=sum(1 for i in items if i.severity == "info"),
        )

    async def _count(self, model: type[object], *criteria: object) -> int:
        query = select(func.count()).select_from(model)
        for criterion in criteria:
            query = query.where(criterion)
        return int(await self._session.scalar(query) or 0)

    async def _count_critical_open_work(self) -> int:
        return await self._count(
            WorkItem,
            OPEN_WORK_ITEM_FILTER,
            WorkItem.priority == WorkItemPriority.CRITICAL,
        )

    async def _count_missing_evidence_checks(self) -> int:
        checks = list(
            (
                await self._session.scalars(
                    select(ComplianceCheck)
                    .options(selectinload(ComplianceCheck.evidence_items))
                    .where(ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES))
                )
            ).all()
        )
        return sum(1 for check in checks if len(check.evidence_items) == 0)

    async def _group_count(self, model: type[object], column: object) -> dict[str, int]:
        result = await self._session.execute(
            select(column, func.count()).select_from(model).group_by(column)
        )
        return {_enum_str(row[0]): int(row[1]) for row in result.all() if row[0] is not None}

    async def _open_work_by_data_product(self) -> dict[uuid.UUID, int]:
        result = await self._session.execute(
            select(WorkItem.data_product_id, func.count())
            .where(OPEN_WORK_ITEM_FILTER, WorkItem.data_product_id.is_not(None))
            .group_by(WorkItem.data_product_id)
        )
        return {row[0]: int(row[1]) for row in result.all() if row[0]}

    async def _open_compliance_by_subject(self, subject_type: str) -> dict[uuid.UUID, int]:
        result = await self._session.execute(
            select(ComplianceCheck.subject_id, func.count())
            .where(
                ComplianceCheck.subject_type == subject_type,
                ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES),
            )
            .group_by(ComplianceCheck.subject_id)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def _open_compliance_by_all_subjects(self) -> dict[str, int]:
        result = await self._session.execute(
            select(ComplianceCheck.subject_id, func.count())
            .where(ComplianceCheck.status.in_(OPEN_COMPLIANCE_STATUSES))
            .group_by(ComplianceCheck.subject_id)
        )
        return {str(row[0]): int(row[1]) for row in result.all()}

    async def _risk_count_by_project(self) -> dict[uuid.UUID, int]:
        result = await self._session.execute(
            select(WorkItem.project_id, func.count())
            .where(WorkItem.type == WorkItemType.RISK, OPEN_WORK_ITEM_FILTER)
            .group_by(WorkItem.project_id)
        )
        return {row[0]: int(row[1]) for row in result.all() if row[0]}

    async def _average_performance_score(self) -> float | None:
        definitions = {
            d.id: d
            for d in (
                await self._session.scalars(
                    select(PerformanceMetricDefinition).where(
                        PerformanceMetricDefinition.status == MetricStatus.ACTIVE.value
                    )
                )
            ).all()
        }
        if not definitions:
            return None
        values = list((await self._session.scalars(select(PerformanceMetricValue))).all())
        subject_scores: dict[tuple[str, uuid.UUID], list[float]] = {}
        seen: set[tuple[uuid.UUID, str, uuid.UUID]] = set()
        for value in values:
            definition = definitions.get(value.metric_definition_id)
            if definition is None:
                continue
            dedupe_key = (value.metric_definition_id, value.subject_type, value.subject_id)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            score = calculate_metric_score(definition, value)
            if score is None:
                continue
            key = (value.subject_type, value.subject_id)
            subject_scores.setdefault(key, []).append(float(score))
        if not subject_scores:
            return None
        averages = [sum(s) / len(s) for s in subject_scores.values()]
        return round(sum(averages) / len(averages), 2)

    async def _latest_product_performance_scores(self) -> dict[uuid.UUID, float]:
        return await self._latest_subject_scores("data_product")

    async def _latest_project_performance_scores(self) -> dict[uuid.UUID, float]:
        scores: dict[uuid.UUID, float] = {}
        for subject_type in ("project", "internal_project"):
            partial = await self._latest_subject_scores(subject_type)
            scores.update(partial)
        return scores

    async def _latest_subject_scores(self, subject_type: str) -> dict[uuid.UUID, float]:
        definitions = {
            d.id: d
            for d in (
                await self._session.scalars(
                    select(PerformanceMetricDefinition).where(
                        PerformanceMetricDefinition.status == MetricStatus.ACTIVE.value
                    )
                )
            ).all()
        }
        values = list(
            (
                await self._session.scalars(
                    select(PerformanceMetricValue).where(
                        PerformanceMetricValue.subject_type == subject_type
                    )
                )
            ).all()
        )
        by_subject: dict[uuid.UUID, list[float]] = {}
        for value in values:
            definition = definitions.get(value.metric_definition_id)
            if definition is None:
                continue
            score = calculate_metric_score(definition, value)
            if score is None:
                continue
            by_subject.setdefault(value.subject_id, []).append(float(score))
        return {
            subject_id: round(sum(scores) / len(scores), 2)
            for subject_id, scores in by_subject.items()
            if scores
        }
