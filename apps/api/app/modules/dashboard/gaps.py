"""Ownership gap detection and severity rules for the dashboard."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domain.enums import DataProductStatus, ProjectStatus
from app.models.catalog import DataProduct
from app.models.projects import Project
from app.models.work import WorkItem


@dataclass(frozen=True)
class OwnershipGapCandidate:
    entity_type: str
    entity_id: uuid.UUID
    name: str
    gap_type: str
    description: str
    severity: str


def resolve_data_product_owner_gap_severity(
    *,
    gap_type: str,
    status: DataProductStatus,
) -> str:
    if gap_type in {"missing_business_owner", "missing_technical_owner"}:
        if status == DataProductStatus.ACTIVE:
            return "high"
        if status == DataProductStatus.DRAFT:
            return "low"
        return "medium"
    if gap_type in {"missing_team", "missing_capability"}:
        return "medium"
    return "low"


def resolve_project_gap_severity(
    *,
    gap_type: str,
    status: ProjectStatus,
) -> str:
    if gap_type == "missing_owner":
        if status == ProjectStatus.ACTIVE:
            return "high"
        if status in {ProjectStatus.PLANNED, ProjectStatus.IDEA}:
            return "low"
        return "medium"
    if gap_type == "missing_team":
        return "medium"
    return "low"


def resolve_work_item_gap_severity() -> str:
    return "medium"


def collect_data_product_gaps(product: DataProduct) -> list[OwnershipGapCandidate]:
    gaps: list[OwnershipGapCandidate] = []
    checks: list[tuple[str, bool, str]] = [
        (
            "missing_business_owner",
            product.business_owner_id is None,
            "Active catalog object without a business owner.",
        ),
        (
            "missing_technical_owner",
            product.technical_owner_id is None,
            "Catalog object without a technical owner.",
        ),
        (
            "missing_team",
            product.team_id is None,
            "Catalog object without an assigned delivery team.",
        ),
        (
            "missing_capability",
            product.capability_id is None,
            "Catalog object without a capability assignment.",
        ),
    ]
    for gap_type, is_missing, description in checks:
        if not is_missing:
            continue
        gaps.append(
            OwnershipGapCandidate(
                entity_type="data_product",
                entity_id=product.id,
                name=product.name,
                gap_type=gap_type,
                description=description,
                severity=resolve_data_product_owner_gap_severity(
                    gap_type=gap_type,
                    status=product.status,
                ),
            )
        )
    return gaps


def collect_project_gaps(project: Project) -> list[OwnershipGapCandidate]:
    gaps: list[OwnershipGapCandidate] = []
    checks: list[tuple[str, bool, str]] = [
        (
            "missing_owner",
            project.owner_id is None,
            "Project without an accountable owner.",
        ),
        (
            "missing_team",
            project.team_id is None,
            "Project without an assigned delivery team.",
        ),
    ]
    for gap_type, is_missing, description in checks:
        if not is_missing:
            continue
        gaps.append(
            OwnershipGapCandidate(
                entity_type="project",
                entity_id=project.id,
                name=project.name,
                gap_type=gap_type,
                description=description,
                severity=resolve_project_gap_severity(gap_type=gap_type, status=project.status),
            )
        )
    return gaps


def collect_work_item_gaps(work_item: WorkItem) -> list[OwnershipGapCandidate]:
    if work_item.assignee_id is not None:
        return []
    return [
        OwnershipGapCandidate(
            entity_type="work_item",
            entity_id=work_item.id,
            name=work_item.title,
            gap_type="missing_assignee",
            description="Open work item without an assignee.",
            severity=resolve_work_item_gap_severity(),
        )
    ]


SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def sort_ownership_gaps(gaps: list[OwnershipGapCandidate]) -> list[OwnershipGapCandidate]:
    return sorted(
        gaps,
        key=lambda gap: (SEVERITY_ORDER.get(gap.severity, 3), gap.name.lower()),
    )
