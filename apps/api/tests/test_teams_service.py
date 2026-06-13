import uuid
from unittest.mock import AsyncMock

import pytest
from app.modules.teams.errors import TeamNotFoundError
from app.modules.teams.repository import TeamListFilters
from app.modules.teams.service import TeamService


@pytest.mark.asyncio
async def test_service_not_found_handling() -> None:
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    service = TeamService(repository)
    missing_id = uuid.uuid4()

    with pytest.raises(TeamNotFoundError):
        await service.get_team(missing_id)


@pytest.mark.asyncio
async def test_service_pagination_calculation() -> None:
    repository = AsyncMock()
    repository.list.return_value = ([], 25)
    service = TeamService(repository)

    result = await service.list_teams(
        filters=TeamListFilters(),
        page=1,
        page_size=20,
    )

    assert result.total == 25
    assert result.pages == 2
