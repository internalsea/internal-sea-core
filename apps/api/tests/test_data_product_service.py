import uuid
from unittest.mock import AsyncMock

import pytest
from app.modules.data_products.errors import DataProductNotFoundError
from app.modules.data_products.repository import DataProductListFilters
from app.modules.data_products.service import DataProductService


@pytest.mark.asyncio
async def test_service_not_found_handling() -> None:
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    service = DataProductService(repository, AsyncMock())
    missing_id = uuid.uuid4()

    with pytest.raises(DataProductNotFoundError):
        await service.get_data_product(missing_id)


@pytest.mark.asyncio
async def test_service_pagination_calculation() -> None:
    repository = AsyncMock()
    repository.list.return_value = ([], 45)
    service = DataProductService(repository, AsyncMock())

    result = await service.list_data_products(
        filters=DataProductListFilters(),
        page=2,
        page_size=20,
    )

    assert result.page == 2
    assert result.page_size == 20
    assert result.total == 45
    assert result.pages == 3
    repository.list.assert_awaited_once_with(filters=DataProductListFilters(), offset=20, limit=20)
