import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import EntityType, ProjectType
from app.modules.relationships.errors import EntityNotFoundError, UnsupportedEntityTypeError
from app.modules.relationships.validators import (
    SUPPORTED_ENTITY_TYPES,
    is_supported_entity_type,
    validate_entity_exists,
)


def test_supported_entity_types_contains_core_types() -> None:
    assert EntityType.DATA_PRODUCT in SUPPORTED_ENTITY_TYPES
    assert EntityType.WORK_ITEM in SUPPORTED_ENTITY_TYPES
    assert EntityType.POLICY not in SUPPORTED_ENTITY_TYPES


def test_is_supported_entity_type() -> None:
    assert is_supported_entity_type(EntityType.TEAM) is True
    assert is_supported_entity_type(EntityType.POLICY) is False


@pytest.mark.asyncio
async def test_validate_entity_exists_rejects_unsupported_type() -> None:
    session = AsyncMock()
    with pytest.raises(UnsupportedEntityTypeError):
        await validate_entity_exists(session, EntityType.POLICY, uuid.uuid4())


@pytest.mark.asyncio
async def test_validate_entity_exists_raises_when_data_product_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    missing_id = uuid.uuid4()
    with pytest.raises(EntityNotFoundError):
        await validate_entity_exists(session, EntityType.DATA_PRODUCT, missing_id)


@pytest.mark.asyncio
async def test_validate_entity_exists_rejects_client_project_as_internal() -> None:
    session = AsyncMock()
    project = MagicMock()
    project.project_type = ProjectType.CLIENT_PROJECT
    session.get = AsyncMock(return_value=project)
    with pytest.raises(EntityNotFoundError):
        await validate_entity_exists(session, EntityType.INTERNAL_PROJECT, uuid.uuid4())
