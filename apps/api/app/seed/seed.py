"""Idempotent database seed runner for local demo data."""

from __future__ import annotations

import asyncio
import sys
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_sessionmaker
from app.domain.enums import (
    AutomationStatus,
    AutomationTriggerType,
    ComplianceSubjectType,
    DataProductStatus,
    DataProductType,
    EntityLinkType,
    EntityType,
    EvidenceStatus,
    FileEntityType,
    MetricValueStatus,
    PerformanceSubjectType,
    ProjectStatus,
    ProjectType,
    QualityStatus,
    ScheduleFrequency,
    SeniorityLevel,
    UserRole,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.models.automation import AutomationSchedule, AutomationTrigger
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
from app.models.people import Capability, Person, Team
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue
from app.models.projects import Project
from app.models.relationships import EntityLink
from app.models.work import WorkItem
from app.modules.auth.security import hash_password
from app.seed.seed_data import (
    AUTOMATION_SCHEDULES,
    AUTOMATION_TRIGGERS,
    BUSINESS_DOMAINS,
    CAPABILITIES,
    CLIENT_PROJECTS,
    COMPLIANCE_CHECKS,
    COMPLIANCE_CONTROLS,
    COMPLIANCE_POLICIES,
    COMPLIANCE_RULES,
    DATA_PRODUCTS,
    DEMO_AUTH_USERS,
    FILE_ASSETS,
    FILE_STORAGES,
    INTERNAL_PROJECTS,
    NOTIFICATION_CHANNELS,
    NOTIFICATION_MESSAGES,
    NOTIFICATION_PREFERENCES,
    NOTIFICATION_TEMPLATES,
    PEOPLE,
    PERFORMANCE_METRIC_DEFINITIONS,
    PERFORMANCE_METRIC_VALUES,
    RELATIONSHIPS,
    TEAMS,
    WORK_ITEMS,
    AutomationScheduleSeed,
    AutomationTriggerSeed,
    BusinessDomainSeed,
    CapabilitySeed,
    ComplianceCheckSeed,
    ComplianceControlSeed,
    CompliancePolicySeed,
    ComplianceRuleSeed,
    DataProductSeed,
    FileAssetSeed,
    FileStorageSeed,
    PerformanceMetricDefinitionSeed,
    PerformanceMetricValueSeed,
    PersonSeed,
    ProjectSeed,
    RelationshipSeed,
    TeamSeed,
    WorkItemSeed,
)
from app.seed.tenant import (
    assign_default_tenant_to_seeded_objects,
    get_or_create_demo_tenant,
    seed_demo_company_members,
)


@dataclass
class EntityStats:
    created: int = 0
    updated: int = 0
    skipped: int = 0


@dataclass
class SeedSummary:
    capabilities: EntityStats = field(default_factory=EntityStats)
    teams: EntityStats = field(default_factory=EntityStats)
    people: EntityStats = field(default_factory=EntityStats)
    users: EntityStats = field(default_factory=EntityStats)
    business_domains: EntityStats = field(default_factory=EntityStats)
    projects: EntityStats = field(default_factory=EntityStats)
    data_products: EntityStats = field(default_factory=EntityStats)
    work_items: EntityStats = field(default_factory=EntityStats)
    relationships: EntityStats = field(default_factory=EntityStats)
    file_storages: EntityStats = field(default_factory=EntityStats)
    file_assets: EntityStats = field(default_factory=EntityStats)
    file_attachments: EntityStats = field(default_factory=EntityStats)
    policies: EntityStats = field(default_factory=EntityStats)
    compliance_rules: EntityStats = field(default_factory=EntityStats)
    controls: EntityStats = field(default_factory=EntityStats)
    compliance_checks: EntityStats = field(default_factory=EntityStats)
    compliance_evidence: EntityStats = field(default_factory=EntityStats)
    automation_schedules: EntityStats = field(default_factory=EntityStats)
    automation_triggers: EntityStats = field(default_factory=EntityStats)
    performance_metric_definitions: EntityStats = field(default_factory=EntityStats)
    performance_metric_values: EntityStats = field(default_factory=EntityStats)
    notification_channels: EntityStats = field(default_factory=EntityStats)
    notification_templates: EntityStats = field(default_factory=EntityStats)
    notification_messages: EntityStats = field(default_factory=EntityStats)
    notification_preferences: EntityStats = field(default_factory=EntityStats)

    def print_summary(self) -> None:
        sections = [
            ("Capabilities", self.capabilities),
            ("Teams", self.teams),
            ("People", self.people),
            ("Users", self.users),
            ("Business domains", self.business_domains),
            ("Projects", self.projects),
            ("Data products", self.data_products),
            ("Work items", self.work_items),
            ("Relationships", self.relationships),
            ("File storages", self.file_storages),
            ("File assets", self.file_assets),
            ("File attachments", self.file_attachments),
            ("Policies", self.policies),
            ("Compliance rules", self.compliance_rules),
            ("Controls", self.controls),
            ("Compliance checks", self.compliance_checks),
            ("Compliance evidence", self.compliance_evidence),
            ("Automation schedules", self.automation_schedules),
            ("Automation triggers", self.automation_triggers),
            ("Performance metrics", self.performance_metric_definitions),
            ("Performance values", self.performance_metric_values),
            ("Notification channels", self.notification_channels),
            ("Notification templates", self.notification_templates),
            ("Notification messages", self.notification_messages),
            ("Notification preferences", self.notification_preferences),
        ]
        print("\nSeed summary")
        print("=" * 60)
        for label, stats in sections:
            print(
                f"{label:20} created={stats.created:3}  "
                f"updated={stats.updated:3}  skipped={stats.skipped:3}"
            )
        print("=" * 60)


def _apply_optional_text_update(
    *,
    existing_value: str | None,
    new_value: str | None,
    stats: EntityStats,
) -> bool:
    if new_value is not None and existing_value != new_value:
        stats.updated += 1
        return True
    return False


async def get_or_create_user(
    session: AsyncSession,
    *,
    email: str,
    full_name: str,
    stats: SeedSummary,
    hashed_password: str | None = None,
    role: UserRole = UserRole.VIEWER,
    is_superuser: bool = False,
    is_active: bool = True,
) -> User:
    normalized_email = email.lower()
    result = await session.execute(select(User).where(User.email == normalized_email))
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        if existing.full_name != full_name:
            existing.full_name = full_name
            changed = True
        if hashed_password is not None and existing.hashed_password != hashed_password:
            existing.hashed_password = hashed_password
            changed = True
        if existing.role != role:
            existing.role = role
            changed = True
        if existing.is_superuser != is_superuser:
            existing.is_superuser = is_superuser
            changed = True
        if existing.is_active != is_active:
            existing.is_active = is_active
            changed = True
        if changed:
            stats.users.updated += 1
        else:
            stats.users.skipped += 1
        return existing

    user = User(
        email=normalized_email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=role,
        is_superuser=is_superuser,
        is_active=is_active,
    )
    session.add(user)
    await session.flush()
    stats.users.created += 1
    return user


async def get_or_create_capability(
    session: AsyncSession,
    data: CapabilitySeed,
    stats: SeedSummary,
) -> Capability:
    result = await session.execute(select(Capability).where(Capability.name == data["name"]))
    existing = result.scalar_one_or_none()
    if existing is not None:
        if _apply_optional_text_update(
            existing_value=existing.description,
            new_value=data["description"],
            stats=stats.capabilities,
        ):
            existing.description = data["description"]
        else:
            stats.capabilities.skipped += 1
        return existing

    capability = Capability(name=data["name"], description=data["description"])
    session.add(capability)
    await session.flush()
    stats.capabilities.created += 1
    return capability


async def get_or_create_team(
    session: AsyncSession,
    data: TeamSeed,
    stats: SeedSummary,
) -> Team:
    result = await session.execute(select(Team).where(Team.name == data["name"]))
    existing = result.scalar_one_or_none()
    if existing is not None:
        if _apply_optional_text_update(
            existing_value=existing.description,
            new_value=data["description"],
            stats=stats.teams,
        ):
            existing.description = data["description"]
        else:
            stats.teams.skipped += 1
        return existing

    team = Team(name=data["name"], description=data["description"])
    session.add(team)
    await session.flush()
    stats.teams.created += 1
    return team


async def get_or_create_person(
    session: AsyncSession,
    data: PersonSeed,
    *,
    team: Team,
    capability: Capability,
    stats: SeedSummary,
) -> Person:
    result = await session.execute(select(Person).where(Person.email == data["email"]))
    existing = result.scalar_one_or_none()
    seniority = SeniorityLevel(data["seniority_level"])

    if existing is not None:
        changed = False
        if existing.full_name != data["full_name"]:
            existing.full_name = data["full_name"]
            changed = True
        if existing.role_title != data["role_title"]:
            existing.role_title = data["role_title"]
            changed = True
        if existing.seniority_level != seniority:
            existing.seniority_level = seniority
            changed = True
        if existing.team_id != team.id:
            existing.team_id = team.id
            changed = True
        if existing.capability_id != capability.id:
            existing.capability_id = capability.id
            changed = True
        if existing.availability_percent != data["availability_percent"]:
            existing.availability_percent = data["availability_percent"]
            changed = True
        if existing.location != data["location"]:
            existing.location = data["location"]
            changed = True
        if existing.is_active != data["is_active"]:
            existing.is_active = data["is_active"]
            changed = True

        if changed:
            stats.people.updated += 1
        else:
            stats.people.skipped += 1
        return existing

    person = Person(
        full_name=data["full_name"],
        email=data["email"],
        role_title=data["role_title"],
        seniority_level=seniority,
        team_id=team.id,
        capability_id=capability.id,
        availability_percent=data["availability_percent"],
        location=data["location"],
        is_active=data["is_active"],
    )
    session.add(person)
    await session.flush()
    stats.people.created += 1
    return person


async def get_or_create_business_domain(
    session: AsyncSession,
    data: BusinessDomainSeed,
    *,
    owner: Person,
    stats: SeedSummary,
) -> BusinessDomain:
    result = await session.execute(
        select(BusinessDomain).where(BusinessDomain.name == data["name"])
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        if existing.description != data["description"]:
            existing.description = data["description"]
            changed = True
        if existing.owner_id != owner.id:
            existing.owner_id = owner.id
            changed = True
        if changed:
            stats.business_domains.updated += 1
        else:
            stats.business_domains.skipped += 1
        return existing

    domain = BusinessDomain(
        name=data["name"],
        description=data["description"],
        owner_id=owner.id,
    )
    session.add(domain)
    await session.flush()
    stats.business_domains.created += 1
    return domain


async def get_or_create_project(
    session: AsyncSession,
    data: ProjectSeed,
    *,
    owner: Person,
    team: Team,
    capability: Capability,
    stats: SeedSummary,
) -> Project:
    result = await session.execute(select(Project).where(Project.name == data["name"]))
    existing = result.scalar_one_or_none()

    start_date = date.today() + timedelta(days=data["start_date_offset_days"])
    target_end_date = date.today() + timedelta(days=data["target_end_date_offset_days"])
    project_type = ProjectType(data["project_type"])
    status = ProjectStatus(data["status"])
    budget_amount = Decimal(data["budget_amount"]) if "budget_amount" in data else None

    if existing is not None:
        changed = False
        field_updates: list[tuple[object, object]] = [
            (existing.project_type, project_type),
            (existing.status, status),
            (existing.client_name, data.get("client_name")),
            (existing.account_name, data.get("account_name")),
            (existing.owner_id, owner.id),
            (existing.team_id, team.id),
            (existing.capability_id, capability.id),
            (existing.start_date, start_date),
            (existing.target_end_date, target_end_date),
            (existing.budget_amount, budget_amount),
            (existing.budget_currency, data.get("budget_currency")),
            (existing.priority, data.get("priority")),
            (existing.health_status, data.get("health_status")),
            (existing.delivery_notes, data.get("delivery_notes")),
        ]
        for current, new in field_updates:
            if current != new:
                changed = True
                break

        if changed:
            existing.project_type = project_type
            existing.status = status
            existing.client_name = data.get("client_name")
            existing.account_name = data.get("account_name")
            existing.owner_id = owner.id
            existing.team_id = team.id
            existing.capability_id = capability.id
            existing.start_date = start_date
            existing.target_end_date = target_end_date
            existing.budget_amount = budget_amount
            existing.budget_currency = data.get("budget_currency")
            existing.priority = data.get("priority")
            existing.health_status = data.get("health_status")
            existing.delivery_notes = data.get("delivery_notes")
            stats.projects.updated += 1
        else:
            stats.projects.skipped += 1
        return existing

    project = Project(
        name=data["name"],
        project_type=project_type,
        status=status,
        client_name=data.get("client_name"),
        account_name=data.get("account_name"),
        owner_id=owner.id,
        team_id=team.id,
        capability_id=capability.id,
        start_date=start_date,
        target_end_date=target_end_date,
        budget_amount=budget_amount,
        budget_currency=data.get("budget_currency"),
        priority=data.get("priority"),
        health_status=data.get("health_status"),
        delivery_notes=data.get("delivery_notes"),
    )
    session.add(project)
    await session.flush()
    stats.projects.created += 1
    return project


async def get_or_create_data_product(
    session: AsyncSession,
    data: DataProductSeed,
    *,
    business_domain: BusinessDomain,
    business_owner: Person | None,
    technical_owner: Person,
    capability: Capability,
    team: Team,
    stats: SeedSummary,
) -> DataProduct:
    business_owner_id = business_owner.id if business_owner else None
    result = await session.execute(select(DataProduct).where(DataProduct.name == data["name"]))
    existing = result.scalar_one_or_none()

    product_type = DataProductType(data["type"])
    status = DataProductStatus(data["status"])
    quality_status = QualityStatus(data["quality_status"])

    if existing is not None:
        changed = False
        documentation_url = data.get("documentation_url")
        field_updates: list[tuple[object, object]] = [
            (existing.description, data["description"]),
            (existing.type, product_type),
            (existing.status, status),
            (existing.quality_status, quality_status),
            (existing.business_domain_id, business_domain.id),
            (existing.business_owner_id, business_owner_id),
            (existing.technical_owner_id, technical_owner.id),
            (existing.capability_id, capability.id),
            (existing.team_id, team.id),
            (existing.refresh_frequency, data["refresh_frequency"]),
            (existing.source_systems, data["source_systems"]),
            (existing.consumers, data["consumers"]),
            (existing.documentation_url, documentation_url),
        ]
        for current, new in field_updates:
            if current != new:
                changed = True
                break

        if changed:
            existing.description = data["description"]
            existing.type = product_type
            existing.status = status
            existing.quality_status = quality_status
            existing.business_domain_id = business_domain.id
            existing.business_owner_id = business_owner_id
            existing.technical_owner_id = technical_owner.id
            existing.capability_id = capability.id
            existing.team_id = team.id
            existing.refresh_frequency = data["refresh_frequency"]
            existing.source_systems = data["source_systems"]
            existing.consumers = data["consumers"]
            existing.documentation_url = documentation_url
            stats.data_products.updated += 1
        else:
            stats.data_products.skipped += 1
        return existing

    product = DataProduct(
        name=data["name"],
        description=data["description"],
        type=product_type,
        status=status,
        quality_status=quality_status,
        business_domain_id=business_domain.id,
        business_owner_id=business_owner_id,
        technical_owner_id=technical_owner.id,
        capability_id=capability.id,
        team_id=team.id,
        refresh_frequency=data["refresh_frequency"],
        source_systems=data["source_systems"],
        consumers=data["consumers"],
        documentation_url=data.get("documentation_url"),
    )
    session.add(product)
    await session.flush()
    stats.data_products.created += 1
    return product


async def get_or_create_work_item(
    session: AsyncSession,
    data: WorkItemSeed,
    *,
    assignee: Person,
    reporter: User | None,
    project: Project,
    data_product: DataProduct | None,
    capability: Capability,
    team: Team,
    stats: SeedSummary,
) -> WorkItem:
    work_type = WorkItemType(data["type"])
    result = await session.execute(
        select(WorkItem).where(and_(WorkItem.title == data["title"], WorkItem.type == work_type))
    )
    existing = result.scalar_one_or_none()

    status = WorkItemStatus(data["status"])
    priority = WorkItemPriority(data["priority"])
    due_date = date.today() + timedelta(days=data["due_date_offset_days"])
    data_product_id = data_product.id if data_product is not None else None
    reporter_id = reporter.id if reporter is not None else None

    if existing is not None:
        changed = False
        field_updates: list[tuple[object, object]] = [
            (existing.status, status),
            (existing.priority, priority),
            (existing.assignee_id, assignee.id),
            (existing.reporter_id, reporter_id),
            (existing.project_id, project.id),
            (existing.data_product_id, data_product_id),
            (existing.capability_id, capability.id),
            (existing.team_id, team.id),
            (existing.due_date, due_date),
            (existing.estimate_points, data["estimate_points"]),
        ]
        for current, new in field_updates:
            if current != new:
                changed = True
                break

        if changed:
            existing.status = status
            existing.priority = priority
            existing.assignee_id = assignee.id
            existing.reporter_id = reporter_id
            existing.project_id = project.id
            existing.data_product_id = data_product_id
            existing.capability_id = capability.id
            existing.team_id = team.id
            existing.due_date = due_date
            existing.estimate_points = data["estimate_points"]
            stats.work_items.updated += 1
        else:
            stats.work_items.skipped += 1
        return existing

    work_item = WorkItem(
        title=data["title"],
        type=work_type,
        status=status,
        priority=priority,
        assignee_id=assignee.id,
        reporter_id=reporter_id,
        project_id=project.id,
        data_product_id=data_product_id,
        capability_id=capability.id,
        team_id=team.id,
        due_date=due_date,
        estimate_points=data["estimate_points"],
    )
    session.add(work_item)
    await session.flush()
    stats.work_items.created += 1
    return work_item


async def seed_database(session: AsyncSession | None = None) -> SeedSummary:
    """Seed demo records in dependency order. Safe to run multiple times."""
    summary = SeedSummary()
    owns_session = session is None
    if owns_session:
        sessionmaker = get_sessionmaker()
        async with sessionmaker() as session:
            await _run_seed(session, summary)
            await session.commit()
    else:
        assert session is not None
        await _run_seed(session, summary)

    summary.print_summary()
    return summary


async def _run_seed(session: AsyncSession, summary: SeedSummary) -> None:
    capability_by_name: dict[str, Capability] = {}
    for item in CAPABILITIES:
        capability = await get_or_create_capability(session, item, summary)
        capability_by_name[item["name"]] = capability

    team_by_name: dict[str, Team] = {}
    for item in TEAMS:
        team = await get_or_create_team(session, item, summary)
        team_by_name[item["name"]] = team

    person_by_email: dict[str, Person] = {}
    for item in PEOPLE:
        team = team_by_name[item["team"]]
        capability = capability_by_name[item["capability"]]
        person = await get_or_create_person(
            session,
            item,
            team=team,
            capability=capability,
            stats=summary,
        )
        person_by_email[item["email"]] = person

    user_by_email: dict[str, User] = {}
    for item in DEMO_AUTH_USERS:
        user = await get_or_create_user(
            session,
            email=item["email"],
            full_name=item["full_name"],
            hashed_password=hash_password(item["password"]),
            role=UserRole(item["role"]),
            is_superuser=item["is_superuser"],
            is_active=item["is_active"],
            stats=summary,
        )
        user_by_email[item["email"]] = user

    reporter_emails = {item["reporter_email"] for item in WORK_ITEMS if "reporter_email" in item}
    for email in sorted(reporter_emails):
        person = person_by_email[email]
        user = await get_or_create_user(
            session,
            email=email,
            full_name=person.full_name,
            stats=summary,
        )
        user_by_email[email] = user

    domain_by_name: dict[str, BusinessDomain] = {}
    for item in BUSINESS_DOMAINS:
        owner = person_by_email[item["owner_email"]]
        domain = await get_or_create_business_domain(
            session,
            item,
            owner=owner,
            stats=summary,
        )
        domain_by_name[item["name"]] = domain

    project_by_name: dict[str, Project] = {}
    for item in CLIENT_PROJECTS + INTERNAL_PROJECTS:
        owner = person_by_email[item["owner_email"]]
        team = team_by_name[item["team"]]
        capability = capability_by_name[item["capability"]]
        project = await get_or_create_project(
            session,
            item,
            owner=owner,
            team=team,
            capability=capability,
            stats=summary,
        )
        project_by_name[item["name"]] = project

    product_by_name: dict[str, DataProduct] = {}
    for item in DATA_PRODUCTS:
        business_owner_email = item.get("business_owner_email")
        business_owner = person_by_email.get(business_owner_email) if business_owner_email else None
        product = await get_or_create_data_product(
            session,
            item,
            business_domain=domain_by_name[item["business_domain"]],
            business_owner=business_owner,
            technical_owner=person_by_email[item["technical_owner_email"]],
            capability=capability_by_name[item["capability"]],
            team=team_by_name[item["team"]],
            stats=summary,
        )
        product_by_name[item["name"]] = product

    work_item_by_title: dict[str, WorkItem] = {}
    for item in WORK_ITEMS:
        data_product = None
        product_name = item.get("data_product")
        if product_name:
            data_product = product_by_name[product_name]

        reporter = None
        reporter_email = item.get("reporter_email")
        if reporter_email:
            reporter = user_by_email[reporter_email]

        work_item = await get_or_create_work_item(
            session,
            item,
            assignee=person_by_email[item["assignee_email"]],
            reporter=reporter,
            project=project_by_name[item["project"]],
            data_product=data_product,
            capability=capability_by_name[item["capability"]],
            team=team_by_name[item["team"]],
            stats=summary,
        )
        work_item_by_title[item["title"]] = work_item

    for item in RELATIONSHIPS:
        source_type = EntityType(item["source_type"])
        target_type = EntityType(item["target_type"])
        source_id = _resolve_entity_id(
            entity_type=source_type,
            key=item["source_key"],
            product_by_name=product_by_name,
            work_item_by_title=work_item_by_title,
            project_by_name=project_by_name,
            team_by_name=team_by_name,
            capability_by_name=capability_by_name,
        )
        target_id = _resolve_entity_id(
            entity_type=target_type,
            key=item["target_key"],
            product_by_name=product_by_name,
            work_item_by_title=work_item_by_title,
            project_by_name=project_by_name,
            team_by_name=team_by_name,
            capability_by_name=capability_by_name,
        )
        if source_id is None or target_id is None:
            continue
        await get_or_create_relationship(
            session,
            item,
            source_id=source_id,
            target_id=target_id,
            stats=summary,
        )

    storage_by_name: dict[str, FileStorage] = {}
    for item in FILE_STORAGES:
        storage = await get_or_create_file_storage(session, item, stats=summary)
        storage_by_name[item["name"]] = storage

    for item in FILE_ASSETS:
        entity_type = FileEntityType(item["entity_type"])
        entity_id = _resolve_file_entity_id(
            entity_type=entity_type,
            key=item["entity_key"],
            product_by_name=product_by_name,
            work_item_by_title=work_item_by_title,
            project_by_name=project_by_name,
        )
        if entity_id is None:
            continue
        storage = storage_by_name.get(item.get("storage", ""))
        await get_or_create_file_asset_with_attachment(
            session,
            item,
            storage=storage,
            entity_type=entity_type,
            entity_id=entity_id,
            stats=summary,
        )

    file_by_name: dict[str, FileAsset] = {}
    for item in FILE_ASSETS:
        result = await session.execute(select(FileAsset).where(FileAsset.name == item["name"]))
        asset = result.scalar_one_or_none()
        if asset is not None:
            file_by_name[item["name"]] = asset

    policy_by_name: dict[str, Policy] = {}
    for item in COMPLIANCE_POLICIES:
        owner = person_by_email.get(item["owner_email"])
        policy = await get_or_create_policy(
            session,
            item,
            owner=owner,
            stats=summary,
        )
        policy_by_name[item["name"]] = policy

    rule_by_code: dict[str, ComplianceRule] = {}
    for item in COMPLIANCE_RULES:
        policy = policy_by_name.get(item["policy"])
        if policy is None:
            continue
        rule = await get_or_create_compliance_rule(
            session,
            item,
            policy=policy,
            stats=summary,
        )
        rule_by_code[item["code"]] = rule

    control_by_name: dict[str, Control] = {}
    for item in COMPLIANCE_CONTROLS:
        rule = rule_by_code.get(item["rule_code"])
        if rule is None:
            continue
        control = await get_or_create_control(
            session,
            item,
            rule=rule,
            stats=summary,
        )
        control_by_name[item["name"]] = control

    for item in COMPLIANCE_CHECKS:
        subject_type = ComplianceSubjectType(item["subject_type"])
        subject_id = _resolve_compliance_subject_id(
            subject_type=subject_type,
            key=item["subject_key"],
            product_by_name=product_by_name,
            project_by_name=project_by_name,
            team_by_name=team_by_name,
            capability_by_name=capability_by_name,
        )
        if subject_id is None:
            continue
        rule = rule_by_code.get(item["rule_code"])
        control = control_by_name.get(item["control_name"])
        evidence_file = (
            file_by_name.get(item.get("evidence_file", "")) if item.get("evidence_file") else None
        )
        await get_or_create_compliance_check(
            session,
            item,
            subject_type=subject_type,
            subject_id=subject_id,
            rule=rule,
            control=control,
            evidence_file=evidence_file,
            stats=summary,
        )

    schedule_by_name: dict[str, AutomationSchedule] = {}
    for item in AUTOMATION_SCHEDULES:
        schedule = await get_or_create_automation_schedule(session, item, stats=summary)
        schedule_by_name[item["name"]] = schedule

    admin_user = user_by_email.get("admin@example.com")
    for item in AUTOMATION_TRIGGERS:
        schedule = schedule_by_name.get(item["schedule"])
        if schedule is None:
            continue
        target_id = _resolve_automation_target_id(
            target_type=item["target_type"],
            key=item["target_key"],
            product_by_name=product_by_name,
            project_by_name=project_by_name,
            team_by_name=team_by_name,
            capability_by_name=capability_by_name,
            work_item_by_title=work_item_by_title,
        )
        if target_id is None:
            continue
        await get_or_create_automation_trigger(
            session,
            item,
            schedule=schedule,
            target_id=target_id,
            created_by=admin_user,
            stats=summary,
        )

    metric_by_code: dict[str, PerformanceMetricDefinition] = {}
    for item in PERFORMANCE_METRIC_DEFINITIONS:
        owner = None
        owner_email = item.get("owner_email")
        if owner_email:
            owner = person_by_email.get(owner_email)
        definition = await get_or_create_performance_metric_definition(
            session,
            item,
            owner=owner,
            stats=summary,
        )
        metric_by_code[item["code"]] = definition

    for item in PERFORMANCE_METRIC_VALUES:
        definition = metric_by_code.get(item["metric_code"])
        if definition is None:
            continue
        subject_type = PerformanceSubjectType(item["subject_type"])
        subject_id = _resolve_performance_subject_id(
            subject_type=subject_type,
            key=item["subject_key"],
            product_by_name=product_by_name,
            project_by_name=project_by_name,
            team_by_name=team_by_name,
            capability_by_name=capability_by_name,
            person_by_email=person_by_email,
        )
        if subject_id is None:
            continue
        period_start, period_end = _performance_period_for_frequency(
            item.get("frequency", "monthly")
        )
        await get_or_create_performance_metric_value(
            session,
            item,
            definition=definition,
            subject_type=subject_type,
            subject_id=subject_id,
            period_start=period_start,
            period_end=period_end,
            stats=summary,
        )

    channel_by_name: dict[str, NotificationChannel] = {}
    for item in NOTIFICATION_CHANNELS:
        channel = await get_or_create_notification_channel(
            session,
            item,
            created_by=admin_user,
            stats=summary,
        )
        channel_by_name[item["name"]] = channel

    template_by_name: dict[str, NotificationTemplate] = {}
    for item in NOTIFICATION_TEMPLATES:
        template = await get_or_create_notification_template(
            session,
            item,
            created_by=admin_user,
            stats=summary,
        )
        template_by_name[item["name"]] = template

    check_by_title = {
        check.title: check for check in (await session.scalars(select(ComplianceCheck))).all()
    }

    for item in NOTIFICATION_MESSAGES:
        channel = channel_by_name.get(item["channel"])
        if channel is None:
            continue
        template = template_by_name.get(item["template"]) if item.get("template") else None
        entity_id = _resolve_notification_entity_id(
            entity_type=item.get("entity_type"),
            entity_key=item.get("entity_key"),
            product_by_name=product_by_name,
            check_by_title=check_by_title,
        )
        await get_or_create_notification_message(
            session,
            item,
            channel=channel,
            template=template,
            entity_id=entity_id,
            created_by=admin_user,
            stats=summary,
        )

    for item in NOTIFICATION_PREFERENCES:
        user = user_by_email.get(item["user_email"])
        if user is None:
            continue
        await get_or_create_notification_preference(
            session,
            item,
            user=user,
            stats=summary,
        )

    company, workspace = await get_or_create_demo_tenant(session)
    await seed_demo_company_members(
        session,
        company=company,
        user_by_email=user_by_email,
        person_by_email=person_by_email,
    )
    await assign_default_tenant_to_seeded_objects(session, company.id, workspace.id)


def _performance_period_for_frequency(frequency: str) -> tuple[date, date]:
    today = date.today()
    if frequency == "weekly":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    month_start = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    month_end = next_month - timedelta(days=1)
    return month_start, month_end


def _resolve_performance_subject_id(
    *,
    subject_type: PerformanceSubjectType,
    key: str,
    product_by_name: dict[str, DataProduct],
    project_by_name: dict[str, Project],
    team_by_name: dict[str, Team],
    capability_by_name: dict[str, Capability],
    person_by_email: dict[str, Person],
) -> uuid.UUID | None:
    if subject_type == PerformanceSubjectType.DATA_PRODUCT:
        product = product_by_name.get(key)
        return product.id if product else None
    if subject_type == PerformanceSubjectType.PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type != ProjectType.INTERNAL_PROJECT else None
    if subject_type == PerformanceSubjectType.INTERNAL_PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type == ProjectType.INTERNAL_PROJECT else None
    if subject_type == PerformanceSubjectType.TEAM:
        team = team_by_name.get(key)
        return team.id if team else None
    if subject_type == PerformanceSubjectType.CAPABILITY:
        capability = capability_by_name.get(key)
        return capability.id if capability else None
    if subject_type == PerformanceSubjectType.PERSON:
        person = person_by_email.get(key)
        return person.id if person else None
    return None


async def get_or_create_performance_metric_definition(
    session: AsyncSession,
    data: PerformanceMetricDefinitionSeed,
    *,
    owner: Person | None,
    stats: SeedSummary,
) -> PerformanceMetricDefinition:
    result = await session.execute(
        select(PerformanceMetricDefinition).where(PerformanceMetricDefinition.code == data["code"])
    )
    existing = result.scalar_one_or_none()
    payload = {
        "name": data["name"],
        "code": data["code"],
        "description": data.get("description"),
        "subject_type": data["subject_type"],
        "value_type": data.get("value_type", "number"),
        "direction": data.get("direction", "neutral"),
        "frequency": data.get("frequency"),
        "status": data.get("status", "active"),
        "unit": data.get("unit"),
        "target_value": Decimal(data["target_value"]) if data.get("target_value") else None,
        "warning_threshold": Decimal(data["warning_threshold"])
        if data.get("warning_threshold")
        else None,
        "critical_threshold": Decimal(data["critical_threshold"])
        if data.get("critical_threshold")
        else None,
        "owner_id": owner.id if owner else None,
    }
    if existing is not None:
        changed = False
        for field, value in payload.items():
            if getattr(existing, field) != value:
                setattr(existing, field, value)
                changed = True
        if changed:
            stats.performance_metric_definitions.updated += 1
        else:
            stats.performance_metric_definitions.skipped += 1
        return existing

    definition = PerformanceMetricDefinition(**payload)
    session.add(definition)
    await session.flush()
    stats.performance_metric_definitions.created += 1
    return definition


async def get_or_create_performance_metric_value(
    session: AsyncSession,
    data: PerformanceMetricValueSeed,
    *,
    definition: PerformanceMetricDefinition,
    subject_type: PerformanceSubjectType,
    subject_id: uuid.UUID,
    period_start: date,
    period_end: date,
    stats: SeedSummary,
) -> PerformanceMetricValue:
    result = await session.execute(
        select(PerformanceMetricValue).where(
            PerformanceMetricValue.metric_definition_id == definition.id,
            PerformanceMetricValue.subject_type == subject_type.value,
            PerformanceMetricValue.subject_id == subject_id,
            PerformanceMetricValue.period_start == period_start,
            PerformanceMetricValue.period_end == period_end,
        )
    )
    existing = result.scalar_one_or_none()
    value_numeric = Decimal(data["value_numeric"])
    if existing is not None:
        changed = False
        if existing.value_numeric != value_numeric:
            existing.value_numeric = value_numeric
            changed = True
        source = data.get("source")
        if source is not None and existing.source != source:
            existing.source = source
            changed = True
        if changed:
            stats.performance_metric_values.updated += 1
        else:
            stats.performance_metric_values.skipped += 1
        return existing

    value = PerformanceMetricValue(
        metric_definition_id=definition.id,
        subject_type=subject_type.value,
        subject_id=subject_id,
        period_start=period_start,
        period_end=period_end,
        value_numeric=value_numeric,
        status=MetricValueStatus.SUBMITTED.value,
        source=data.get("source", "Manual demo seed"),
    )
    session.add(value)
    await session.flush()
    stats.performance_metric_values.created += 1
    return value


def _resolve_automation_target_id(
    *,
    target_type: str,
    key: str,
    product_by_name: dict[str, DataProduct],
    project_by_name: dict[str, Project],
    team_by_name: dict[str, Team],
    capability_by_name: dict[str, Capability],
    work_item_by_title: dict[str, WorkItem],
) -> uuid.UUID | None:
    if target_type == "data_product":
        product = product_by_name.get(key)
        return product.id if product else None
    if target_type == "work_item":
        work_item = work_item_by_title.get(key)
        return work_item.id if work_item else None
    if target_type == "project":
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type != ProjectType.INTERNAL_PROJECT else None
    if target_type == "internal_project":
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type == ProjectType.INTERNAL_PROJECT else None
    if target_type == "team":
        team = team_by_name.get(key)
        return team.id if team else None
    if target_type == "capability":
        capability = capability_by_name.get(key)
        return capability.id if capability else None
    return None


async def get_or_create_automation_schedule(
    session: AsyncSession,
    data: AutomationScheduleSeed,
    *,
    stats: SeedSummary,
) -> AutomationSchedule:
    result = await session.execute(
        select(AutomationSchedule).where(AutomationSchedule.name == data["name"])
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in ("description", "frequency", "timezone", "is_active"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.automation_schedules.updated += 1
        else:
            stats.automation_schedules.skipped += 1
        return existing

    schedule = AutomationSchedule(
        name=data["name"],
        description=data.get("description"),
        frequency=data.get("frequency", ScheduleFrequency.MONTHLY.value),
        timezone=data.get("timezone", "UTC"),
        is_active=data.get("is_active", True),
    )
    session.add(schedule)
    await session.flush()
    stats.automation_schedules.created += 1
    return schedule


async def get_or_create_automation_trigger(
    session: AsyncSession,
    data: AutomationTriggerSeed,
    *,
    schedule: AutomationSchedule,
    target_id: uuid.UUID,
    created_by: User | None,
    stats: SeedSummary,
) -> AutomationTrigger:
    result = await session.execute(
        select(AutomationTrigger).where(AutomationTrigger.name == data["name"])
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        updates = {
            "description": data.get("description"),
            "status": data.get("status", AutomationStatus.DRAFT.value),
            "trigger_type": data.get("trigger_type", AutomationTriggerType.SCHEDULE.value),
            "action_type": data["action_type"],
            "schedule_id": schedule.id,
            "target_type": data["target_type"],
            "target_id": target_id,
            "action_config": data.get("action_config"),
        }
        past_minutes = data.get("next_run_at_past_minutes")
        if past_minutes is not None:
            updates["next_run_at"] = datetime.now(UTC) - timedelta(minutes=past_minutes)
        for field, value in updates.items():
            if value is not None and getattr(existing, field) != value:
                setattr(existing, field, value)
                changed = True
        if changed:
            stats.automation_triggers.updated += 1
        else:
            stats.automation_triggers.skipped += 1
        return existing

    next_run_at = None
    past_minutes = data.get("next_run_at_past_minutes")
    if past_minutes is not None:
        next_run_at = datetime.now(UTC) - timedelta(minutes=past_minutes)
    elif data.get("status", AutomationStatus.ACTIVE.value) == AutomationStatus.ACTIVE.value:
        next_run_at = schedule.next_run_at or datetime.now(UTC)

    trigger = AutomationTrigger(
        name=data["name"],
        description=data.get("description"),
        status=data.get("status", AutomationStatus.ACTIVE.value),
        trigger_type=data.get("trigger_type", AutomationTriggerType.SCHEDULE.value),
        action_type=data["action_type"],
        schedule_id=schedule.id,
        target_type=data["target_type"],
        target_id=target_id,
        action_config=data.get("action_config"),
        created_by_id=created_by.id if created_by else None,
        next_run_at=next_run_at,
    )
    session.add(trigger)
    await session.flush()
    stats.automation_triggers.created += 1
    return trigger


def _resolve_compliance_subject_id(
    *,
    subject_type: ComplianceSubjectType,
    key: str,
    product_by_name: dict[str, DataProduct],
    project_by_name: dict[str, Project],
    team_by_name: dict[str, Team],
    capability_by_name: dict[str, Capability],
) -> uuid.UUID | None:
    if subject_type == ComplianceSubjectType.DATA_PRODUCT:
        product = product_by_name.get(key)
        return product.id if product else None
    if subject_type == ComplianceSubjectType.PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type != ProjectType.INTERNAL_PROJECT else None
    if subject_type == ComplianceSubjectType.INTERNAL_PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type == ProjectType.INTERNAL_PROJECT else None
    if subject_type == ComplianceSubjectType.TEAM:
        team = team_by_name.get(key)
        return team.id if team else None
    if subject_type == ComplianceSubjectType.CAPABILITY:
        capability = capability_by_name.get(key)
        return capability.id if capability else None
    return None


async def get_or_create_policy(
    session: AsyncSession,
    data: CompliancePolicySeed,
    *,
    owner: Person | None,
    stats: SeedSummary,
) -> Policy:
    result = await session.execute(select(Policy).where(Policy.name == data["name"]))
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in ("description", "status", "version"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if owner is not None and existing.owner_id != owner.id:
            existing.owner_id = owner.id
            changed = True
        if changed:
            stats.policies.updated += 1
        else:
            stats.policies.skipped += 1
        return existing

    policy = Policy(
        name=data["name"],
        description=data.get("description"),
        status=data["status"],
        owner_id=owner.id if owner else None,
        version=data.get("version"),
    )
    session.add(policy)
    await session.flush()
    stats.policies.created += 1
    return policy


async def get_or_create_compliance_rule(
    session: AsyncSession,
    data: ComplianceRuleSeed,
    *,
    policy: Policy,
    stats: SeedSummary,
) -> ComplianceRule:
    result = await session.execute(
        select(ComplianceRule).where(
            ComplianceRule.policy_id == policy.id,
            ComplianceRule.code == data["code"],
        )
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in ("name", "description", "severity", "subject_type"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.compliance_rules.updated += 1
        else:
            stats.compliance_rules.skipped += 1
        return existing

    rule = ComplianceRule(
        policy_id=policy.id,
        code=data.get("code"),
        name=data["name"],
        description=data.get("description"),
        severity=data["severity"],
        subject_type=data.get("subject_type"),
        is_active=True,
    )
    session.add(rule)
    await session.flush()
    stats.compliance_rules.created += 1
    return rule


async def get_or_create_control(
    session: AsyncSession,
    data: ComplianceControlSeed,
    *,
    rule: ComplianceRule,
    stats: SeedSummary,
) -> Control:
    result = await session.execute(
        select(Control).where(Control.rule_id == rule.id, Control.name == data["name"])
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in ("description", "control_type", "status", "frequency"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.controls.updated += 1
        else:
            stats.controls.skipped += 1
        return existing

    control = Control(
        rule_id=rule.id,
        name=data["name"],
        description=data.get("description"),
        control_type=data["control_type"],
        status=data["status"],
        frequency=data.get("frequency"),
    )
    session.add(control)
    await session.flush()
    stats.controls.created += 1
    return control


async def get_or_create_compliance_check(
    session: AsyncSession,
    data: ComplianceCheckSeed,
    *,
    subject_type: ComplianceSubjectType,
    subject_id: uuid.UUID,
    rule: ComplianceRule | None,
    control: Control | None,
    evidence_file: FileAsset | None,
    stats: SeedSummary,
) -> ComplianceCheck:
    result = await session.execute(
        select(ComplianceCheck).where(
            ComplianceCheck.subject_type == subject_type.value,
            ComplianceCheck.subject_id == subject_id,
            ComplianceCheck.title == data["title"],
        )
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        due_date = None
        if data.get("due_date_offset_days") is not None:
            due_date = date.today() + timedelta(days=data["due_date_offset_days"])
        for field in ("description", "status", "check_type", "result_summary"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if due_date is not None and existing.due_date != due_date:
            existing.due_date = due_date
            changed = True
        if rule is not None and existing.rule_id != rule.id:
            existing.rule_id = rule.id
            changed = True
        if control is not None and existing.control_id != control.id:
            existing.control_id = control.id
            changed = True
        if changed:
            stats.compliance_checks.updated += 1
        else:
            stats.compliance_checks.skipped += 1
        check = existing
    else:
        due_date = None
        if data.get("due_date_offset_days") is not None:
            due_date = date.today() + timedelta(days=data["due_date_offset_days"])
        check = ComplianceCheck(
            rule_id=rule.id if rule else None,
            control_id=control.id if control else None,
            subject_type=subject_type.value,
            subject_id=subject_id,
            check_type=data["check_type"],
            status=data["status"],
            title=data["title"],
            description=data.get("description"),
            result_summary=data.get("result_summary"),
            due_date=due_date,
        )
        session.add(check)
        await session.flush()
        stats.compliance_checks.created += 1

    if evidence_file is not None:
        evidence_result = await session.execute(
            select(ComplianceCheckEvidence).where(
                ComplianceCheckEvidence.compliance_check_id == check.id,
                ComplianceCheckEvidence.file_id == evidence_file.id,
            )
        )
        evidence = evidence_result.scalar_one_or_none()
        if evidence is None:
            session.add(
                ComplianceCheckEvidence(
                    compliance_check_id=check.id,
                    file_id=evidence_file.id,
                    status=EvidenceStatus.SUBMITTED.value,
                    description=f"Seeded evidence for {data['title']}",
                )
            )
            await session.flush()
            stats.compliance_evidence.created += 1
        else:
            stats.compliance_evidence.skipped += 1

    return check


def _resolve_entity_id(
    *,
    entity_type: EntityType,
    key: str,
    product_by_name: dict[str, DataProduct],
    work_item_by_title: dict[str, WorkItem],
    project_by_name: dict[str, Project],
    team_by_name: dict[str, Team],
    capability_by_name: dict[str, Capability],
) -> uuid.UUID | None:
    if entity_type == EntityType.DATA_PRODUCT:
        product = product_by_name.get(key)
        return product.id if product else None
    if entity_type == EntityType.WORK_ITEM:
        work_item = work_item_by_title.get(key)
        return work_item.id if work_item else None
    if entity_type in (EntityType.PROJECT, EntityType.INTERNAL_PROJECT):
        project = project_by_name.get(key)
        if project is None:
            return None
        if entity_type == EntityType.INTERNAL_PROJECT:
            return project.id if project.project_type == ProjectType.INTERNAL_PROJECT else None
        return project.id if project.project_type != ProjectType.INTERNAL_PROJECT else None
    if entity_type == EntityType.TEAM:
        team = team_by_name.get(key)
        return team.id if team else None
    if entity_type == EntityType.CAPABILITY:
        capability = capability_by_name.get(key)
        return capability.id if capability else None
    return None


def _resolve_file_entity_id(
    *,
    entity_type: FileEntityType,
    key: str,
    product_by_name: dict[str, DataProduct],
    work_item_by_title: dict[str, WorkItem],
    project_by_name: dict[str, Project],
) -> uuid.UUID | None:
    if entity_type == FileEntityType.DATA_PRODUCT:
        product = product_by_name.get(key)
        return product.id if product else None
    if entity_type == FileEntityType.WORK_ITEM:
        work_item = work_item_by_title.get(key)
        return work_item.id if work_item else None
    if entity_type == FileEntityType.PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type != ProjectType.INTERNAL_PROJECT else None
    if entity_type == FileEntityType.INTERNAL_PROJECT:
        project = project_by_name.get(key)
        if project is None:
            return None
        return project.id if project.project_type == ProjectType.INTERNAL_PROJECT else None
    return None


async def get_or_create_file_storage(
    session: AsyncSession,
    data: FileStorageSeed,
    *,
    stats: SeedSummary,
) -> FileStorage:
    result = await session.execute(select(FileStorage).where(FileStorage.name == data["name"]))
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in ("storage_type", "base_url", "description", "is_active"):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.file_storages.updated += 1
        else:
            stats.file_storages.skipped += 1
        return existing

    storage = FileStorage(
        name=data["name"],
        storage_type=data["storage_type"],
        base_url=data.get("base_url"),
        description=data.get("description"),
        is_active=data.get("is_active", True),
    )
    session.add(storage)
    await session.flush()
    stats.file_storages.created += 1
    return storage


async def get_or_create_file_asset_with_attachment(
    session: AsyncSession,
    data: FileAssetSeed,
    *,
    storage: FileStorage | None,
    entity_type: FileEntityType,
    entity_id: uuid.UUID,
    stats: SeedSummary,
) -> FileAsset:
    result = await session.execute(select(FileAsset).where(FileAsset.name == data["name"]))
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        for field in (
            "description",
            "file_type",
            "status",
            "sensitivity",
            "external_url",
            "version",
        ):
            if field in data and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if storage is not None and existing.storage_id != storage.id:
            existing.storage_id = storage.id
            changed = True
        if changed:
            stats.file_assets.updated += 1
        else:
            stats.file_assets.skipped += 1
        file_asset = existing
    else:
        file_asset = FileAsset(
            name=data["name"],
            description=data.get("description"),
            file_type=data["file_type"],
            status=data["status"],
            sensitivity=data["sensitivity"],
            external_url=data.get("external_url"),
            version=data.get("version"),
            storage_id=storage.id if storage else None,
        )
        session.add(file_asset)
        await session.flush()
        stats.file_assets.created += 1

    purpose = data.get("purpose")
    attachment_result = await session.execute(
        select(FileAttachment).where(
            FileAttachment.file_id == file_asset.id,
            FileAttachment.entity_type == entity_type.value,
            FileAttachment.entity_id == entity_id,
            FileAttachment.purpose == purpose
            if purpose is not None
            else FileAttachment.purpose.is_(None),
        )
    )
    attachment = attachment_result.scalar_one_or_none()
    if attachment is not None:
        changed = False
        if attachment.is_evidence != data.get("is_evidence", False):
            attachment.is_evidence = data.get("is_evidence", False)
            changed = True
        if data.get("evidence_type") and attachment.evidence_type != data.get("evidence_type"):
            attachment.evidence_type = data.get("evidence_type")
            changed = True
        if changed:
            stats.file_attachments.updated += 1
        else:
            stats.file_attachments.skipped += 1
    else:
        attachment = FileAttachment(
            file_id=file_asset.id,
            entity_type=entity_type.value,
            entity_id=entity_id,
            purpose=purpose,
            is_evidence=data.get("is_evidence", False),
            evidence_type=data.get("evidence_type"),
        )
        session.add(attachment)
        await session.flush()
        stats.file_attachments.created += 1

    return file_asset


async def get_or_create_relationship(
    session: AsyncSession,
    data: RelationshipSeed,
    *,
    source_id: uuid.UUID,
    target_id: uuid.UUID,
    stats: SeedSummary,
) -> EntityLink:
    source_type = EntityType(data["source_type"])
    target_type = EntityType(data["target_type"])
    link_type = EntityLinkType(data["link_type"])
    result = await session.execute(
        select(EntityLink).where(
            EntityLink.source_type == source_type.value,
            EntityLink.source_id == source_id,
            EntityLink.target_type == target_type.value,
            EntityLink.target_id == target_id,
            EntityLink.link_type == link_type.value,
        )
    )
    existing = result.scalar_one_or_none()
    if existing is not None:
        changed = False
        if data.get("title") and existing.title != data.get("title"):
            existing.title = data.get("title")
            changed = True
        if data.get("description") and existing.description != data.get("description"):
            existing.description = data.get("description")
            changed = True
        if changed:
            stats.relationships.updated += 1
        else:
            stats.relationships.skipped += 1
        return existing

    link = EntityLink(
        source_type=source_type.value,
        source_id=source_id,
        target_type=target_type.value,
        target_id=target_id,
        link_type=link_type.value,
        title=data.get("title"),
        description=data.get("description"),
    )
    session.add(link)
    await session.flush()
    stats.relationships.created += 1
    return link


def _resolve_notification_entity_id(
    *,
    entity_type: str | None,
    entity_key: str | None,
    product_by_name: dict[str, DataProduct],
    check_by_title: dict[str, ComplianceCheck],
) -> uuid.UUID | None:
    if not entity_type or not entity_key:
        return None
    if entity_type == "data_product":
        product = product_by_name.get(entity_key)
        return product.id if product else None
    if entity_type == "compliance_check":
        check = check_by_title.get(entity_key)
        return check.id if check else None
    return None


async def get_or_create_notification_channel(
    session: AsyncSession,
    data: dict,
    *,
    created_by: User | None,
    stats: SeedSummary,
) -> NotificationChannel:
    existing = await session.scalar(
        select(NotificationChannel).where(NotificationChannel.name == data["name"])
    )
    if existing:
        changed = False
        for field in ("channel_type", "status", "description", "default_recipient"):
            if data.get(field) and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.notification_channels.updated += 1
        else:
            stats.notification_channels.skipped += 1
        return existing

    channel = NotificationChannel(
        name=data["name"],
        channel_type=data["channel_type"],
        status=data.get("status", "draft"),
        description=data.get("description"),
        endpoint_url=data.get("endpoint_url"),
        default_recipient=data.get("default_recipient"),
        provider_config=data.get("provider_config"),
        created_by_id=created_by.id if created_by else None,
    )
    session.add(channel)
    await session.flush()
    stats.notification_channels.created += 1
    return channel


async def get_or_create_notification_template(
    session: AsyncSession,
    data: dict,
    *,
    created_by: User | None,
    stats: SeedSummary,
) -> NotificationTemplate:
    existing = await session.scalar(
        select(NotificationTemplate).where(NotificationTemplate.name == data["name"])
    )
    if existing:
        changed = False
        for field in (
            "status",
            "event_type",
            "subject_template",
            "body_template",
            "description",
        ):
            if data.get(field) is not None and getattr(existing, field) != data.get(field):
                setattr(existing, field, data.get(field))
                changed = True
        if changed:
            stats.notification_templates.updated += 1
        else:
            stats.notification_templates.skipped += 1
        return existing

    template = NotificationTemplate(
        name=data["name"],
        status=data.get("status", "draft"),
        event_type=data.get("event_type"),
        subject_template=data.get("subject_template"),
        body_template=data["body_template"],
        description=data.get("description"),
        created_by_id=created_by.id if created_by else None,
    )
    session.add(template)
    await session.flush()
    stats.notification_templates.created += 1
    return template


async def get_or_create_notification_message(
    session: AsyncSession,
    data: dict,
    *,
    channel: NotificationChannel,
    template: NotificationTemplate | None,
    entity_id: uuid.UUID | None,
    created_by: User | None,
    stats: SeedSummary,
) -> NotificationMessage:
    subject = data.get("subject")
    existing = await session.scalar(
        select(NotificationMessage).where(
            NotificationMessage.subject == subject,
            NotificationMessage.channel_id == channel.id,
        )
    )
    now = datetime.now(UTC)
    scheduled_at = None
    past_minutes = data.get("scheduled_at_past_minutes")
    if past_minutes is not None:
        scheduled_at = now - timedelta(minutes=past_minutes)

    error_message = data.get("error_message")
    if existing:
        changed = False
        if data.get("status") and existing.status != data["status"]:
            existing.status = data["status"]
            changed = True
        if scheduled_at is not None and existing.scheduled_at != scheduled_at:
            existing.scheduled_at = scheduled_at
            changed = True
        if error_message is not None and existing.error_message != error_message:
            existing.error_message = error_message
            changed = True
        if changed:
            stats.notification_messages.updated += 1
        else:
            stats.notification_messages.skipped += 1
        return existing

    message = NotificationMessage(
        channel_id=channel.id,
        template_id=template.id if template else None,
        status=data.get("status", "draft"),
        priority=data.get("priority", "normal"),
        event_type=data.get("event_type", "manual"),
        subject=subject,
        body=data["body"],
        recipient_type=data.get("recipient_type"),
        recipient_value=data.get("recipient_value"),
        entity_type=data.get("entity_type"),
        entity_id=entity_id,
        created_by_id=created_by.id if created_by else None,
        scheduled_at=scheduled_at,
        simulated_at=now if data.get("simulated") else None,
        error_message=error_message,
    )
    session.add(message)
    await session.flush()

    if data.get("simulated"):
        attempt = NotificationDeliveryAttempt(
            message_id=message.id,
            status="simulated",
            attempt_number=1,
            provider=channel.channel_type,
            started_at=now,
            finished_at=now,
            request_payload={"simulate": True, "seed": True},
            response_payload={"mode": "simulation"},
        )
        session.add(attempt)
    elif data.get("status") == "failed":
        attempt = NotificationDeliveryAttempt(
            message_id=message.id,
            status="failed",
            attempt_number=1,
            provider=channel.channel_type,
            started_at=now,
            finished_at=now,
            error_message=error_message or "Delivery failed",
            request_payload={"seed": True},
            response_payload={"error": error_message or "Delivery failed"},
        )
        session.add(attempt)

    stats.notification_messages.created += 1
    return message


async def get_or_create_notification_preference(
    session: AsyncSession,
    data: dict,
    *,
    user: User,
    stats: SeedSummary,
) -> NotificationPreference:
    existing = await session.scalar(
        select(NotificationPreference).where(
            NotificationPreference.user_id == user.id,
            NotificationPreference.person_id.is_(None),
            NotificationPreference.channel_type == data["channel_type"],
            NotificationPreference.event_type == data["event_type"],
        )
    )
    if existing:
        if existing.is_enabled != data.get("is_enabled", True):
            existing.is_enabled = data.get("is_enabled", True)
            stats.notification_preferences.updated += 1
        else:
            stats.notification_preferences.skipped += 1
        return existing

    preference = NotificationPreference(
        user_id=user.id,
        person_id=None,
        channel_type=data["channel_type"],
        event_type=data["event_type"],
        is_enabled=data.get("is_enabled", True),
    )
    session.add(preference)
    await session.flush()
    stats.notification_preferences.created += 1
    return preference


async def count_seeded_entities(session: AsyncSession) -> dict[str, int]:
    """Return row counts for integration tests."""
    counts: dict[str, int] = {}
    for label, model in (
        ("capabilities", Capability),
        ("teams", Team),
        ("people", Person),
        ("users", User),
        ("business_domains", BusinessDomain),
        ("projects", Project),
        ("data_products", DataProduct),
        ("work_items", WorkItem),
        ("entity_links", EntityLink),
        ("file_storages", FileStorage),
        ("file_assets", FileAsset),
        ("file_attachments", FileAttachment),
        ("policies", Policy),
        ("compliance_rules", ComplianceRule),
        ("controls", Control),
        ("compliance_checks", ComplianceCheck),
        ("compliance_check_evidence", ComplianceCheckEvidence),
    ):
        result = await session.execute(select(func.count()).select_from(model))
        counts[label] = int(result.scalar_one())
    return counts


def main() -> None:
    """CLI entrypoint: python -m app.seed.seed"""
    try:
        asyncio.run(seed_database())
    except Exception as exc:
        import traceback

        traceback.print_exc()
        print(f"Seed failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
