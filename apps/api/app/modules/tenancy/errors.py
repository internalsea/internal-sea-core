"""Tenancy module errors."""

import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class CompanyNotFoundError(NotFoundError):
    def __init__(self, company_id: uuid.UUID | None = None) -> None:
        message = f"Company {company_id} not found" if company_id else "Company not found"
        super().__init__(message)


class WorkspaceNotFoundError(NotFoundError):
    def __init__(self, workspace_id: uuid.UUID | None = None) -> None:
        message = f"Workspace {workspace_id} not found" if workspace_id else "Workspace not found"
        super().__init__(message)


class CompanyMemberNotFoundError(NotFoundError):
    def __init__(self, member_id: uuid.UUID | None = None) -> None:
        message = f"Company member {member_id} not found" if member_id else "Company member not found"
        super().__init__(message)


class CompanyConflictError(ConflictError):
    pass


class OnboardingNotAllowedError(ValidationError):
    def __init__(self) -> None:
        super().__init__("First-user onboarding is only allowed when no users or companies exist")


class TenantSelectionRequiredError(ValidationError):
    def __init__(self) -> None:
        super().__init__("Company selection required — provide X-Company-ID header or join a company")


class TenantAccessDeniedError(ValidationError):
    def __init__(self) -> None:
        super().__init__("You do not have access to this company")


class InsufficientCompanyRoleError(ValidationError):
    def __init__(self) -> None:
        super().__init__("Insufficient company role for this operation")
