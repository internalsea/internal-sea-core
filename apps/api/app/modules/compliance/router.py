import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import (
    ComplianceCheckType,
    ComplianceFrequency,
    ComplianceStatus,
    ComplianceSubjectType,
    ControlStatus,
    ControlType,
    PolicyStatus,
    RuleSeverity,
)
from app.modules.activity.dependencies import build_activity_service
from app.modules.compliance.repository import ComplianceRepository
from app.modules.compliance.schemas import (
    ComplianceCheckCreate,
    ComplianceCheckFilters,
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
    PolicyListResponse,
    PolicyRead,
    PolicyUpdate,
    RuleFilters,
    RuleListResponse,
)
from app.modules.compliance.service import ComplianceService
from app.modules.files.repository import FileRepository

router = APIRouter(prefix="/compliance", tags=["Compliance"])


def get_compliance_service(db: AsyncSession = Depends(get_db)) -> ComplianceService:
    return ComplianceService(
        ComplianceRepository(db),
        FileRepository(db),
        build_activity_service(db),
        db,
    )


@router.get("/overview", response_model=ComplianceOverview)
async def get_compliance_overview(
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceOverview:
    return await service.get_overview()


@router.get("/policies", response_model=PolicyListResponse)
async def list_policies(
    _user: ViewerUser,
    search: str | None = None,
    status: PolicyStatus | None = None,
    owner_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> PolicyListResponse:
    filters = PolicyFilters(search=search, status=status, owner_id=owner_id)
    return await service.list_policies(filters=filters, page=page, page_size=page_size)


@router.post("/policies", response_model=PolicyRead, status_code=status.HTTP_201_CREATED)
async def create_policy(
    payload: PolicyCreate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> PolicyRead:
    return await service.create_policy(payload)


@router.get("/policies/{policy_id}", response_model=PolicyRead)
async def get_policy(
    policy_id: uuid.UUID,
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> PolicyRead:
    return await service.get_policy(policy_id)


@router.patch("/policies/{policy_id}", response_model=PolicyRead)
async def update_policy(
    policy_id: uuid.UUID,
    payload: PolicyUpdate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> PolicyRead:
    return await service.update_policy(policy_id, payload)


@router.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: uuid.UUID,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> None:
    await service.delete_policy(policy_id)


@router.get("/policies/{policy_id}/rules", response_model=RuleListResponse)
async def list_policy_rules(
    policy_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> RuleListResponse:
    filters = RuleFilters(policy_id=policy_id)
    return await service.list_rules(filters=filters, page=page, page_size=page_size)


@router.get("/rules", response_model=RuleListResponse)
async def list_rules(
    _user: ViewerUser,
    search: str | None = None,
    policy_id: uuid.UUID | None = None,
    severity: RuleSeverity | None = None,
    subject_type: ComplianceSubjectType | None = None,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> RuleListResponse:
    filters = RuleFilters(
        search=search,
        policy_id=policy_id,
        severity=severity,
        subject_type=subject_type,
        is_active=is_active,
    )
    return await service.list_rules(filters=filters, page=page, page_size=page_size)


@router.post("/rules", response_model=ComplianceRuleRead, status_code=status.HTTP_201_CREATED)
async def create_rule(
    payload: ComplianceRuleCreate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceRuleRead:
    return await service.create_rule(payload)


@router.get("/rules/{rule_id}", response_model=ComplianceRuleRead)
async def get_rule(
    rule_id: uuid.UUID,
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceRuleRead:
    return await service.get_rule(rule_id)


@router.patch("/rules/{rule_id}", response_model=ComplianceRuleRead)
async def update_rule(
    rule_id: uuid.UUID,
    payload: ComplianceRuleUpdate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceRuleRead:
    return await service.update_rule(rule_id, payload)


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: uuid.UUID,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> None:
    await service.delete_rule(rule_id)


@router.get("/rules/{rule_id}/controls", response_model=ControlListResponse)
async def list_rule_controls(
    rule_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> ControlListResponse:
    filters = ControlFilters(rule_id=rule_id)
    return await service.list_controls(filters=filters, page=page, page_size=page_size)


@router.get("/controls", response_model=ControlListResponse)
async def list_controls(
    _user: ViewerUser,
    search: str | None = None,
    rule_id: uuid.UUID | None = None,
    control_type: ControlType | None = None,
    status: ControlStatus | None = None,
    owner_id: uuid.UUID | None = None,
    frequency: ComplianceFrequency | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> ControlListResponse:
    filters = ControlFilters(
        search=search,
        rule_id=rule_id,
        control_type=control_type,
        status=status,
        owner_id=owner_id,
        frequency=frequency,
    )
    return await service.list_controls(filters=filters, page=page, page_size=page_size)


@router.post("/controls", response_model=ControlRead, status_code=status.HTTP_201_CREATED)
async def create_control(
    payload: ControlCreate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ControlRead:
    return await service.create_control(payload)


@router.get("/controls/{control_id}", response_model=ControlRead)
async def get_control(
    control_id: uuid.UUID,
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ControlRead:
    return await service.get_control(control_id)


@router.patch("/controls/{control_id}", response_model=ControlRead)
async def update_control(
    control_id: uuid.UUID,
    payload: ControlUpdate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ControlRead:
    return await service.update_control(control_id, payload)


@router.delete("/controls/{control_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_control(
    control_id: uuid.UUID,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> None:
    await service.delete_control(control_id)


@router.get("/entity/{subject_type}/{subject_id}", response_model=EntityComplianceResponse)
async def get_entity_compliance(
    subject_type: ComplianceSubjectType,
    subject_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> EntityComplianceResponse:
    return await service.get_entity_compliance(
        subject_type,
        subject_id,
        page=page,
        page_size=page_size,
    )


@router.get("/checks", response_model=ComplianceCheckListResponse)
async def list_checks(
    _user: ViewerUser,
    search: str | None = None,
    subject_type: ComplianceSubjectType | None = None,
    subject_id: uuid.UUID | None = None,
    status: ComplianceStatus | None = None,
    check_type: ComplianceCheckType | None = None,
    rule_id: uuid.UUID | None = None,
    control_id: uuid.UUID | None = None,
    owner_id: uuid.UUID | None = None,
    due_before: date | None = None,
    due_after: date | None = None,
    overdue: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceCheckListResponse:
    filters = ComplianceCheckFilters(
        search=search,
        subject_type=subject_type,
        subject_id=subject_id,
        status=status,
        check_type=check_type,
        rule_id=rule_id,
        control_id=control_id,
        owner_id=owner_id,
        due_before=due_before,
        due_after=due_after,
        overdue=overdue,
    )
    return await service.list_checks(filters=filters, page=page, page_size=page_size)


@router.post("/checks", response_model=ComplianceCheckRead, status_code=status.HTTP_201_CREATED)
async def create_check(
    payload: ComplianceCheckCreate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceCheckRead:
    return await service.create_check(payload)


@router.get("/checks/{check_id}", response_model=ComplianceCheckRead)
async def get_check(
    check_id: uuid.UUID,
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceCheckRead:
    return await service.get_check(check_id)


@router.patch("/checks/{check_id}", response_model=ComplianceCheckRead)
async def update_check(
    check_id: uuid.UUID,
    payload: ComplianceCheckUpdate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceCheckRead:
    return await service.update_check(check_id, payload)


@router.delete("/checks/{check_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_check(
    check_id: uuid.UUID,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> None:
    await service.delete_check(check_id)


@router.get("/checks/{check_id}/evidence", response_model=list[ComplianceEvidenceRead])
async def list_check_evidence(
    check_id: uuid.UUID,
    _user: ViewerUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> list[ComplianceEvidenceRead]:
    return await service.list_check_evidence(check_id)


@router.post(
    "/checks/{check_id}/evidence",
    response_model=ComplianceEvidenceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_check_evidence(
    check_id: uuid.UUID,
    payload: ComplianceEvidenceCreate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceEvidenceRead:
    return await service.add_evidence(check_id, payload)


@router.patch("/evidence/{evidence_id}", response_model=ComplianceEvidenceRead)
async def update_evidence(
    evidence_id: uuid.UUID,
    payload: ComplianceEvidenceUpdate,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> ComplianceEvidenceRead:
    return await service.update_evidence(evidence_id, payload)


@router.delete("/evidence/{evidence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_evidence(
    evidence_id: uuid.UUID,
    _user: EditorUser,
    service: ComplianceService = Depends(get_compliance_service),
) -> None:
    await service.delete_evidence(evidence_id)
