"""Seed helpers for default SaaS tenant."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import (
    CompanyMemberRole,
    CompanyMemberStatus,
    CompanySize,
    CompanyStatus,
    Industry,
    WorkspaceStatus,
)
from app.models.activity import ActivityEvent
from app.models.automation import AutomationRun, AutomationSchedule, AutomationTrigger
from app.models.catalog import BusinessDomain, DataProduct
from app.models.compliance import (
    ComplianceCheck,
    ComplianceCheckEvidence,
    ComplianceRule,
    Control,
    Policy,
)
from app.models.files import FileAsset, FileAttachment, FileStorage
from app.models.identity import User
from app.models.notifications import (
    NotificationChannel,
    NotificationDeliveryAttempt,
    NotificationMessage,
    NotificationPreference,
    NotificationTemplate,
)
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.models.relationships import EntityLink
from app.models.tenancy import Company, CompanyMember, Workspace
from app.models.work import Comment, WorkItem

DEMO_COMPANY_SLUG = "internal-sea-demo"
DEMO_WORKSPACE_SLUG = "default"

COMPANY_WORKSPACE_MODELS = (
    Person,
    Team,
    Capability,
    BusinessDomain,
    DataProduct,
    WorkItem,
    Project,
    EntityLink,
    FileAsset,
    FileAttachment,
    ComplianceCheck,
    AutomationTrigger,
    PerformanceMetricValue,
    NotificationMessage,
)

COMPANY_ONLY_MODELS = (
    Comment,
    ActivityEvent,
    FileStorage,
    Policy,
    ComplianceRule,
    Control,
    ComplianceCheckEvidence,
    AutomationSchedule,
    AutomationRun,
    PerformanceMetricDefinition,
    NotificationChannel,
    NotificationTemplate,
    NotificationPreference,
    NotificationDeliveryAttempt,
)

DEMO_MEMBER_ROLES = {
    "admin@example.com": CompanyMemberRole.OWNER,
    "editor@example.com": CompanyMemberRole.EDITOR,
    "viewer@example.com": CompanyMemberRole.VIEWER,
}


async def get_or_create_demo_tenant(session: AsyncSession) -> tuple[Company, Workspace]:
    result = await session.execute(select(Company).where(Company.slug == DEMO_COMPANY_SLUG))
    company = result.scalar_one_or_none()
    if company is None:
        company = Company(
            name="Internal Sea Demo",
            slug=DEMO_COMPANY_SLUG,
            description="Default demo company for local development",
            industry=Industry.CONSULTING.value,
            company_size=CompanySize.SIZE_2_10.value,
            country="Netherlands",
            status=CompanyStatus.ACTIVE.value,
        )
        session.add(company)
        await session.flush()

    ws_result = await session.execute(
        select(Workspace).where(
            Workspace.company_id == company.id,
            Workspace.slug == DEMO_WORKSPACE_SLUG,
        )
    )
    workspace = ws_result.scalar_one_or_none()
    if workspace is None:
        workspace = Workspace(
            company_id=company.id,
            name="Default Workspace",
            slug=DEMO_WORKSPACE_SLUG,
            description="Default workspace for demo data",
            default_timezone="Europe/Amsterdam",
            default_currency="EUR",
            status=WorkspaceStatus.ACTIVE.value,
        )
        session.add(workspace)
        await session.flush()

    return company, workspace


async def seed_demo_company_members(
    session: AsyncSession,
    *,
    company: Company,
    user_by_email: dict[str, User],
    person_by_email: dict[str, Person],
) -> None:
    now = datetime.now(timezone.utc)
    for email, role in DEMO_MEMBER_ROLES.items():
        user = user_by_email.get(email)
        if user is None:
            continue
        person = person_by_email.get(email)
        result = await session.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == company.id,
                CompanyMember.user_id == user.id,
            )
        )
        member = result.scalar_one_or_none()
        if member is None:
            session.add(
                CompanyMember(
                    company_id=company.id,
                    user_id=user.id,
                    person_id=person.id if person else None,
                    role=role.value,
                    status=CompanyMemberStatus.ACTIVE.value,
                    joined_at=now,
                )
            )
        else:
            member.role = role.value
            member.status = CompanyMemberStatus.ACTIVE.value
            if person and member.person_id is None:
                member.person_id = person.id


async def assign_default_tenant_to_seeded_objects(
    session: AsyncSession,
    company_id: uuid.UUID,
    workspace_id: uuid.UUID,
) -> None:
    for model in COMPANY_WORKSPACE_MODELS:
        await session.execute(
            update(model)
            .where(model.company_id.is_(None))
            .values(company_id=company_id, workspace_id=workspace_id)
        )
    for model in COMPANY_ONLY_MODELS:
        await session.execute(
            update(model).where(model.company_id.is_(None)).values(company_id=company_id)
        )
