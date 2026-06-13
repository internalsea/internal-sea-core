import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, EntityType
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.relationships.errors import (
    EntityLinkConflictError,
    EntityLinkNotFoundError,
    InvalidEntityLinkError,
)
from app.modules.relationships.repository import EntityLinkListFilters, RelationshipRepository
from app.modules.relationships.schemas import (
    EntityLinkCreate,
    EntityLinkFilters,
    EntityLinkListResponse,
    EntityLinkRead,
    EntityLinkUpdate,
    EntityRelationshipView,
)
from app.modules.relationships.validators import (
    SUPPORTED_ENTITY_TYPES,
    is_supported_entity_type,
    validate_entity_exists,
)


class RelationshipService:
    def __init__(
        self,
        repository: RelationshipRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._session = session

    def _to_activity_entity_type(self, entity_type: EntityType) -> ActivityEntityType | None:
        try:
            return ActivityEntityType(entity_type.value)
        except ValueError:
            return None

    async def _record_link_activity(
        self,
        *,
        entity_type: EntityType,
        entity_id: uuid.UUID,
        action: ActivityAction,
        description: str,
        link_id: uuid.UUID,
        actor_id: uuid.UUID | None = None,
    ) -> None:
        activity_entity_type = self._to_activity_entity_type(entity_type)
        if activity_entity_type is None:
            return
        title = "Relationship added" if action == ActivityAction.LINKED else "Relationship removed"
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=activity_entity_type,
                entity_id=entity_id,
                action=action,
                actor_id=actor_id,
                title=title,
                description=description,
                details={"link_id": str(link_id)},
            )
        )

    async def list_links(
        self,
        *,
        filters: EntityLinkFilters,
        page: int,
        page_size: int,
    ) -> EntityLinkListResponse:
        if filters.entity_type is not None and not is_supported_entity_type(filters.entity_type):
            raise InvalidEntityLinkError(f"Unsupported entity type: {filters.entity_type.value}")
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        repo_filters = EntityLinkListFilters(
            entity_type=filters.entity_type,
            entity_id=filters.entity_id,
            source_type=filters.source_type,
            source_id=filters.source_id,
            target_type=filters.target_type,
            target_id=filters.target_id,
            link_type=filters.link_type,
            include_reverse=filters.include_reverse,
        )
        items, total = await self._repository.list(
            filters=repo_filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return EntityLinkListResponse(
            items=[EntityLinkRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_relationship_view(
        self,
        entity_type: EntityType,
        entity_id: uuid.UUID,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> EntityRelationshipView:
        if not is_supported_entity_type(entity_type):
            raise InvalidEntityLinkError(f"Unsupported entity type: {entity_type.value}")
        await validate_entity_exists(self._session, entity_type, entity_id)

        items, total = await self._repository.list_for_entity(
            entity_type=entity_type,
            entity_id=entity_id,
            include_reverse=True,
            offset=0,
            limit=page_size,
        )
        entity_type_value = entity_type.value
        outgoing = [
            EntityLinkRead.model_validate(item)
            for item in items
            if item.source_type == entity_type_value and item.source_id == entity_id
        ]
        incoming = [
            EntityLinkRead.model_validate(item)
            for item in items
            if item.target_type == entity_type_value and item.target_id == entity_id
        ]
        return EntityRelationshipView(
            entity_type=entity_type,
            entity_id=entity_id,
            outgoing=outgoing,
            incoming=incoming,
            total=total,
        )

    async def get_link(self, link_id: uuid.UUID) -> EntityLinkRead:
        link = await self._repository.get_by_id(link_id)
        if link is None:
            raise EntityLinkNotFoundError(link_id)
        return EntityLinkRead.model_validate(link)

    async def create_link(self, payload: EntityLinkCreate) -> EntityLinkRead:
        if payload.source_type not in SUPPORTED_ENTITY_TYPES:
            raise InvalidEntityLinkError(f"Unsupported source type: {payload.source_type.value}")
        if payload.target_type not in SUPPORTED_ENTITY_TYPES:
            raise InvalidEntityLinkError(f"Unsupported target type: {payload.target_type.value}")

        await validate_entity_exists(self._session, payload.source_type, payload.source_id)
        await validate_entity_exists(self._session, payload.target_type, payload.target_id)

        duplicate = await self._repository.get_duplicate(
            source_type=payload.source_type,
            source_id=payload.source_id,
            target_type=payload.target_type,
            target_id=payload.target_id,
            link_type=payload.link_type,
        )
        if duplicate is not None:
            raise EntityLinkConflictError(
                "A relationship with the same source, target and link type already exists"
            )

        link = await self._repository.create(payload)
        description = (
            f"{payload.source_type.value} linked to {payload.target_type.value} "
            f"as {payload.link_type.value}"
        )
        await self._record_link_activity(
            entity_type=payload.source_type,
            entity_id=payload.source_id,
            action=ActivityAction.LINKED,
            description=description,
            link_id=link.id,
            actor_id=payload.created_by_id,
        )
        await self._record_link_activity(
            entity_type=payload.target_type,
            entity_id=payload.target_id,
            action=ActivityAction.LINKED,
            description=description,
            link_id=link.id,
            actor_id=payload.created_by_id,
        )
        return EntityLinkRead.model_validate(link)

    async def update_link(
        self,
        link_id: uuid.UUID,
        payload: EntityLinkUpdate,
    ) -> EntityLinkRead:
        link = await self._repository.get_by_id(link_id)
        if link is None:
            raise EntityLinkNotFoundError(link_id)
        updated = await self._repository.update(link, payload)
        return EntityLinkRead.model_validate(updated)

    async def delete_link(self, link_id: uuid.UUID) -> None:
        link = await self._repository.get_by_id(link_id)
        if link is None:
            raise EntityLinkNotFoundError(link_id)

        description = f"{link.source_type} unlinked from {link.target_type} ({link.link_type})"
        source_type = EntityType(link.source_type)
        target_type = EntityType(link.target_type)

        await self._repository.delete(link)

        await self._record_link_activity(
            entity_type=source_type,
            entity_id=link.source_id,
            action=ActivityAction.UNLINKED,
            description=description,
            link_id=link_id,
            actor_id=link.created_by_id,
        )
        await self._record_link_activity(
            entity_type=target_type,
            entity_id=link.target_id,
            action=ActivityAction.UNLINKED,
            description=description,
            link_id=link_id,
            actor_id=link.created_by_id,
        )
