import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import DataProductStatus, DataProductType, QualityStatus
from app.modules.activity.dependencies import build_activity_service
from app.modules.data_products.repository import DataProductListFilters, DataProductRepository
from app.modules.data_products.schemas import (
    DataProductCreate,
    DataProductRead,
    DataProductUpdate,
    PaginatedDataProductList,
)
from app.modules.data_products.service import DataProductService
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant

router = APIRouter(prefix="/data-products", tags=["Catalog"])


def get_data_product_service(db: AsyncSession = Depends(get_db)) -> DataProductService:
    return DataProductService(DataProductRepository(db), build_activity_service(db))


@router.get("", response_model=PaginatedDataProductList)
async def list_data_products(
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    status: DataProductStatus | None = None,
    type: DataProductType | None = None,
    quality_status: QualityStatus | None = None,
    business_domain_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    team_id: uuid.UUID | None = None,
    business_owner_id: uuid.UUID | None = None,
    technical_owner_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: DataProductService = Depends(get_data_product_service),
) -> PaginatedDataProductList:
    filters = DataProductListFilters(
        search=search,
        status=status,
        type=type,
        quality_status=quality_status,
        business_domain_id=business_domain_id,
        capability_id=capability_id,
        team_id=team_id,
        business_owner_id=business_owner_id,
        technical_owner_id=technical_owner_id,
        company_id=tenant.company_id,
    )
    return await service.list_data_products(
        filters=filters,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=DataProductRead, status_code=status.HTTP_201_CREATED)
async def create_data_product(
    payload: DataProductCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: DataProductService = Depends(get_data_product_service),
) -> DataProductRead:
    return await service.create_data_product(
        payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{data_product_id}", response_model=DataProductRead)
async def get_data_product(
    data_product_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: DataProductService = Depends(get_data_product_service),
) -> DataProductRead:
    return await service.get_data_product(data_product_id, company_id=tenant.company_id)


@router.patch("/{data_product_id}", response_model=DataProductRead)
async def update_data_product(
    data_product_id: uuid.UUID,
    payload: DataProductUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: DataProductService = Depends(get_data_product_service),
) -> DataProductRead:
    return await service.update_data_product(
        data_product_id,
        payload,
        company_id=tenant.company_id,
    )


@router.delete("/{data_product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_product(
    data_product_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: DataProductService = Depends(get_data_product_service),
) -> None:
    await service.delete_data_product(data_product_id, company_id=tenant.company_id)
