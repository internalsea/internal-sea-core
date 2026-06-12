import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class PolicyNotFoundError(NotFoundError):
    def __init__(self, policy_id: uuid.UUID) -> None:
        super().__init__(f"Policy not found: {policy_id}")


class ComplianceRuleNotFoundError(NotFoundError):
    def __init__(self, rule_id: uuid.UUID) -> None:
        super().__init__(f"Compliance rule not found: {rule_id}")


class ControlNotFoundError(NotFoundError):
    def __init__(self, control_id: uuid.UUID) -> None:
        super().__init__(f"Control not found: {control_id}")


class ComplianceCheckNotFoundError(NotFoundError):
    def __init__(self, check_id: uuid.UUID) -> None:
        super().__init__(f"Compliance check not found: {check_id}")


class ComplianceEvidenceNotFoundError(NotFoundError):
    def __init__(self, evidence_id: uuid.UUID) -> None:
        super().__init__(f"Compliance evidence not found: {evidence_id}")


class ComplianceConflictError(ConflictError):
    def __init__(self, message: str = "Compliance operation conflict") -> None:
        super().__init__(message)


class UnsupportedComplianceSubjectTypeError(ValidationError):
    def __init__(self, subject_type: str) -> None:
        super().__init__(f"Unsupported compliance subject type: {subject_type}")


class ComplianceSubjectNotFoundError(NotFoundError):
    def __init__(self, subject_type: str, subject_id: uuid.UUID) -> None:
        super().__init__(f"{subject_type} not found: {subject_id}")


class ComplianceEvidenceConflictError(ConflictError):
    def __init__(self, message: str = "Evidence already linked to this check") -> None:
        super().__init__(message)
