import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.enums import ProjectType
from app.modules.projects.errors import ProjectNotFoundError
from app.modules.projects.repository import ProjectListFilters
from app.modules.projects.service import ProjectService


@pytest.mark.asyncio
async def test_service_not_found_handling() -> None:
    repository = AsyncMock()
    repository.get_by_id.return_value = None
    service = ProjectService(repository, AsyncMock())
    missing_id = uuid.uuid4()

    with pytest.raises(ProjectNotFoundError):
        await service.get_project(missing_id)


@pytest.mark.asyncio
async def test_service_pagination_calculation() -> None:
    repository = AsyncMock()
    repository.list.return_value = ([], 45)
    service = ProjectService(repository, AsyncMock())

    result = await service.list_projects(
        filters=ProjectListFilters(),
        page=2,
        page_size=20,
    )

    assert result.page == 2
    assert result.page_size == 20
    assert result.total == 45
    assert result.pages == 3
    repository.list.assert_awaited_once_with(filters=ProjectListFilters(), offset=20, limit=20)


@pytest.mark.asyncio
async def test_internal_project_not_found_for_client_type() -> None:
    repository = AsyncMock()
    project = AsyncMock()
    project.project_type = ProjectType.CLIENT_PROJECT
    repository.get_by_id.return_value = project
    service = ProjectService(repository, AsyncMock())

    with pytest.raises(ProjectNotFoundError):
        await service.get_internal_project(uuid.uuid4())
