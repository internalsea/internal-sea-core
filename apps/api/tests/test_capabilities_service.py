import uuid
from unittest.mock import AsyncMock

import pytest
from app.modules.capabilities.errors import CapabilityNotFoundError
from app.modules.capabilities.repository import CapabilityListFilters
from app.modules.capabilities.service import CapabilityService


@pytest.mark.asyncio
async def test_service_not_found_handling() -> None:
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    service = CapabilityService(repository)
    missing_id = uuid.uuid4()

    with pytest.raises(CapabilityNotFoundError):
        await service.get_capability(missing_id)


@pytest.mark.asyncio
async def test_service_pagination_calculation() -> None:
    repository = AsyncMock()
    repository.list.return_value = ([], 10)
    service = CapabilityService(repository)

    result = await service.list_capabilities(
        filters=CapabilityListFilters(),
        page=1,
        page_size=20,
    )

    assert result.total == 10
    assert result.pages == 1
