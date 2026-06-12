import uuid
from unittest.mock import AsyncMock

import pytest

from app.modules.people.errors import PersonNotFoundError
from app.modules.people.repository import PersonListFilters
from app.modules.people.service import PersonService


@pytest.mark.asyncio
async def test_service_not_found_handling() -> None:
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    service = PersonService(repository)
    missing_id = uuid.uuid4()

    with pytest.raises(PersonNotFoundError):
        await service.get_person(missing_id)


@pytest.mark.asyncio
async def test_service_pagination_calculation() -> None:
    repository = AsyncMock()
    repository.list.return_value = ([], 45)
    service = PersonService(repository)

    result = await service.list_people(
        filters=PersonListFilters(),
        page=2,
        page_size=20,
    )

    assert result.page == 2
    assert result.page_size == 20
    assert result.total == 45
    assert result.pages == 3
    repository.list.assert_awaited_once_with(filters=PersonListFilters(), offset=20, limit=20)


@pytest.mark.asyncio
async def test_deactivate_person() -> None:
    repository = AsyncMock()
    person = AsyncMock()
    repository.get_by_id.return_value = person
    service = PersonService(repository)
    person_id = uuid.uuid4()

    await service.deactivate_person(person_id)

    repository.deactivate.assert_awaited_once_with(person)
