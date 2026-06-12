import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import (
    ComplianceCheckType,
    ComplianceFrequency,
    ComplianceStatus,
    ComplianceSubjectType,
    ControlStatus,
    ControlType,
    EvidenceStatus,
    PolicyStatus,
    RuleSeverity,
)


class PolicyBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: PolicyStatus = PolicyStatus.DRAFT
    owner_id: uuid.UUID | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    version: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self) -> "PolicyBase":
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError("effective_to must not be before effective_from")
        return self


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: PolicyStatus | None = None
    owner_id: uuid.UUID | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    version: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self) -> "PolicyUpdate":
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError("effective_to must not be before effective_from")
        return self


class PolicyRead(PolicyBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PolicyListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    status: PolicyStatus
    owner_id: uuid.UUID | None
    effective_from: date | None
    effective_to: date | None
    version: str | None
    updated_at: datetime


class PolicyListResponse(BaseModel):
    items: list[PolicyListItem]
    total: int
    page: int
    page_size: int
    pages: int


class PolicyFilters(BaseModel):
    search: str | None = None
    status: PolicyStatus | None = None
    owner_id: uuid.UUID | None = None


class ComplianceRuleBase(BaseModel):
    policy_id: uuid.UUID
    code: str | None = Field(default=None, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    severity: RuleSeverity = RuleSeverity.MEDIUM
    subject_type: ComplianceSubjectType | None = None
    is_active: bool = True


class ComplianceRuleCreate(ComplianceRuleBase):
    pass


class ComplianceRuleUpdate(BaseModel):
    code: str | None = Field(default=None, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    severity: RuleSeverity | None = None
    subject_type: ComplianceSubjectType | None = None
    is_active: bool | None = None


class ComplianceRuleRead(ComplianceRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class RuleFilters(BaseModel):
    search: str | None = None
    policy_id: uuid.UUID | None = None
    severity: RuleSeverity | None = None
    subject_type: ComplianceSubjectType | None = None
    is_active: bool | None = None


class RuleListResponse(BaseModel):
    items: list[ComplianceRuleRead]
    total: int
    page: int
    page_size: int
    pages: int


class ControlBase(BaseModel):
    rule_id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    control_type: ControlType = ControlType.MANUAL
    status: ControlStatus = ControlStatus.ACTIVE
    owner_id: uuid.UUID | None = None
    frequency: ComplianceFrequency | None = None


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    control_type: ControlType | None = None
    status: ControlStatus | None = None
    owner_id: uuid.UUID | None = None
    frequency: ComplianceFrequency | None = None


class ControlRead(ControlBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ControlFilters(BaseModel):
    search: str | None = None
    rule_id: uuid.UUID | None = None
    control_type: ControlType | None = None
    status: ControlStatus | None = None
    owner_id: uuid.UUID | None = None
    frequency: ComplianceFrequency | None = None


class ControlListResponse(BaseModel):
    items: list[ControlRead]
    total: int
    page: int
    page_size: int
    pages: int


class ComplianceCheckBase(BaseModel):
    rule_id: uuid.UUID | None = None
    control_id: uuid.UUID | None = None
    subject_type: ComplianceSubjectType
    subject_id: uuid.UUID
    check_type: ComplianceCheckType = ComplianceCheckType.MANUAL
    status: ComplianceStatus = ComplianceStatus.NOT_STARTED
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    result_summary: str | None = None
    owner_id: uuid.UUID | None = None
    due_date: date | None = None
    completed_at: datetime | None = None
    next_check_at: datetime | None = None


class ComplianceCheckCreate(ComplianceCheckBase):
    pass


class ComplianceCheckUpdate(BaseModel):
    rule_id: uuid.UUID | None = None
    control_id: uuid.UUID | None = None
    subject_type: ComplianceSubjectType | None = None
    subject_id: uuid.UUID | None = None
    check_type: ComplianceCheckType | None = None
    status: ComplianceStatus | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    result_summary: str | None = None
    owner_id: uuid.UUID | None = None
    due_date: date | None = None
    completed_at: datetime | None = None
    next_check_at: datetime | None = None


class ComplianceCheckRead(ComplianceCheckBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ComplianceCheckListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subject_type: ComplianceSubjectType
    subject_id: uuid.UUID
    title: str
    status: ComplianceStatus
    check_type: ComplianceCheckType
    owner_id: uuid.UUID | None
    due_date: date | None
    completed_at: datetime | None
    next_check_at: datetime | None
    rule_id: uuid.UUID | None
    control_id: uuid.UUID | None
    updated_at: datetime


class ComplianceCheckListResponse(BaseModel):
    items: list[ComplianceCheckListItem]
    total: int
    page: int
    page_size: int
    pages: int


class ComplianceCheckFilters(BaseModel):
    search: str | None = None
    subject_type: ComplianceSubjectType | None = None
    subject_id: uuid.UUID | None = None
    status: ComplianceStatus | None = None
    check_type: ComplianceCheckType | None = None
    rule_id: uuid.UUID | None = None
    control_id: uuid.UUID | None = None
    owner_id: uuid.UUID | None = None
    due_before: date | None = None
    due_after: date | None = None
    overdue: bool | None = None


class ComplianceEvidenceCreate(BaseModel):
    file_id: uuid.UUID
    status: EvidenceStatus = EvidenceStatus.SUBMITTED
    description: str | None = None
    submitted_by_id: uuid.UUID | None = None


class ComplianceEvidenceUpdate(BaseModel):
    status: EvidenceStatus | None = None
    description: str | None = None
    reviewed_by_id: uuid.UUID | None = None
    reviewed_at: datetime | None = None


class ComplianceEvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    compliance_check_id: uuid.UUID
    file_id: uuid.UUID
    status: EvidenceStatus
    description: str | None
    submitted_by_id: uuid.UUID | None
    reviewed_by_id: uuid.UUID | None
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EntityComplianceResponse(BaseModel):
    subject_type: ComplianceSubjectType
    subject_id: uuid.UUID
    checks: list[ComplianceCheckListItem]
    total: int
    compliant_count: int
    non_compliant_count: int
    open_count: int
    overdue_count: int


class ComplianceOverview(BaseModel):
    policies_total: int = 0
    policies_active: int = 0
    rules_total: int = 0
    active_rules: int = 0
    controls_total: int = 0
    active_controls: int = 0
    checks_total: int = 0
    checks_open: int = 0
    checks_compliant: int = 0
    checks_non_compliant: int = 0
    checks_overdue: int = 0
    evidence_missing: int = 0
