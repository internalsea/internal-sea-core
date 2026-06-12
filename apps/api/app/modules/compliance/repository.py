import uuid
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import (
    ComplianceStatus,
    ComplianceSubjectType,
    ControlStatus,
    EvidenceStatus,
    PolicyStatus,
    RuleSeverity,
)
from app.models.compliance import (
    ComplianceCheck,
    ComplianceCheckEvidence,
    ComplianceRule,
    Control,
    Policy,
)
from app.modules.compliance.schemas import (
    ComplianceCheckFilters,
    ControlFilters,
    PolicyFilters,
    RuleFilters,
)

OPEN_CHECK_STATUSES = (ComplianceStatus.NOT_STARTED, ComplianceStatus.IN_PROGRESS)
CLOSED_CHECK_STATUSES = (
    ComplianceStatus.COMPLIANT,
    ComplianceStatus.NON_COMPLIANT,
    ComplianceStatus.EXCEPTION,
    ComplianceStatus.NOT_APPLICABLE,
)

SEVERITY_ORDER = {
    RuleSeverity.CRITICAL: 0,
    RuleSeverity.HIGH: 1,
    RuleSeverity.MEDIUM: 2,
    RuleSeverity.LOW: 3,
}


class ComplianceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _enum_value(self, value) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    async def list_policies(
        self,
        *,
        filters: PolicyFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Policy], int]:
        query = select(Policy)
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(Policy.name.ilike(pattern), Policy.description.ilike(pattern))
            )
        if filters.status is not None:
            query = query.where(Policy.status == filters.status.value)
        if filters.owner_id is not None:
            query = query.where(Policy.owner_id == filters.owner_id)

        total = int(
            await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0
        )
        result = await self._session.scalars(
            query.order_by(Policy.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_policy_by_id(self, policy_id: uuid.UUID) -> Policy | None:
        return await self._session.get(Policy, policy_id)

    async def get_policy_by_name(self, name: str) -> Policy | None:
        result = await self._session.execute(select(Policy).where(Policy.name == name))
        return result.scalar_one_or_none()

    async def create_policy(self, data: dict[str, object]) -> Policy:
        policy = Policy(**data)
        self._session.add(policy)
        await self._session.commit()
        await self._session.refresh(policy)
        return policy

    async def update_policy(self, policy: Policy, data: dict[str, object]) -> Policy:
        for key, value in data.items():
            setattr(policy, key, value)
        await self._session.commit()
        await self._session.refresh(policy)
        return policy

    async def delete_policy(self, policy: Policy) -> None:
        await self._session.delete(policy)
        await self._session.commit()

    async def list_rules(
        self,
        *,
        filters: RuleFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[ComplianceRule], int]:
        query = select(ComplianceRule)
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    ComplianceRule.name.ilike(pattern),
                    ComplianceRule.code.ilike(pattern),
                    ComplianceRule.description.ilike(pattern),
                )
            )
        if filters.policy_id is not None:
            query = query.where(ComplianceRule.policy_id == filters.policy_id)
        if filters.severity is not None:
            query = query.where(ComplianceRule.severity == filters.severity.value)
        if filters.subject_type is not None:
            query = query.where(ComplianceRule.subject_type == filters.subject_type.value)
        if filters.is_active is not None:
            query = query.where(ComplianceRule.is_active.is_(filters.is_active))

        total = int(
            await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0
        )
        result = await self._session.scalars(
            query.order_by(ComplianceRule.updated_at.desc()).offset(offset).limit(limit)
        )
        items = list(result.all())
        items.sort(
            key=lambda item: (
                SEVERITY_ORDER.get(RuleSeverity(item.severity), 99),
                -item.updated_at.timestamp(),
            )
        )
        return items, total

    async def get_rule_by_id(self, rule_id: uuid.UUID) -> ComplianceRule | None:
        return await self._session.get(ComplianceRule, rule_id)

    async def create_rule(self, data: dict[str, object]) -> ComplianceRule:
        rule = ComplianceRule(**data)
        self._session.add(rule)
        await self._session.commit()
        await self._session.refresh(rule)
        return rule

    async def update_rule(self, rule: ComplianceRule, data: dict[str, object]) -> ComplianceRule:
        for key, value in data.items():
            setattr(rule, key, value)
        await self._session.commit()
        await self._session.refresh(rule)
        return rule

    async def delete_rule(self, rule: ComplianceRule) -> None:
        await self._session.delete(rule)
        await self._session.commit()

    async def list_controls(
        self,
        *,
        filters: ControlFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Control], int]:
        query = select(Control)
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(Control.name.ilike(pattern), Control.description.ilike(pattern))
            )
        if filters.rule_id is not None:
            query = query.where(Control.rule_id == filters.rule_id)
        if filters.control_type is not None:
            query = query.where(Control.control_type == filters.control_type.value)
        if filters.status is not None:
            query = query.where(Control.status == filters.status.value)
        if filters.owner_id is not None:
            query = query.where(Control.owner_id == filters.owner_id)
        if filters.frequency is not None:
            query = query.where(Control.frequency == filters.frequency.value)

        total = int(
            await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0
        )
        result = await self._session.scalars(
            query.order_by(Control.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_control_by_id(self, control_id: uuid.UUID) -> Control | None:
        return await self._session.get(Control, control_id)

    async def create_control(self, data: dict[str, object]) -> Control:
        control = Control(**data)
        self._session.add(control)
        await self._session.commit()
        await self._session.refresh(control)
        return control

    async def update_control(self, control: Control, data: dict[str, object]) -> Control:
        for key, value in data.items():
            setattr(control, key, value)
        await self._session.commit()
        await self._session.refresh(control)
        return control

    async def delete_control(self, control: Control) -> None:
        await self._session.delete(control)
        await self._session.commit()

    def _apply_check_filters(self, query, filters: ComplianceCheckFilters, *, today: date):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    ComplianceCheck.title.ilike(pattern),
                    ComplianceCheck.description.ilike(pattern),
                    ComplianceCheck.result_summary.ilike(pattern),
                )
            )
        if filters.subject_type is not None:
            query = query.where(ComplianceCheck.subject_type == filters.subject_type.value)
        if filters.subject_id is not None:
            query = query.where(ComplianceCheck.subject_id == filters.subject_id)
        if filters.status is not None:
            query = query.where(ComplianceCheck.status == filters.status.value)
        if filters.check_type is not None:
            query = query.where(ComplianceCheck.check_type == filters.check_type.value)
        if filters.rule_id is not None:
            query = query.where(ComplianceCheck.rule_id == filters.rule_id)
        if filters.control_id is not None:
            query = query.where(ComplianceCheck.control_id == filters.control_id)
        if filters.owner_id is not None:
            query = query.where(ComplianceCheck.owner_id == filters.owner_id)
        if filters.due_before is not None:
            query = query.where(ComplianceCheck.due_date <= filters.due_before)
        if filters.due_after is not None:
            query = query.where(ComplianceCheck.due_date >= filters.due_after)
        if filters.overdue is True:
            query = query.where(
                ComplianceCheck.due_date < today,
                ComplianceCheck.status.in_([s.value for s in OPEN_CHECK_STATUSES]),
            )
        return query

    async def list_checks(
        self,
        *,
        filters: ComplianceCheckFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[ComplianceCheck], int]:
        today = date.today()
        query = select(ComplianceCheck)
        query = self._apply_check_filters(query, filters, today=today)
        total = int(
            await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0
        )
        result = await self._session.scalars(
            query.order_by(
                ComplianceCheck.due_date.asc().nulls_last(),
                ComplianceCheck.updated_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def list_checks_for_subject(
        self,
        *,
        subject_type: ComplianceSubjectType,
        subject_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[ComplianceCheck], int]:
        query = select(ComplianceCheck).where(
            ComplianceCheck.subject_type == subject_type.value,
            ComplianceCheck.subject_id == subject_id,
        )
        total = int(await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0)
        result = await self._session.scalars(
            query.order_by(
                ComplianceCheck.due_date.asc().nulls_last(),
                ComplianceCheck.updated_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_check_by_id(self, check_id: uuid.UUID) -> ComplianceCheck | None:
        return await self._session.get(ComplianceCheck, check_id)

    async def create_check(self, data: dict[str, object]) -> ComplianceCheck:
        check = ComplianceCheck(**data)
        self._session.add(check)
        await self._session.commit()
        await self._session.refresh(check)
        return check

    async def update_check(self, check: ComplianceCheck, data: dict[str, object]) -> ComplianceCheck:
        for key, value in data.items():
            setattr(check, key, value)
        await self._session.commit()
        await self._session.refresh(check)
        return check

    async def delete_check(self, check: ComplianceCheck) -> None:
        await self._session.delete(check)
        await self._session.commit()

    async def list_evidence_for_check(
        self,
        check_id: uuid.UUID,
    ) -> list[ComplianceCheckEvidence]:
        result = await self._session.scalars(
            select(ComplianceCheckEvidence)
            .where(ComplianceCheckEvidence.compliance_check_id == check_id)
            .order_by(ComplianceCheckEvidence.created_at.desc())
        )
        return list(result.all())

    async def get_evidence_by_id(self, evidence_id: uuid.UUID) -> ComplianceCheckEvidence | None:
        return await self._session.get(ComplianceCheckEvidence, evidence_id)

    async def get_duplicate_evidence(
        self,
        *,
        check_id: uuid.UUID,
        file_id: uuid.UUID,
    ) -> ComplianceCheckEvidence | None:
        result = await self._session.execute(
            select(ComplianceCheckEvidence).where(
                ComplianceCheckEvidence.compliance_check_id == check_id,
                ComplianceCheckEvidence.file_id == file_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_evidence(self, data: dict[str, object]) -> ComplianceCheckEvidence:
        evidence = ComplianceCheckEvidence(**data)
        self._session.add(evidence)
        await self._session.commit()
        await self._session.refresh(evidence)
        return evidence

    async def update_evidence(
        self,
        evidence: ComplianceCheckEvidence,
        data: dict[str, object],
    ) -> ComplianceCheckEvidence:
        for key, value in data.items():
            setattr(evidence, key, value)
        await self._session.commit()
        await self._session.refresh(evidence)
        return evidence

    async def delete_evidence(self, evidence: ComplianceCheckEvidence) -> None:
        await self._session.delete(evidence)
        await self._session.commit()

    async def get_overview(self) -> dict[str, int]:
        today = date.today()
        policies_total = int(await self._session.scalar(select(func.count(Policy.id))) or 0)
        policies_active = int(
            await self._session.scalar(
                select(func.count(Policy.id)).where(Policy.status == PolicyStatus.ACTIVE.value)
            )
            or 0
        )
        rules_total = int(await self._session.scalar(select(func.count(ComplianceRule.id))) or 0)
        active_rules = int(
            await self._session.scalar(
                select(func.count(ComplianceRule.id)).where(ComplianceRule.is_active.is_(True))
            )
            or 0
        )
        controls_total = int(await self._session.scalar(select(func.count(Control.id))) or 0)
        active_controls = int(
            await self._session.scalar(
                select(func.count(Control.id)).where(Control.status == ControlStatus.ACTIVE.value)
            )
            or 0
        )
        checks_total = int(await self._session.scalar(select(func.count(ComplianceCheck.id))) or 0)
        checks_open = int(
            await self._session.scalar(
                select(func.count(ComplianceCheck.id)).where(
                    ComplianceCheck.status.in_([s.value for s in OPEN_CHECK_STATUSES])
                )
            )
            or 0
        )
        checks_compliant = int(
            await self._session.scalar(
                select(func.count(ComplianceCheck.id)).where(
                    ComplianceCheck.status == ComplianceStatus.COMPLIANT.value
                )
            )
            or 0
        )
        checks_non_compliant = int(
            await self._session.scalar(
                select(func.count(ComplianceCheck.id)).where(
                    ComplianceCheck.status == ComplianceStatus.NON_COMPLIANT.value
                )
            )
            or 0
        )
        checks_overdue = int(
            await self._session.scalar(
                select(func.count(ComplianceCheck.id)).where(
                    ComplianceCheck.due_date < today,
                    ComplianceCheck.status.in_([s.value for s in OPEN_CHECK_STATUSES]),
                )
            )
            or 0
        )
        evidence_missing = int(
            await self._session.scalar(
                select(func.count(ComplianceCheck.id)).where(
                    ComplianceCheck.status.in_([s.value for s in OPEN_CHECK_STATUSES]),
                    ~ComplianceCheck.id.in_(
                        select(ComplianceCheckEvidence.compliance_check_id).distinct()
                    ),
                )
            )
            or 0
        )
        return {
            "policies_total": policies_total,
            "policies_active": policies_active,
            "rules_total": rules_total,
            "active_rules": active_rules,
            "controls_total": controls_total,
            "active_controls": active_controls,
            "checks_total": checks_total,
            "checks_open": checks_open,
            "checks_compliant": checks_compliant,
            "checks_non_compliant": checks_non_compliant,
            "checks_overdue": checks_overdue,
            "evidence_missing": evidence_missing,
        }
