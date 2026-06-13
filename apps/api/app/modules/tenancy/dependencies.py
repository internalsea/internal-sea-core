"""FastAPI dependencies for SaaS tenant context."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.dependencies import get_db
from app.domain.enums import CompanyMemberRole, CompanyMemberStatus
from app.models.identity import User
from app.models.tenancy import CompanyMember
from app.modules.auth.dependencies import require_active_user
from app.modules.tenancy.errors import TenantSelectionRequiredError
from app.modules.tenancy.repository import TenancyRepository

ROLE_RANK = {
    CompanyMemberRole.VIEWER: 1,
    CompanyMemberRole.EDITOR: 2,
    CompanyMemberRole.ADMIN: 3,
    CompanyMemberRole.OWNER: 4,
}


@dataclass
class CurrentTenant:
    user: User
    company_id: uuid.UUID
    workspace_id: uuid.UUID
    member: CompanyMember
    role: CompanyMemberRole


def _get_tenancy_repository(db: AsyncSession = Depends(get_db)) -> TenancyRepository:
    return TenancyRepository(db)


async def get_current_company_id(
    user: Annotated[User, Depends(require_active_user)],
    repository: Annotated[TenancyRepository, Depends(_get_tenancy_repository)],
    x_company_id: Annotated[str | None, Header(alias="X-Company-ID")] = None,
) -> uuid.UUID:
    settings = get_settings()
    if x_company_id:
        try:
            company_id = uuid.UUID(x_company_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid X-Company-ID header") from exc
        member = await repository.get_member(company_id, user.id)
        if member is None and not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this company",
            )
        return company_id

    memberships = await repository.get_active_memberships(user.id)
    if len(memberships) == 1:
        return memberships[0].company_id

    if user.is_superuser or not settings.auth_enabled:
        company = await repository.get_first_company()
        if company is not None:
            return company.id

    raise TenantSelectionRequiredError()


async def get_current_workspace_id(
    company_id: Annotated[uuid.UUID, Depends(get_current_company_id)],
    repository: Annotated[TenancyRepository, Depends(_get_tenancy_repository)],
    x_workspace_id: Annotated[str | None, Header(alias="X-Workspace-ID")] = None,
) -> uuid.UUID:
    if x_workspace_id:
        try:
            workspace_id = uuid.UUID(x_workspace_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid X-Workspace-ID header") from exc
        workspace = await repository.get_workspace_by_id(workspace_id)
        if workspace is None or workspace.company_id != company_id:
            raise HTTPException(status_code=400, detail="Invalid workspace for company")
        return workspace_id

    workspace = await repository.get_default_workspace_for_company(company_id)
    if workspace is None:
        raise HTTPException(status_code=400, detail="No workspace found for company")
    return workspace.id


async def get_current_member(
    user: Annotated[User, Depends(require_active_user)],
    company_id: Annotated[uuid.UUID, Depends(get_current_company_id)],
    repository: Annotated[TenancyRepository, Depends(_get_tenancy_repository)],
) -> CompanyMember:
    member = await repository.get_member(company_id, user.id)
    if member is None or member.status != CompanyMemberStatus.ACTIVE.value:
        if user.is_superuser:
            return CompanyMember(
                company_id=company_id,
                user_id=user.id,
                role=CompanyMemberRole.ADMIN.value,
                status=CompanyMemberStatus.ACTIVE.value,
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company",
        )
    return member


async def get_current_tenant(
    user: Annotated[User, Depends(require_active_user)],
    company_id: Annotated[uuid.UUID, Depends(get_current_company_id)],
    workspace_id: Annotated[uuid.UUID, Depends(get_current_workspace_id)],
    member: Annotated[CompanyMember, Depends(get_current_member)],
) -> CurrentTenant:
    return CurrentTenant(
        user=user,
        company_id=company_id,
        workspace_id=workspace_id,
        member=member,
        role=CompanyMemberRole(member.role),
    )


def require_company_role(*roles: CompanyMemberRole) -> Callable[..., CurrentTenant]:
    min_rank = min(ROLE_RANK[role] for role in roles)

    async def _dependency(
        tenant: Annotated[CurrentTenant, Depends(get_current_tenant)],
    ) -> CurrentTenant:
        if tenant.user.is_superuser:
            return tenant
        if ROLE_RANK.get(tenant.role, 0) >= min_rank:
            return tenant
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient company role for this operation",
        )

    return _dependency


def company_role_can_write(role: CompanyMemberRole) -> bool:
    return ROLE_RANK.get(role, 0) >= ROLE_RANK[CompanyMemberRole.EDITOR]


def company_role_can_admin(role: CompanyMemberRole) -> bool:
    return ROLE_RANK.get(role, 0) >= ROLE_RANK[CompanyMemberRole.ADMIN]
