import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import get_model
from app.domain.enums import DataProductStatus, DataProductType, QualityStatus
from app.models.catalog import DataProduct


@dataclass
class DataProductListFilters:
    search: str | None = None
    status: DataProductStatus | None = None
    type: DataProductType | None = None
    quality_status: QualityStatus | None = None
    business_domain_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    business_owner_id: uuid.UUID | None = None
    technical_owner_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None


class DataProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query: Any, filters: DataProductListFilters) -> Any:
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    DataProduct.name.ilike(pattern),
                    DataProduct.description.ilike(pattern),
                )
            )
        if filters.status is not None:
            query = query.where(DataProduct.status == filters.status)
        if filters.type is not None:
            query = query.where(DataProduct.type == filters.type)
        if filters.quality_status is not None:
            query = query.where(DataProduct.quality_status == filters.quality_status)
        if filters.business_domain_id is not None:
            query = query.where(DataProduct.business_domain_id == filters.business_domain_id)
        if filters.capability_id is not None:
            query = query.where(DataProduct.capability_id == filters.capability_id)
        if filters.team_id is not None:
            query = query.where(DataProduct.team_id == filters.team_id)
        if filters.business_owner_id is not None:
            query = query.where(DataProduct.business_owner_id == filters.business_owner_id)
        if filters.technical_owner_id is not None:
            query = query.where(DataProduct.technical_owner_id == filters.technical_owner_id)
        if filters.company_id is not None:
            query = query.where(DataProduct.company_id == filters.company_id)
        return query

    async def list_paginated(
        self,
        *,
        filters: DataProductListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[DataProduct], int]:
        base_query = select(DataProduct)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(DataProduct.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(DataProduct.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_by_id(self, data_product_id: uuid.UUID) -> DataProduct | None:
        return await get_model(self._session, DataProduct, data_product_id)

    async def create(self, data: dict[str, object]) -> DataProduct:
        data_product = DataProduct(**data)
        self._session.add(data_product)
        await self._session.commit()
        await self._session.refresh(data_product)
        return data_product

    async def update(
        self,
        data_product: DataProduct,
        data: dict[str, object],
    ) -> DataProduct:
        for field, value in data.items():
            setattr(data_product, field, value)
        await self._session.commit()
        await self._session.refresh(data_product)
        return data_product

    async def delete(self, data_product: DataProduct) -> None:
        await self._session.delete(data_product)
        await self._session.commit()
