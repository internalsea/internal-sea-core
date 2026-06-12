import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import FileEntityType, ProjectType
from app.modules.files.errors import FileEntityNotFoundError, UnsupportedFileEntityTypeError
from app.modules.files.validators import (
    SUPPORTED_FILE_ENTITY_TYPES,
    is_supported_file_entity_type,
    validate_file_attachment_entity_exists,
)


def test_supported_file_entity_types_contains_active_types() -> None:
    assert FileEntityType.DATA_PRODUCT in SUPPORTED_FILE_ENTITY_TYPES
    assert FileEntityType.WORK_ITEM in SUPPORTED_FILE_ENTITY_TYPES
    assert FileEntityType.PROJECT in SUPPORTED_FILE_ENTITY_TYPES
    assert FileEntityType.INTERNAL_PROJECT in SUPPORTED_FILE_ENTITY_TYPES
    assert FileEntityType.POLICY not in SUPPORTED_FILE_ENTITY_TYPES


def test_is_supported_file_entity_type() -> None:
    assert is_supported_file_entity_type(FileEntityType.DATA_PRODUCT) is True
    assert is_supported_file_entity_type(FileEntityType.POLICY) is False


@pytest.mark.asyncio
async def test_validate_file_attachment_entity_rejects_unsupported_type() -> None:
    session = AsyncMock()
    with pytest.raises(UnsupportedFileEntityTypeError):
        await validate_file_attachment_entity_exists(
            session,
            FileEntityType.POLICY,
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_validate_file_attachment_entity_raises_when_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with pytest.raises(FileEntityNotFoundError):
        await validate_file_attachment_entity_exists(
            session,
            FileEntityType.DATA_PRODUCT,
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_validate_file_attachment_entity_rejects_client_project_as_internal() -> None:
    session = AsyncMock()
    project = MagicMock()
    project.project_type = ProjectType.CLIENT_PROJECT
    session.get = AsyncMock(return_value=project)
    with pytest.raises(FileEntityNotFoundError):
        await validate_file_attachment_entity_exists(
            session,
            FileEntityType.INTERNAL_PROJECT,
            uuid.uuid4(),
        )
