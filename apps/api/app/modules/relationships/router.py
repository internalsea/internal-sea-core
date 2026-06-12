import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import EntityLinkType, EntityType
from app.modules.activity.dependencies import build_activity_service
from app.modules.relationships.repository import RelationshipRepository
from app.modules.relationships.schemas import (
    EntityLinkCreate,
    EntityLinkFilters,
    EntityLinkListResponse,
    EntityLinkRead,
    EntityLinkUpdate,
    EntityRelationshipView,
)
from app.modules.relationships.service import RelationshipService

router = APIRouter(prefix="/relationships", tags=["Relationships"])


def get_relationship_service(db: AsyncSession = Depends(get_db)) -> RelationshipService:
    return RelationshipService(
        RelationshipRepository(db),
        build_activity_service(db),
        db,
    )


@router.get("", response_model=EntityLinkListResponse)
async def list_relationships(
    _user: ViewerUser,
    entity_type: EntityType | None = None,
    entity_id: uuid.UUID | None = None,
    source_type: EntityType | None = None,
    source_id: uuid.UUID | None = None,
    target_type: EntityType | None = None,
    target_id: uuid.UUID | None = None,
    link_type: EntityLinkType | None = None,
    include_reverse: bool = True,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: RelationshipService = Depends(get_relationship_service),
) -> EntityLinkListResponse:
    filters = EntityLinkFilters(
        entity_type=entity_type,
        entity_id=entity_id,
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        link_type=link_type,
        include_reverse=include_reverse,
    )
    return await service.list_links(filters=filters, page=page, page_size=page_size)


@router.post("", response_model=EntityLinkRead, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    payload: EntityLinkCreate,
    _user: EditorUser,
    service: RelationshipService = Depends(get_relationship_service),
) -> EntityLinkRead:
    return await service.create_link(payload)


@router.get("/entity/{entity_type}/{entity_id}", response_model=EntityRelationshipView)
async def get_entity_relationships(
    entity_type: EntityType,
    entity_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=MAX_PAGE_SIZE),
    service: RelationshipService = Depends(get_relationship_service),
) -> EntityRelationshipView:
    return await service.get_relationship_view(
        entity_type,
        entity_id,
        page=page,
        page_size=page_size,
    )


@router.get("/{link_id}", response_model=EntityLinkRead)
async def get_relationship(
    link_id: uuid.UUID,
    _user: ViewerUser,
    service: RelationshipService = Depends(get_relationship_service),
) -> EntityLinkRead:
    return await service.get_link(link_id)


@router.patch("/{link_id}", response_model=EntityLinkRead)
async def update_relationship(
    link_id: uuid.UUID,
    payload: EntityLinkUpdate,
    _user: EditorUser,
    service: RelationshipService = Depends(get_relationship_service),
) -> EntityLinkRead:
    return await service.update_link(link_id, payload)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship(
    link_id: uuid.UUID,
    _user: EditorUser,
    service: RelationshipService = Depends(get_relationship_service),
) -> None:
    await service.delete_link(link_id)
