import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import (
    ActivityAction,
    ActivityEntityType,
    ComplianceCheckType,
    ComplianceStatus,
    ComplianceSubjectType,
    FileEntityType,
)
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.compliance.errors import (
    ComplianceCheckNotFoundError,
    ComplianceConflictError,
    ComplianceEvidenceConflictError,
    ComplianceEvidenceNotFoundError,
    ComplianceRuleNotFoundError,
    ControlNotFoundError,
    PolicyNotFoundError,
    UnsupportedComplianceSubjectTypeError,
)
from app.modules.compliance.repository import (
    OPEN_CHECK_STATUSES,
    ComplianceRepository,
)
from app.modules.compliance.schemas import (
    ComplianceCheckCreate,
    ComplianceCheckFilters,
    ComplianceCheckListItem,
    ComplianceCheckListResponse,
    ComplianceCheckRead,
    ComplianceCheckUpdate,
    ComplianceEvidenceCreate,
    ComplianceEvidenceRead,
    ComplianceEvidenceUpdate,
    ComplianceOverview,
    ComplianceRuleCreate,
    ComplianceRuleRead,
    ComplianceRuleUpdate,
    ControlCreate,
    ControlFilters,
    ControlListResponse,
    ControlRead,
    ControlUpdate,
    EntityComplianceResponse,
    PolicyCreate,
    PolicyFilters,
    PolicyListItem,
    PolicyListResponse,
    PolicyRead,
    PolicyUpdate,
    RuleFilters,
    RuleListResponse,
)
from app.modules.compliance.validators import (
    is_supported_compliance_subject_type,
    validate_compliance_subject_exists,
)
from app.modules.files.errors import FileAssetNotFoundError
from app.modules.files.repository import FileRepository


