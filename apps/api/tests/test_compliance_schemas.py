import uuid
from datetime import date

import pytest
from pydantic import ValidationError

from app.domain.enums import ComplianceSubjectType, EvidenceStatus, RuleSeverity
from app.modules.compliance.schemas import (
    ComplianceCheckCreate,
    ComplianceEvidenceCreate,
    ComplianceRuleCreate,
    ControlCreate,
    PolicyCreate,
    PolicyUpdate,
)


def test_policy_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        PolicyCreate(name="")


def test_policy_date_validation() -> None:
    with pytest.raises(ValidationError):
        PolicyUpdate(effective_from=date(2026, 6, 1), effective_to=date(2026, 5, 1))


def test_compliance_rule_create_accepts_valid_payload() -> None:
    payload = ComplianceRuleCreate(
        policy_id=uuid.uuid4(),
        code="DPG-001",
        name="Active data products must have business owner",
        severity=RuleSeverity.HIGH,
        subject_type=ComplianceSubjectType.DATA_PRODUCT,
    )
    assert payload.severity == RuleSeverity.HIGH


def test_control_create_accepts_valid_payload() -> None:
    payload = ControlCreate(
        rule_id=uuid.uuid4(),
        name="Ownership Review Control",
    )
    assert payload.name == "Ownership Review Control"


def test_compliance_check_create_accepts_valid_subject() -> None:
    payload = ComplianceCheckCreate(
        subject_type=ComplianceSubjectType.DATA_PRODUCT,
        subject_id=uuid.uuid4(),
        title="Business owner assigned",
    )
    assert payload.title == "Business owner assigned"


def test_evidence_create_accepts_valid_file_id() -> None:
    payload = ComplianceEvidenceCreate(
        file_id=uuid.uuid4(),
        status=EvidenceStatus.SUBMITTED,
        description="Approval document",
    )
    assert payload.status == EvidenceStatus.SUBMITTED
