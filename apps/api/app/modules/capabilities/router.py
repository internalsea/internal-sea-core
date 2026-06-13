import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.modules.capabilities.repository import CapabilityListFilters, CapabilityRepository
from app.modules.capabilities.schemas import (
    CapabilityCreate,
    CapabilityListResponse,
    CapabilityRead,
    CapabilitySummary,
    CapabilityUpdate,
)
from app.modules.capabilities.service import CapabilityService
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant

router = APIRouter(prefix="/capabilities", tags=["Capabilities"])


def get_capability_service(db: AsyncSession = Depends(get_db)) -> CapabilityService:
    return CapabilityService(CapabilityRepository(db))


@router.get("", response_model=CapabilityListResponse)
async def list_capabilities(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: CapabilityService = Depends(get_capability_service),
) -> CapabilityListResponse:
    filters = CapabilityListFilters(search=search, company_id=tenant.company_id)
    return await service.list_capabilities(filters=filters, page=page, page_size=page_size)


@router.post("", response_model=CapabilityRead, status_code=status.HTTP_201_CREATED)
async def create_capability(
    payload: CapabilityCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: CapabilityService = Depends(get_capability_service),
) -> CapabilityRead:
    return await service.create_capability(
        payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{capability_id}", response_model=CapabilityRead)
async def get_capability(
    capability_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: CapabilityService = Depends(get_capability_service),
) -> CapabilityRead:
    return await service.get_capability(capability_id, company_id=tenant.company_id)


@router.get("/{capability_id}/summary", response_model=CapabilitySummary)
async def get_capability_summary(
    capability_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: CapabilityService = Depends(get_capability_service),
) -> CapabilitySummary:
    return await service.get_capability_summary(capability_id, company_id=tenant.company_id)


@router.patch("/{capability_id}", response_model=CapabilityRead)
async def update_capability(
    capability_id: uuid.UUID,
    payload: CapabilityUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: CapabilityService = Depends(get_capability_service),
) -> CapabilityRead:
    return await service.update_capability(capability_id, payload, company_id=tenant.company_id)


@router.delete("/{capability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_capability(
    capability_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: CapabilityService = Depends(get_capability_service),
) -> None:
    await service.delete_capability(capability_id, company_id=tenant.company_id)
