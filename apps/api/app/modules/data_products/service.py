import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType
from app.modules.activity.helpers import get_updated_fields
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.data_products.errors import DataProductNotFoundError
from app.modules.data_products.repository import DataProductListFilters, DataProductRepository
from app.modules.data_products.schemas import (
    DataProductCreate,
    DataProductRead,
    DataProductUpdate,
    PaginatedDataProductList,
)
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields


class DataProductService:
    def __init__(
        self,
        repository: DataProductRepository,
        activity_service: ActivityService,
    ) -> None:
        self._repository = repository
        self._activity = activity_service

    async def list_data_products(
        self,
        *,
        filters: DataProductListFilters,
        page: int,
        page_size: int,
    ) -> PaginatedDataProductList:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return PaginatedDataProductList(
            items=[DataProductRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_data_product(
        self, data_product_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> DataProductRead:
        data_product = await self._repository.get_by_id(data_product_id)
        if data_product is None:
            raise DataProductNotFoundError(data_product_id)
        if company_id is not None:
            ensure_company_access(data_product, company_id, label="Data product")
        return DataProductRead.model_validate(data_product)

    async def create_data_product(
        self,
        payload: DataProductCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> DataProductRead:
        data = merge_tenant_fields(
            payload.model_dump(), company_id=company_id, workspace_id=workspace_id
        )
        data_product = await self._repository.create(data)
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=ActivityEntityType.DATA_PRODUCT,
                entity_id=data_product.id,
                action=ActivityAction.CREATED,
                title="Data product created",
            )
        )
        return DataProductRead.model_validate(data_product)

    async def update_data_product(
        self,
        data_product_id: uuid.UUID,
        payload: DataProductUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> DataProductRead:
        data_product = await self._repository.get_by_id(data_product_id)
        if data_product is None:
            raise DataProductNotFoundError(data_product_id)
        if company_id is not None:
            ensure_company_access(data_product, company_id, label="Data product")
        update_data = payload.model_dump(exclude_unset=True)
        updated = await self._repository.update(data_product, update_data)
        if update_data:
            await self._activity.record_event(
                ActivityEventCreateInternal(
                    entity_type=ActivityEntityType.DATA_PRODUCT,
                    entity_id=data_product_id,
                    action=ActivityAction.UPDATED,
                    title="Data product updated",
                    details={"updated_fields": get_updated_fields(update_data)},
                )
            )
        return DataProductRead.model_validate(updated)

    async def delete_data_product(
        self, data_product_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> None:
        data_product = await self._repository.get_by_id(data_product_id)
        if data_product is None:
            raise DataProductNotFoundError(data_product_id)
        if company_id is not None:
            ensure_company_access(data_product, company_id, label="Data product")
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=ActivityEntityType.DATA_PRODUCT,
                entity_id=data_product_id,
                action=ActivityAction.DELETED,
                title="Data product deleted",
            )
        )
        await self._repository.delete(data_product)
