"""Tenancy API routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import CompanyMemberRole
from app.models.identity import User
from app.modules.auth.dependencies import require_active_user
from app.modules.tenancy.dependencies import (
    CurrentTenant,
    get_current_tenant,
    require_company_role,
)
from app.modules.tenancy.repository import TenancyRepository
from app.modules.tenancy.schemas import (
    CompanyCreate,
    CompanyListResponse,
    CompanyMemberCreate,
    CompanyMemberListResponse,
    CompanyMemberRead,
    CompanyMemberUpdate,
    CompanyRead,
    CompanyUpdate,
    CurrentTenantContext,
    FirstUserOnboardingRequest,
    FirstUserOnboardingResponse,
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceRead,
    WorkspaceUpdate,
)
from app.modules.tenancy.service import TenancyService

router = APIRouter(prefix="/tenancy", tags=["Tenancy"])


def get_tenancy_service(db: AsyncSession = Depends(get_db)) -> TenancyService:
    return TenancyService(TenancyRepository(db), db)


@router.post(
    "/onboarding/first-user",
    response_model=FirstUserOnboardingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def first_user_onboarding(
    payload: FirstUserOnboardingRequest,
    service: TenancyService = Depends(get_tenancy_service),
) -> FirstUserOnboardingResponse:
    return await service.first_user_onboarding(payload)


@router.get("/current", response_model=CurrentTenantContext)
async def get_current_context(
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TenancyService = Depends(get_tenancy_service),
) -> CurrentTenantContext:
    return await service.get_current_tenant_context(
        user=tenant.user,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/companies", response_model=CompanyListResponse)
async def list_companies(
    user: User = Depends(require_active_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyListResponse:
    return await service.list_companies_for_current_user(page=page, page_size=page_size, user=user)


@router.post("/companies", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    payload: CompanyCreate,
    user: User = Depends(require_active_user),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyRead:
    return await service.create_company(payload, owner_user=user)


@router.get("/companies/{company_id}", response_model=CompanyRead)
async def get_company(
    company_id: uuid.UUID,
    user: User = Depends(require_active_user),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyRead:
    return await service.get_company(company_id, user=user)


@router.patch("/companies/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: uuid.UUID,
    payload: CompanyUpdate,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyRead:
    return await service.update_company(company_id, payload)


@router.get("/companies/{company_id}/workspaces", response_model=WorkspaceListResponse)
async def list_workspaces(
    company_id: uuid.UUID,
    user: User = Depends(require_active_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: TenancyService = Depends(get_tenancy_service),
) -> WorkspaceListResponse:
    await service.get_company(company_id, user=user)
    return await service.list_workspaces(company_id, page=page, page_size=page_size)


@router.post(
    "/companies/{company_id}/workspaces",
    response_model=WorkspaceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    company_id: uuid.UUID,
    payload: WorkspaceCreate,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> WorkspaceRead:
    payload = payload.model_copy(update={"company_id": company_id})
    return await service.create_workspace(payload)


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceRead)
async def get_workspace(
    workspace_id: uuid.UUID,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TenancyService = Depends(get_tenancy_service),
) -> WorkspaceRead:
    context = await service.get_current_tenant_context(
        user=tenant.user,
        company_id=tenant.company_id,
        workspace_id=workspace_id,
    )
    return context.workspace


@router.patch("/workspaces/{workspace_id}", response_model=WorkspaceRead)
async def update_workspace(
    workspace_id: uuid.UUID,
    payload: WorkspaceUpdate,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> WorkspaceRead:
    return await service.update_workspace(workspace_id, payload)


@router.get("/companies/{company_id}/members", response_model=CompanyMemberListResponse)
async def list_members(
    company_id: uuid.UUID,
    user: User = Depends(require_active_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyMemberListResponse:
    await service.get_company(company_id, user=user)
    return await service.list_members(company_id, page=page, page_size=page_size)


@router.post(
    "/companies/{company_id}/members",
    response_model=CompanyMemberRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_member(
    company_id: uuid.UUID,
    payload: CompanyMemberCreate,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyMemberRead:
    payload = payload.model_copy(update={"company_id": company_id})
    return await service.add_member(payload)


@router.patch("/members/{member_id}", response_model=CompanyMemberRead)
async def update_member(
    member_id: uuid.UUID,
    payload: CompanyMemberUpdate,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> CompanyMemberRead:
    return await service.update_member(member_id, payload)


@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    member_id: uuid.UUID,
    _tenant: CurrentTenant = Depends(require_company_role(CompanyMemberRole.ADMIN, CompanyMemberRole.OWNER)),
    service: TenancyService = Depends(get_tenancy_service),
) -> None:
    await service.remove_member(member_id)
