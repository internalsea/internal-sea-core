import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import EntityLinkType, EntityType
from app.modules.relationships.errors import EntityLinkConflictError
from app.modules.relationships.schemas import EntityLinkCreate
from app.modules.relationships.service import RelationshipService


@pytest.mark.asyncio
async def test_create_link_raises_conflict_for_duplicate() -> None:
    repository = AsyncMock()
    activity_service = AsyncMock()
    session = AsyncMock()
    session.get = AsyncMock(return_value=MagicMock())

    source_id = uuid.uuid4()
    target_id = uuid.uuid4()
    duplicate = MagicMock()
    repository.get_duplicate.return_value = duplicate

    service = RelationshipService(repository, activity_service, session)
    payload = EntityLinkCreate(
        source_type=EntityType.DATA_PRODUCT,
        source_id=source_id,
        target_type=EntityType.WORK_ITEM,
        target_id=target_id,
        link_type=EntityLinkType.IMPROVES,
    )

    with pytest.raises(EntityLinkConflictError):
        await service.create_link(payload)

    repository.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_link_records_activity_on_success() -> None:
    repository = AsyncMock()
    activity_service = AsyncMock()
    session = AsyncMock()
    session.get = AsyncMock(return_value=MagicMock())

    source_id = uuid.uuid4()
    target_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    link = MagicMock()
    link.id = uuid.uuid4()
    link.source_type = EntityType.DATA_PRODUCT.value
    link.source_id = source_id
    link.target_type = EntityType.WORK_ITEM.value
    link.target_id = target_id
    link.link_type = EntityLinkType.IMPROVES.value
    link.title = None
    link.description = None
    link.created_by_id = None
    link.created_at = now
    link.updated_at = now
    repository.get_duplicate.return_value = None
    repository.create.return_value = link

    service = RelationshipService(repository, activity_service, session)
    payload = EntityLinkCreate(
        source_type=EntityType.DATA_PRODUCT,
        source_id=source_id,
        target_type=EntityType.WORK_ITEM,
        target_id=target_id,
        link_type=EntityLinkType.IMPROVES,
    )

    result = await service.create_link(payload)

    repository.create.assert_awaited_once()
    assert activity_service.record_event.await_count == 2
    assert result.source_type == EntityType.DATA_PRODUCT