class ComplianceService:
    def __init__(
        self,
        repository: ComplianceRepository,
        file_repository: FileRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._files = file_repository
        self._activity = activity_service
        self._session = session

    def _enum_value(self, value) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    def _to_activity_entity_type(
        self,
        subject_type: ComplianceSubjectType,
    ) -> ActivityEntityType | None:
        try:
            return ActivityEntityType(subject_type.value)
        except ValueError:
            return None

    def _to_file_entity_type(
        self,
        subject_type: ComplianceSubjectType,
    ) -> FileEntityType | None:
        mapping = {
            ComplianceSubjectType.DATA_PRODUCT: FileEntityType.DATA_PRODUCT,
            ComplianceSubjectType.PROJECT: FileEntityType.PROJECT,
            ComplianceSubjectType.INTERNAL_PROJECT: FileEntityType.INTERNAL_PROJECT,
        }
        return mapping.get(subject_type)

    def _check_to_list_item(self, check) -> ComplianceCheckListItem:
        return ComplianceCheckListItem(
            id=check.id,
            subject_type=ComplianceSubjectType(check.subject_type),
            subject_id=check.subject_id,
            title=check.title,
            status=ComplianceStatus(check.status),
            check_type=ComplianceCheckType(check.check_type),
            owner_id=check.owner_id,
            due_date=check.due_date,
            completed_at=check.completed_at,
            next_check_at=check.next_check_at,
            rule_id=check.rule_id,
            control_id=check.control_id,
            updated_at=check.updated_at,
        )

    async def _record_check_activity(
        self,
        *,
        subject_type: ComplianceSubjectType,
        subject_id: uuid.UUID,
        title: str,
        description: str,
        check_id: uuid.UUID,
        created: bool,
    ) -> None:
        activity_entity_type = self._to_activity_entity_type(subject_type)
        if activity_entity_type is None:
            return
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=activity_entity_type,
                entity_id=subject_id,
                action=ActivityAction.UPDATED,
                title="Compliance check created" if created else "Compliance check updated",
                description=description,
                details={"check_id": str(check_id), "title": title},
            )
        )

    async def _record_evidence_activity(
        self,
        *,
        subject_type: ComplianceSubjectType,
        subject_id: uuid.UUID,
        file_name: str,
        evidence_id: uuid.UUID,
    ) -> None:
        activity_entity_type = self._to_activity_entity_type(subject_type)
        if activity_entity_type is None:
            return
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=activity_entity_type,
                entity_id=subject_id,
                action=ActivityAction.LINKED,
                title="Compliance evidence added",
                description=file_name,
                details={"evidence_id": str(evidence_id)},
            )
        )

    async def _ensure_file_attachment_for_evidence(
        self,
        *,
        check: object,
        file_id: uuid.UUID,
        purpose: str,
    ) -> None:
        subject_type = ComplianceSubjectType(check.subject_type)
        file_entity_type = self._to_file_entity_type(subject_type)
        if file_entity_type is None:
            return

        duplicate = await self._files.get_duplicate_attachment(
            file_id=file_id,
            entity_type=file_entity_type,
            entity_id=check.subject_id,
            purpose=purpose,
        )
        if duplicate is not None:
            return

        await self._files.create_attachment(
            {
                "file_id": file_id,
                "entity_type": file_entity_type.value,
                "entity_id": check.subject_id,
                "purpose": purpose,
                "is_evidence": True,
                "evidence_type": "compliance",
            }
        )

    async def _validate_rule_and_control(
        self,
        *,
        rule_id: uuid.UUID | None,
        control_id: uuid.UUID | None,
    ) -> None:
        if rule_id is not None:
            rule = await self._repository.get_rule_by_id(rule_id)
            if rule is None:
                raise ComplianceRuleNotFoundError(rule_id)
        if control_id is not None:
            control = await self._repository.get_control_by_id(control_id)
            if control is None:
                raise ControlNotFoundError(control_id)

    async def list_policies(
        self,
        *,
        filters: PolicyFilters,
        page: int,
        page_size: int,
    ) -> PolicyListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_policies(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return PolicyListResponse(
            items=[PolicyListItem.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_policy(self, policy_id: uuid.UUID) -> PolicyRead:
        policy = await self._repository.get_policy_by_id(policy_id)
        if policy is None:
            raise PolicyNotFoundError(policy_id)
        return PolicyRead.model_validate(policy)

    async def create_policy(self, payload: PolicyCreate) -> PolicyRead:
        existing = await self._repository.get_policy_by_name(payload.name)
        if existing is not None:
            raise ComplianceConflictError(f"Policy already exists: {payload.name}")
        data = payload.model_dump()
        data["status"] = self._enum_value(data["status"])
        policy = await self._repository.create_policy(data)
        return PolicyRead.model_validate(policy)

    async def update_policy(self, policy_id: uuid.UUID, payload: PolicyUpdate) -> PolicyRead:
        policy = await self._repository.get_policy_by_id(policy_id)
        if policy is None:
            raise PolicyNotFoundError(policy_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = await self._repository.get_policy_by_name(update_data["name"])
            if existing is not None and existing.id != policy_id:
                raise ComplianceConflictError(f"Policy already exists: {update_data['name']}")
        if "status" in update_data:
            update_data["status"] = self._enum_value(update_data["status"])
        updated = await self._repository.update_policy(policy, update_data)
        return PolicyRead.model_validate(updated)

    async def delete_policy(self, policy_id: uuid.UUID) -> None:
        policy = await self._repository.get_policy_by_id(policy_id)
        if policy is None:
            raise PolicyNotFoundError(policy_id)
        await self._repository.delete_policy(policy)

    async def list_rules(
        self,
        *,
        filters: RuleFilters,
        page: int,
        page_size: int,
    ) -> RuleListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_rules(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return RuleListResponse(
            items=[ComplianceRuleRead.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_rule(self, rule_id: uuid.UUID) -> ComplianceRuleRead:
        rule = await self._repository.get_rule_by_id(rule_id)
        if rule is None:
            raise ComplianceRuleNotFoundError(rule_id)
        return ComplianceRuleRead.model_validate(rule)

    async def create_rule(self, payload: ComplianceRuleCreate) -> ComplianceRuleRead:
        policy = await self._repository.get_policy_by_id(payload.policy_id)
        if policy is None:
            raise PolicyNotFoundError(payload.policy_id)
        data = payload.model_dump()
        data["severity"] = self._enum_value(data["severity"])
        if data.get("subject_type") is not None:
            data["subject_type"] = self._enum_value(data["subject_type"])
        rule = await self._repository.create_rule(data)
        return ComplianceRuleRead.model_validate(rule)

    async def update_rule(
        self, rule_id: uuid.UUID, payload: ComplianceRuleUpdate
    ) -> ComplianceRuleRead:
        rule = await self._repository.get_rule_by_id(rule_id)
        if rule is None:
            raise ComplianceRuleNotFoundError(rule_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "severity" in update_data:
            update_data["severity"] = self._enum_value(update_data["severity"])
        if "subject_type" in update_data and update_data["subject_type"] is not None:
            update_data["subject_type"] = self._enum_value(update_data["subject_type"])
        updated = await self._repository.update_rule(rule, update_data)
        return ComplianceRuleRead.model_validate(updated)

    async def delete_rule(self, rule_id: uuid.UUID) -> None:
        rule = await self._repository.get_rule_by_id(rule_id)
        if rule is None:
            raise ComplianceRuleNotFoundError(rule_id)
        await self._repository.delete_rule(rule)

    async def list_controls(
        self,
        *,
        filters: ControlFilters,
        page: int,
        page_size: int,
    ) -> ControlListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_controls(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return ControlListResponse(
            items=[ControlRead.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_control(self, control_id: uuid.UUID) -> ControlRead:
        control = await self._repository.get_control_by_id(control_id)
        if control is None:
            raise ControlNotFoundError(control_id)
        return ControlRead.model_validate(control)

    async def create_control(self, payload: ControlCreate) -> ControlRead:
        rule = await self._repository.get_rule_by_id(payload.rule_id)
        if rule is None:
            raise ComplianceRuleNotFoundError(payload.rule_id)
        data = payload.model_dump()
        data["control_type"] = self._enum_value(data["control_type"])
        data["status"] = self._enum_value(data["status"])
        if data.get("frequency") is not None:
            data["frequency"] = self._enum_value(data["frequency"])
        control = await self._repository.create_control(data)
        return ControlRead.model_validate(control)

    async def update_control(self, control_id: uuid.UUID, payload: ControlUpdate) -> ControlRead:
        control = await self._repository.get_control_by_id(control_id)
        if control is None:
            raise ControlNotFoundError(control_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key in ("control_type", "status", "frequency"):
            if key in update_data and update_data[key] is not None:
                update_data[key] = self._enum_value(update_data[key])
        updated = await self._repository.update_control(control, update_data)
        return ControlRead.model_validate(updated)

    async def delete_control(self, control_id: uuid.UUID) -> None:
        control = await self._repository.get_control_by_id(control_id)
        if control is None:
            raise ControlNotFoundError(control_id)
        await self._repository.delete_control(control)

    async def list_checks(
        self,
        *,
        filters: ComplianceCheckFilters,
        page: int,
        page_size: int,
    ) -> ComplianceCheckListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_checks(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return ComplianceCheckListResponse(
            items=[self._check_to_list_item(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_check(self, check_id: uuid.UUID) -> ComplianceCheckRead:
        check = await self._repository.get_check_by_id(check_id)
        if check is None:
            raise ComplianceCheckNotFoundError(check_id)
        return ComplianceCheckRead.model_validate(check)

    async def create_check(self, payload: ComplianceCheckCreate) -> ComplianceCheckRead:
        if not is_supported_compliance_subject_type(payload.subject_type):
            raise UnsupportedComplianceSubjectTypeError(payload.subject_type.value)
        await validate_compliance_subject_exists(
            self._session,
            payload.subject_type,
            payload.subject_id,
        )
        await self._validate_rule_and_control(
            rule_id=payload.rule_id,
            control_id=payload.control_id,
        )
        data = payload.model_dump()
        for key in ("subject_type", "check_type", "status"):
            data[key] = self._enum_value(data[key])
        check = await self._repository.create_check(data)
        await self._record_check_activity(
            subject_type=payload.subject_type,
            subject_id=payload.subject_id,
            title=check.title,
            description=check.title,
            check_id=check.id,
            created=True,
        )
        return ComplianceCheckRead.model_validate(check)

    async def update_check(
        self,
        check_id: uuid.UUID,
        payload: ComplianceCheckUpdate,
    ) -> ComplianceCheckRead:
        check = await self._repository.get_check_by_id(check_id)
        if check is None:
            raise ComplianceCheckNotFoundError(check_id)
        update_data = payload.model_dump(exclude_unset=True)
        subject_type = ComplianceSubjectType(update_data.get("subject_type", check.subject_type))
        subject_id = update_data.get("subject_id", check.subject_id)
        if "subject_type" in update_data or "subject_id" in update_data:
            if not is_supported_compliance_subject_type(subject_type):
                raise UnsupportedComplianceSubjectTypeError(subject_type.value)
            await validate_compliance_subject_exists(self._session, subject_type, subject_id)
        await self._validate_rule_and_control(
            rule_id=update_data.get("rule_id", check.rule_id),
            control_id=update_data.get("control_id", check.control_id),
        )
        for key in ("subject_type", "check_type", "status"):
            if key in update_data and update_data[key] is not None:
                update_data[key] = self._enum_value(update_data[key])
        updated = await self._repository.update_check(check, update_data)
        await self._record_check_activity(
            subject_type=ComplianceSubjectType(updated.subject_type),
            subject_id=updated.subject_id,
            title=updated.title,
            description=updated.title,
            check_id=updated.id,
            created=False,
        )
        return ComplianceCheckRead.model_validate(updated)

    async def delete_check(self, check_id: uuid.UUID) -> None:
        check = await self._repository.get_check_by_id(check_id)
        if check is None:
            raise ComplianceCheckNotFoundError(check_id)
        await self._repository.delete_check(check)

    async def get_entity_compliance(
        self,
        subject_type: ComplianceSubjectType,
        subject_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> EntityComplianceResponse:
        if not is_supported_compliance_subject_type(subject_type):
            raise UnsupportedComplianceSubjectTypeError(subject_type.value)
        await validate_compliance_subject_exists(self._session, subject_type, subject_id)
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_checks_for_subject(
            subject_type=subject_type,
            subject_id=subject_id,
            offset=offset,
            limit=normalized_page_size,
        )
        today = date.today()
        list_items = [self._check_to_list_item(item) for item in items]
        compliant_count = sum(1 for i in list_items if i.status == ComplianceStatus.COMPLIANT)
        non_compliant_count = sum(
            1 for i in list_items if i.status == ComplianceStatus.NON_COMPLIANT
        )
        open_count = sum(1 for i in list_items if i.status in OPEN_CHECK_STATUSES)
        overdue_count = sum(
            1
            for i in list_items
            if i.due_date is not None and i.due_date < today and i.status in OPEN_CHECK_STATUSES
        )
        return EntityComplianceResponse(
            subject_type=subject_type,
            subject_id=subject_id,
            checks=list_items,
            total=total,
            compliant_count=compliant_count,
            non_compliant_count=non_compliant_count,
            open_count=open_count,
            overdue_count=overdue_count,
        )

    async def list_check_evidence(self, check_id: uuid.UUID) -> list[ComplianceEvidenceRead]:
        check = await self._repository.get_check_by_id(check_id)
        if check is None:
            raise ComplianceCheckNotFoundError(check_id)
        items = await self._repository.list_evidence_for_check(check_id)
        return [ComplianceEvidenceRead.model_validate(item) for item in items]

    async def add_evidence(
        self,
        check_id: uuid.UUID,
        payload: ComplianceEvidenceCreate,
    ) -> ComplianceEvidenceRead:
        check = await self._repository.get_check_by_id(check_id)
        if check is None:
            raise ComplianceCheckNotFoundError(check_id)

        file_asset = await self._files.get_file_by_id(payload.file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(payload.file_id)

        duplicate = await self._repository.get_duplicate_evidence(
            check_id=check_id,
            file_id=payload.file_id,
        )
        if duplicate is not None:
            raise ComplianceEvidenceConflictError()

        data = payload.model_dump()
        data["compliance_check_id"] = check_id
        data["status"] = self._enum_value(data["status"])
        evidence = await self._repository.create_evidence(data)

        await self._ensure_file_attachment_for_evidence(
            check=check,
            file_id=payload.file_id,
            purpose=check.title,
        )

        await self._record_evidence_activity(
            subject_type=ComplianceSubjectType(check.subject_type),
            subject_id=check.subject_id,
            file_name=file_asset.name,
            evidence_id=evidence.id,
        )

        return ComplianceEvidenceRead.model_validate(evidence)

    async def update_evidence(
        self,
        evidence_id: uuid.UUID,
        payload: ComplianceEvidenceUpdate,
    ) -> ComplianceEvidenceRead:
        evidence = await self._repository.get_evidence_by_id(evidence_id)
        if evidence is None:
            raise ComplianceEvidenceNotFoundError(evidence_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = self._enum_value(update_data["status"])
        updated = await self._repository.update_evidence(evidence, update_data)
        return ComplianceEvidenceRead.model_validate(updated)

    async def delete_evidence(self, evidence_id: uuid.UUID) -> None:
        evidence = await self._repository.get_evidence_by_id(evidence_id)
        if evidence is None:
            raise ComplianceEvidenceNotFoundError(evidence_id)
        await self._repository.delete_evidence(evidence)

    async def get_overview(self) -> ComplianceOverview:
        data = await self._repository.get_overview()
        return ComplianceOverview.model_validate(data)
