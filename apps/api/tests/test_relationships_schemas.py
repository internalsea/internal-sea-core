import uuid

import pytest
from pydantic import ValidationError

from app.domain.enums import EntityLinkType, EntityType
from app.modules.relationships.schemas import (
    EntityLinkCreate,
    EntityLinkFilters,
    EntityRelationshipView,
)


def test_entity_link_create_accepts_valid_payload() -> None:
    source_id = uuid.uuid4()
    target_id = uuid.uuid4()
    payload = EntityLinkCreate(
        source_type=EntityType.DATA_PRODUCT,
        source_id=source_id,
        target_type=EntityType.WORK_ITEM,
        target_id=target_id,
        link_type=EntityLinkType.IMPROVES,
        title="Work item improves data product",
    )
    assert payload.source_type == EntityType.DATA_PRODUCT
    assert payload.link_type == EntityLinkType.IMPROVES


def test_entity_link_create_rejects_self_link() -> None:
    entity_id = uuid.uuid4()
    with pytest.raises(ValidationError):
        EntityLinkCreate(
            source_type=EntityType.DATA_PRODUCT,
            source_id=entity_id,
            target_type=EntityType.DATA_PRODUCT,
            target_id=entity_id,
            link_type=EntityLinkType.RELATES_TO,
        )


def test_entity_relationship_view_schema_works() -> None:
    entity_id = uuid.uuid4()
    view = EntityRelationshipView(
        entity_type=EntityType.DATA_PRODUCT,
        entity_id=entity_id,
        outgoing=[],
        incoming=[],
        total=0,
    )
    assert view.entity_type == EntityType.DATA_PRODUCT
    assert view.total == 0


def test_entity_link_filters_schema_works() -> None:
    entity_id = uuid.uuid4()
    filters = EntityLinkFilters(
        entity_type=EntityType.WORK_ITEM,
        entity_id=entity_id,
        link_type=EntityLinkType.BLOCKS,
        include_reverse=True,
    )
    assert filters.entity_type == EntityType.WORK_ITEM
    assert filters.include_reverse is True
