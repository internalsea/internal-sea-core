"""Deterministic actionable insight generation for the dashboard."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime

from app.domain.enums import DataProductStatus, ProjectStatus, WorkItemPriority
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.dashboard.gaps import OwnershipGapCandidate
from app.modules.dashboard.schemas import ActionableInsight

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}


@dataclass
class InsightContext:
    ownership_gaps: list[OwnershipGapCandidate]
    overdue_work_items: list[WorkItem]
    old_technical_debt: list[WorkItem]
    at_risk_projects: list[Project]
    overdue_compliance_checks: list[ComplianceCheck]
    non_compliant_checks: list[ComplianceCheck]
    missing_evidence_checks: list[ComplianceCheck]
    weak_performance: list[tuple[str, uuid.UUID, str, float]]
    failed_automation_count: int
    due_automation_triggers: int
    failed_notification_count: int


def _insight_id(
    category: str, entity_type: str | None, entity_id: uuid.UUID | None, rule: str
) -> str:
    raw = f"{category}:{entity_type}:{entity_id}:{rule}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _entity_url(entity_type: str | None, entity_id: uuid.UUID | None) -> str | None:
    if not entity_type or not entity_id:
        return None
    routes = {
        "data_product": f"/data-products/{entity_id}",
        "work_item": f"/work-items/{entity_id}",
        "project": f"/projects/{entity_id}",
        "internal_project": f"/internal-projects/{entity_id}",
        "compliance_check": f"/compliance/checks/{entity_id}",
    }
    return routes.get(entity_type)


def build_actionable_insights(ctx: InsightContext, *, limit: int = 20) -> list[ActionableInsight]:
    insights: list[ActionableInsight] = []

    for gap in ctx.ownership_gaps:
        if gap.entity_type == "data_product" and gap.gap_type == "missing_business_owner":
            insights.append(
                ActionableInsight(
                    id=_insight_id("ownership", gap.entity_type, gap.entity_id, gap.gap_type),
                    category="ownership",
                    severity="critical" if gap.severity == "high" else "warning",
                    title="Data product is missing business owner",
                    description=gap.description,
                    entity_type=gap.entity_type,
                    entity_id=gap.entity_id,
                    recommended_action="Assign business owner",
                    url=_entity_url(gap.entity_type, gap.entity_id),
                )
            )
        elif gap.entity_type == "data_product" and gap.gap_type == "missing_technical_owner":
            insights.append(
                ActionableInsight(
                    id=_insight_id("ownership", gap.entity_type, gap.entity_id, gap.gap_type),
                    category="ownership",
                    severity="warning",
                    title="Data product is missing technical owner",
                    description=gap.description,
                    entity_type=gap.entity_type,
                    entity_id=gap.entity_id,
                    recommended_action="Assign technical owner",
                    url=_entity_url(gap.entity_type, gap.entity_id),
                )
            )

    for item in ctx.overdue_work_items:
        priority = WorkItemPriority(item.priority) if item.priority else WorkItemPriority.MEDIUM
        severity = "critical" if priority == WorkItemPriority.CRITICAL else "warning"
        insights.append(
            ActionableInsight(
                id=_insight_id("delivery", "work_item", item.id, "overdue"),
                category="delivery",
                severity=severity,
                title=f"Overdue work item: {item.title}",
                description=f"Due date passed with status {item.status}.",
                entity_type="work_item",
                entity_id=item.id,
                recommended_action="Review due date and assignee",
                url=_entity_url("work_item", item.id),
            )
        )

    for item in ctx.old_technical_debt:
        insights.append(
            ActionableInsight(
                id=_insight_id("delivery", "work_item", item.id, "stale_technical_debt"),
                category="delivery",
                severity="warning",
                title=f"Stale technical debt: {item.title}",
                description="Technical debt item older than 30 days.",
                entity_type="work_item",
                entity_id=item.id,
                recommended_action="Prioritize or schedule remediation",
                url=_entity_url("work_item", item.id),
            )
        )

    for project in ctx.at_risk_projects:
        entity_type = (
            "internal_project"
            if str(project.project_type) == "internal_project"
            or getattr(project.project_type, "value", project.project_type) == "internal_project"
            else "project"
        )
        insights.append(
            ActionableInsight(
                id=_insight_id("project_health", entity_type, project.id, "at_risk"),
                category="project_health",
                severity="critical",
                title=f"Project at risk: {project.name}",
                description=(
                    "Active project with warning/critical health or passed target end date."
                ),
                entity_type=entity_type,
                entity_id=project.id,
                recommended_action="Review project health and delivery plan",
                url=_entity_url(entity_type, project.id),
            )
        )

    for check in ctx.overdue_compliance_checks:
        insights.append(
            ActionableInsight(
                id=_insight_id("compliance", "compliance_check", check.id, "overdue"),
                category="compliance",
                severity="critical",
                title=f"Compliance check overdue: {check.title}",
                description="Check is past due date and still open.",
                entity_type="compliance_check",
                entity_id=check.id,
                recommended_action="Complete or reschedule the check",
                url=_entity_url("compliance_check", check.id),
            )
        )

    for check in ctx.non_compliant_checks:
        insights.append(
            ActionableInsight(
                id=_insight_id("compliance", "compliance_check", check.id, "non_compliant"),
                category="compliance",
                severity="critical",
                title=f"Non-compliant check: {check.title}",
                description=check.result_summary or "Check marked non-compliant.",
                entity_type="compliance_check",
                entity_id=check.id,
                recommended_action="Remediate and re-assess compliance",
                url=_entity_url("compliance_check", check.id),
            )
        )

    for check in ctx.missing_evidence_checks:
        insights.append(
            ActionableInsight(
                id=_insight_id("compliance", "compliance_check", check.id, "missing_evidence"),
                category="compliance",
                severity="warning",
                title=f"Missing evidence: {check.title}",
                description="Open compliance check without attached evidence.",
                entity_type="compliance_check",
                entity_id=check.id,
                recommended_action="Attach supporting evidence",
                url=_entity_url("compliance_check", check.id),
            )
        )

    for subject_type, subject_id, metric_name, score in ctx.weak_performance:
        severity = "critical" if score < 60 else "warning"
        insights.append(
            ActionableInsight(
                id=_insight_id("performance", subject_type, subject_id, metric_name),
                category="performance",
                severity=severity,
                title=f"Weak performance: {metric_name}",
                description=f"Score {score:.0f} is below target threshold.",
                entity_type=subject_type,
                entity_id=subject_id,
                recommended_action="Review metric values and improvement plan",
                url=None,
            )
        )

    if ctx.failed_automation_count > 0:
        insights.append(
            ActionableInsight(
                id=_insight_id("automation", None, None, "failed_runs"),
                category="automation",
                severity="warning",
                title=f"{ctx.failed_automation_count} failed automation run(s)",
                description="Review automation run history for errors.",
                entity_type=None,
                entity_id=None,
                recommended_action="Inspect failed runs on Automation page",
                url="/automation",
            )
        )

    if ctx.due_automation_triggers > 0:
        insights.append(
            ActionableInsight(
                id=_insight_id("automation", None, None, "due_triggers"),
                category="automation",
                severity="info" if ctx.due_automation_triggers <= 2 else "warning",
                title=f"{ctx.due_automation_triggers} automation trigger(s) due",
                description="Scheduled triggers are waiting for worker processing.",
                entity_type=None,
                entity_id=None,
                recommended_action="Run worker or review automation queue",
                url="/automation",
            )
        )

    if ctx.failed_notification_count > 0:
        insights.append(
            ActionableInsight(
                id=_insight_id("notifications", None, None, "failed_messages"),
                category="notifications",
                severity="warning",
                title=f"{ctx.failed_notification_count} failed notification(s)",
                description="Review notification delivery attempts.",
                entity_type=None,
                entity_id=None,
                recommended_action="Inspect notifications page",
                url="/notifications",
            )
        )

    insights.sort(key=lambda item: (SEVERITY_ORDER.get(item.severity, 3), item.title.lower()))
    return insights[:limit]


def is_project_at_risk(project: Project, *, today: date) -> bool:
    if project.status != ProjectStatus.ACTIVE:
        return False
    if project.health_status in ("warning", "critical"):
        return True
    if project.target_end_date and project.target_end_date < today:
        return True
    return False


def is_stale_technical_debt(item: WorkItem, *, cutoff: datetime) -> bool:
    from app.domain.enums import WorkItemType

    if item.type != WorkItemType.TECHNICAL_DEBT:
        return False
    created = item.created_at
    if created is None:
        return False
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return created < cutoff


def active_product_missing_owner(product: DataProduct) -> bool:
    return product.status == DataProductStatus.ACTIVE and product.business_owner_id is None
