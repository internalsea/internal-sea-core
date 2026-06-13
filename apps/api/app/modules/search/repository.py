from __future__ import annotations

import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.automation import AutomationTrigger
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck, Policy
from app.models.files import FileAsset
from app.models.notifications import NotificationMessage, NotificationTemplate
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.search.ranking import detect_matched_field
from app.modules.search.schemas import EntityLookupResult, SearchResult, SearchResultType
from app.modules.search.urls import (
    build_automation_trigger_url,
    build_capability_url,
    build_compliance_check_url,
    build_data_product_url,
    build_file_url,
    build_notification_message_url,
    build_notification_template_url,
    build_person_url,
    build_policy_url,
    build_project_url,
    build_team_url,
    build_work_item_url,
    project_search_result_type,
)
from app.modules.tenancy.scope import apply_company_filter

ALL_SEARCH_TYPES = list(SearchResultType)
PER_TYPE_FETCH_LIMIT = 15


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _company_scope(self, query, model: type[object], company_id: uuid.UUID | None):
        if company_id is not None:
            return apply_company_filter(query, model, company_id)
        return query

    async def search(
        self,
        *,
        query: str,
        types: list[SearchResultType] | None,
        company_id: uuid.UUID | None = None,
    ) -> list[SearchResult]:
        selected_types = types or ALL_SEARCH_TYPES
        results: list[SearchResult] = []

        if SearchResultType.DATA_PRODUCT in selected_types:
            results.extend(await self._search_data_products(query, company_id=company_id))
        if SearchResultType.WORK_ITEM in selected_types:
            results.extend(await self._search_work_items(query, company_id=company_id))
        if (
            SearchResultType.PROJECT in selected_types
            or SearchResultType.INTERNAL_PROJECT in selected_types
        ):
            results.extend(
                await self._search_projects(query, selected_types, company_id=company_id)
            )
        if SearchResultType.PERSON in selected_types:
            results.extend(await self._search_people(query, company_id=company_id))
        if SearchResultType.TEAM in selected_types:
            results.extend(await self._search_teams(query, company_id=company_id))
        if SearchResultType.CAPABILITY in selected_types:
            results.extend(await self._search_capabilities(query, company_id=company_id))
        if SearchResultType.FILE in selected_types:
            results.extend(await self._search_files(query, company_id=company_id))
        if SearchResultType.POLICY in selected_types:
            results.extend(await self._search_policies(query, company_id=company_id))
        if SearchResultType.COMPLIANCE_CHECK in selected_types:
            results.extend(await self._search_compliance_checks(query, company_id=company_id))
        if SearchResultType.AUTOMATION_TRIGGER in selected_types:
            results.extend(await self._search_automation_triggers(query, company_id=company_id))
        if SearchResultType.NOTIFICATION_TEMPLATE in selected_types:
            results.extend(await self._search_notification_templates(query, company_id=company_id))
        if SearchResultType.NOTIFICATION_MESSAGE in selected_types:
            results.extend(await self._search_notification_messages(query, company_id=company_id))

        return results

    async def lookup_entity(
        self,
        entity_type: SearchResultType,
        entity_id: uuid.UUID,
    ) -> EntityLookupResult | None:
        if entity_type in (SearchResultType.PROJECT, SearchResultType.INTERNAL_PROJECT):
            project = await self._session.get(Project, entity_id)
            if project is None:
                return None
            return _project_to_lookup(project)

        lookup_handlers = {
            SearchResultType.DATA_PRODUCT: self._lookup_data_product,
            SearchResultType.WORK_ITEM: self._lookup_work_item,
            SearchResultType.PERSON: self._lookup_person,
            SearchResultType.TEAM: self._lookup_team,
            SearchResultType.CAPABILITY: self._lookup_capability,
            SearchResultType.FILE: self._lookup_file,
            SearchResultType.POLICY: self._lookup_policy,
            SearchResultType.COMPLIANCE_CHECK: self._lookup_compliance_check,
        }
        handler = lookup_handlers.get(entity_type)
        if handler is None:
            return None
        return await handler(entity_id)

    async def _lookup_data_product(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        product = await self._session.get(DataProduct, entity_id)
        if product is None:
            return None
        return EntityLookupResult(
            id=product.id,
            type=SearchResultType.DATA_PRODUCT,
            title=product.name,
            description=product.description,
            status=str(product.status.value),
            secondary_status=str(product.quality_status.value),
            url=build_data_product_url(product.id),
        )

    async def _lookup_work_item(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        item = await self._session.get(WorkItem, entity_id)
        if item is None:
            return None
        return EntityLookupResult(
            id=item.id,
            type=SearchResultType.WORK_ITEM,
            title=item.title,
            description=item.description,
            status=str(item.status.value),
            secondary_status=str(item.priority.value),
            url=build_work_item_url(item.id),
        )

    async def _lookup_person(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        person = await self._session.get(Person, entity_id)
        if person is None:
            return None
        return EntityLookupResult(
            id=person.id,
            type=SearchResultType.PERSON,
            title=person.full_name,
            description=person.role_title or person.email,
            status="active" if person.is_active else "inactive",
            secondary_status=(
                str(person.seniority_level.value) if person.seniority_level is not None else None
            ),
            url=build_person_url(person.id),
        )

    async def _lookup_team(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        team = await self._session.get(Team, entity_id)
        if team is None:
            return None
        return EntityLookupResult(
            id=team.id,
            type=SearchResultType.TEAM,
            title=team.name,
            description=team.description,
            status=None,
            secondary_status=None,
            url=build_team_url(team.id),
        )

    async def _lookup_capability(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        capability = await self._session.get(Capability, entity_id)
        if capability is None:
            return None
        return EntityLookupResult(
            id=capability.id,
            type=SearchResultType.CAPABILITY,
            title=capability.name,
            description=capability.description,
            status=None,
            secondary_status=None,
            url=build_capability_url(capability.id),
        )

    async def _lookup_file(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        file_asset = await self._session.get(FileAsset, entity_id)
        if file_asset is None:
            return None
        return _file_to_lookup(file_asset)

    async def _lookup_policy(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        policy = await self._session.get(Policy, entity_id)
        if policy is None:
            return None
        return EntityLookupResult(
            id=policy.id,
            type=SearchResultType.POLICY,
            title=policy.name,
            description=policy.description,
            status=str(policy.status),
            secondary_status=policy.version,
            url=build_policy_url(policy.id),
        )

    async def _lookup_compliance_check(self, entity_id: uuid.UUID) -> EntityLookupResult | None:
        check = await self._session.get(ComplianceCheck, entity_id)
        if check is None:
            return None
        return EntityLookupResult(
            id=check.id,
            type=SearchResultType.COMPLIANCE_CHECK,
            title=check.title,
            description=check.description,
            status=str(check.status),
            secondary_status=str(check.check_type),
            url=build_compliance_check_url(check.id),
        )

    async def _search_data_products(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(DataProduct), DataProduct, company_id)
            .where(
                or_(
                    DataProduct.name.ilike(pattern),
                    DataProduct.description.ilike(pattern),
                    DataProduct.source_systems.ilike(pattern),
                    DataProduct.consumers.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for product in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "name": product.name,
                    "description": product.description,
                    "source_systems": product.source_systems,
                    "consumers": product.consumers,
                },
            )
            results.append(
                SearchResult(
                    id=product.id,
                    type=SearchResultType.DATA_PRODUCT,
                    title=product.name,
                    description=product.description,
                    status=str(product.status.value),
                    secondary_status=str(product.quality_status.value),
                    url=build_data_product_url(product.id),
                    matched_field=matched_field,
                    updated_at=product.updated_at,
                )
            )
        return results

    async def _search_work_items(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(WorkItem), WorkItem, company_id)
            .where(
                or_(
                    WorkItem.title.ilike(pattern),
                    WorkItem.description.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for item in rows.all():
            matched_field = detect_matched_field(
                query,
                {"title": item.title, "description": item.description},
            )
            results.append(
                SearchResult(
                    id=item.id,
                    type=SearchResultType.WORK_ITEM,
                    title=item.title,
                    description=item.description,
                    status=str(item.status.value),
                    secondary_status=str(item.priority.value),
                    url=build_work_item_url(item.id),
                    matched_field=matched_field,
                    updated_at=item.updated_at,
                )
            )
        return results

    async def _search_projects(
        self,
        query: str,
        selected_types: list[SearchResultType],
        *,
        company_id: uuid.UUID | None = None,
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(Project), Project, company_id)
            .where(
                or_(
                    Project.name.ilike(pattern),
                    Project.description.ilike(pattern),
                    Project.client_name.ilike(pattern),
                    Project.account_name.ilike(pattern),
                    Project.delivery_notes.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for project in rows.all():
            result_type = project_search_result_type(project.project_type)
            if result_type not in selected_types:
                continue
            matched_field = detect_matched_field(
                query,
                {
                    "name": project.name,
                    "description": project.description,
                    "client_name": project.client_name,
                    "account_name": project.account_name,
                    "delivery_notes": project.delivery_notes,
                },
            )
            results.append(
                SearchResult(
                    id=project.id,
                    type=result_type,
                    title=project.name,
                    description=project.description,
                    status=str(project.status.value),
                    secondary_status=project.health_status,
                    url=build_project_url(project.id, project.project_type),
                    matched_field=matched_field,
                    updated_at=project.updated_at,
                )
            )
        return results

    async def _search_people(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(Person), Person, company_id)
            .where(
                or_(
                    Person.full_name.ilike(pattern),
                    Person.email.ilike(pattern),
                    Person.role_title.ilike(pattern),
                    Person.location.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for person in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "full_name": person.full_name,
                    "email": person.email,
                    "role_title": person.role_title,
                    "location": person.location,
                },
            )
            description = person.role_title or person.email
            secondary_status = (
                str(person.seniority_level.value) if person.seniority_level is not None else None
            )
            results.append(
                SearchResult(
                    id=person.id,
                    type=SearchResultType.PERSON,
                    title=person.full_name,
                    description=description,
                    status="active" if person.is_active else "inactive",
                    secondary_status=secondary_status,
                    url=build_person_url(person.id),
                    matched_field=matched_field,
                    updated_at=person.updated_at,
                )
            )
        return results

    async def _search_teams(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(Team), Team, company_id)
            .where(
                or_(
                    Team.name.ilike(pattern),
                    Team.description.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for team in rows.all():
            matched_field = detect_matched_field(
                query,
                {"name": team.name, "description": team.description},
            )
            results.append(
                SearchResult(
                    id=team.id,
                    type=SearchResultType.TEAM,
                    title=team.name,
                    description=team.description,
                    status=None,
                    secondary_status=None,
                    url=build_team_url(team.id),
                    matched_field=matched_field,
                    updated_at=team.updated_at,
                )
            )
        return results

    async def _search_capabilities(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(Capability), Capability, company_id)
            .where(
                or_(
                    Capability.name.ilike(pattern),
                    Capability.description.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for capability in rows.all():
            matched_field = detect_matched_field(
                query,
                {"name": capability.name, "description": capability.description},
            )
            results.append(
                SearchResult(
                    id=capability.id,
                    type=SearchResultType.CAPABILITY,
                    title=capability.name,
                    description=capability.description,
                    status=None,
                    secondary_status=None,
                    url=build_capability_url(capability.id),
                    matched_field=matched_field,
                    updated_at=capability.updated_at,
                )
            )
        return results

    async def _search_files(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(FileAsset), FileAsset, company_id)
            .where(
                or_(
                    FileAsset.name.ilike(pattern),
                    FileAsset.description.ilike(pattern),
                    FileAsset.original_filename.ilike(pattern),
                    FileAsset.external_url.ilike(pattern),
                    FileAsset.version.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for file_asset in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "name": file_asset.name,
                    "description": file_asset.description,
                    "original_filename": file_asset.original_filename,
                    "external_url": file_asset.external_url,
                    "version": file_asset.version,
                },
            )
            description = file_asset.description or file_asset.external_url
            results.append(
                SearchResult(
                    id=file_asset.id,
                    type=SearchResultType.FILE,
                    title=file_asset.name,
                    description=description,
                    status=str(file_asset.status),
                    secondary_status=str(file_asset.sensitivity),
                    url=build_file_url(file_asset.id),
                    matched_field=matched_field,
                    updated_at=file_asset.updated_at,
                )
            )
        return results

    async def _search_policies(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(Policy), Policy, company_id)
            .where(
                or_(
                    Policy.name.ilike(pattern),
                    Policy.description.ilike(pattern),
                    Policy.version.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for policy in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "name": policy.name,
                    "description": policy.description,
                    "version": policy.version,
                },
            )
            results.append(
                SearchResult(
                    id=policy.id,
                    type=SearchResultType.POLICY,
                    title=policy.name,
                    description=policy.description,
                    status=str(policy.status),
                    secondary_status=policy.version,
                    url=build_policy_url(policy.id),
                    matched_field=matched_field,
                    updated_at=policy.updated_at,
                )
            )
        return results

    async def _search_compliance_checks(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(ComplianceCheck), ComplianceCheck, company_id)
            .where(
                or_(
                    ComplianceCheck.title.ilike(pattern),
                    ComplianceCheck.description.ilike(pattern),
                    ComplianceCheck.result_summary.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for check in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "title": check.title,
                    "description": check.description,
                    "result_summary": check.result_summary,
                },
            )
            results.append(
                SearchResult(
                    id=check.id,
                    type=SearchResultType.COMPLIANCE_CHECK,
                    title=check.title,
                    description=check.description,
                    status=str(check.status),
                    secondary_status=str(check.check_type),
                    url=build_compliance_check_url(check.id),
                    matched_field=matched_field,
                    updated_at=check.updated_at,
                )
            )
        return results

    async def _search_automation_triggers(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(AutomationTrigger), AutomationTrigger, company_id)
            .where(
                or_(
                    AutomationTrigger.name.ilike(pattern),
                    AutomationTrigger.description.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for trigger in rows.all():
            matched_field = detect_matched_field(
                query,
                {"name": trigger.name, "description": trigger.description},
            )
            results.append(
                SearchResult(
                    id=trigger.id,
                    type=SearchResultType.AUTOMATION_TRIGGER,
                    title=trigger.name,
                    description=trigger.description,
                    status=str(trigger.status),
                    secondary_status=str(trigger.action_type),
                    url=build_automation_trigger_url(trigger.id),
                    matched_field=matched_field,
                    updated_at=trigger.updated_at,
                )
            )
        return results

    async def _search_notification_templates(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(NotificationTemplate), NotificationTemplate, company_id)
            .where(
                or_(
                    NotificationTemplate.name.ilike(pattern),
                    NotificationTemplate.description.ilike(pattern),
                    NotificationTemplate.body_template.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for template in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "name": template.name,
                    "description": template.description,
                    "body_template": template.body_template,
                },
            )
            results.append(
                SearchResult(
                    id=template.id,
                    type=SearchResultType.NOTIFICATION_TEMPLATE,
                    title=template.name,
                    description=template.description,
                    status=str(template.status),
                    secondary_status=template.event_type,
                    url=build_notification_template_url(template.id),
                    matched_field=matched_field,
                    updated_at=template.updated_at,
                )
            )
        return results

    async def _search_notification_messages(
        self, query: str, *, company_id: uuid.UUID | None = None
    ) -> list[SearchResult]:
        pattern = f"%{query}%"
        rows = await self._session.scalars(
            self._company_scope(select(NotificationMessage), NotificationMessage, company_id)
            .where(
                or_(
                    NotificationMessage.subject.ilike(pattern),
                    NotificationMessage.body.ilike(pattern),
                    NotificationMessage.recipient_value.ilike(pattern),
                )
            )
            .limit(PER_TYPE_FETCH_LIMIT)
        )
        results: list[SearchResult] = []
        for message in rows.all():
            matched_field = detect_matched_field(
                query,
                {
                    "subject": message.subject,
                    "body": message.body,
                    "recipient_value": message.recipient_value,
                },
            )
            results.append(
                SearchResult(
                    id=message.id,
                    type=SearchResultType.NOTIFICATION_MESSAGE,
                    title=message.subject or "Notification message",
                    description=message.body[:200] if message.body else None,
                    status=str(message.status),
                    secondary_status=str(message.priority),
                    url=build_notification_message_url(message.id),
                    matched_field=matched_field,
                    updated_at=message.updated_at,
                )
            )
        return results


def _project_to_lookup(project: Project) -> EntityLookupResult:
    result_type = project_search_result_type(project.project_type)
    return EntityLookupResult(
        id=project.id,
        type=result_type,
        title=project.name,
        description=project.description,
        status=str(project.status.value),
        secondary_status=project.health_status,
        url=build_project_url(project.id, project.project_type),
    )


def _file_to_lookup(file_asset: FileAsset) -> EntityLookupResult:
    return EntityLookupResult(
        id=file_asset.id,
        type=SearchResultType.FILE,
        title=file_asset.name,
        description=file_asset.description or file_asset.external_url,
        status=str(file_asset.status),
        secondary_status=str(file_asset.sensitivity),
        url=build_file_url(file_asset.id),
    )
