import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import EntityLinkType, EntityType
from app.models.relationships import EntityLink
from app.modules.relationships.schemas import EntityLinkCreate, EntityLinkUpdate


@dataclass
class EntityLinkListFilters:
    entity_type: EntityType | None = None
    entity_id: uuid.UUID | None = None
    source_type: EntityType | None = None
    source_id: uuid.UUID | None = None
    target_type: EntityType | None = None
    target_id: uuid.UUID | None = None
    link_type: EntityLinkType | None = None
    include_reverse: bool = True


class RelationshipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query, filters: EntityLinkListFilters):
        if filters.source_type is not None:
            query = query.where(EntityLink.source_type == filters.source_type.value)
        if filters.source_id is not None:
            query = query.where(EntityLink.source_id == filters.source_id)
        if filters.target_type is not None:
            query = query.where(EntityLink.target_type == filters.target_type.value)
        if filters.target_id is not None:
            query = query.where(EntityLink.target_id == filters.target_id)
        if filters.link_type is not None:
            query = query.where(EntityLink.link_type == filters.link_type.value)

        if filters.entity_type is not None and filters.entity_id is not None:
            entity_type_value = filters.entity_type.value
            if filters.include_reverse:
                query = query.where(
                    or_(
                        (EntityLink.source_type == entity_type_value)
                        & (EntityLink.source_id == filters.entity_id),
                        (EntityLink.target_type == entity_type_value)
                        & (EntityLink.target_id == filters.entity_id),
                    )
                )
            else:
                query = query.where(
                    (EntityLink.source_type == entity_type_value)
                    & (EntityLink.source_id == filters.entity_id)
                )
        return query

    async def list(
        self,
        *,
        filters: EntityLinkListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[EntityLink], int]:
        base_query = select(EntityLink)
        base_query = self._apply_filters(base_query, filters)

        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self._session.scalar(count_query) or 0

        items_query = (
            base_query.order_by(EntityLink.created_at.desc()).offset(offset).limit(limit)
        )
        result = await self._session.execute(items_query)
        return list(result.scalars().all()), total

    async def list_for_entity(
        self,
        *,
        entity_type: EntityType,
        entity_id: uuid.UUID,
        include_reverse: bool = True,
        offset: int,
        limit: int,
    ) -> tuple[list[EntityLink], int]:
        filters = EntityLinkListFilters(
            entity_type=entity_type,
            entity_id=entity_id,
            include_reverse=include_reverse,
        )
        return await self.list(filters=filters, offset=offset, limit=limit)

    async def get_by_id(self, link_id: uuid.UUID) -> EntityLink | None:
        return await self._session.get(EntityLink, link_id)

    async def get_duplicate(
        self,
        *,
        source_type: EntityType,
        source_id: uuid.UUID,
        target_type: EntityType,
        target_id: uuid.UUID,
        link_type: EntityLinkType,
    ) -> EntityLink | None:
        result = await self._session.execute(
            select(EntityLink).where(
                EntityLink.source_type == source_type.value,
                EntityLink.source_id == source_id,
                EntityLink.target_type == target_type.value,
                EntityLink.target_id == target_id,
                EntityLink.link_type == link_type.value,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, payload: EntityLinkCreate) -> EntityLink:
        link = EntityLink(
            source_type=payload.source_type.value,
            source_id=payload.source_id,
            target_type=payload.target_type.value,
            target_id=payload.target_id,
            link_type=payload.link_type.value,
            title=payload.title,
            description=payload.description,
            created_by_id=payload.created_by_id,
        )
        self._session.add(link)
        await self._session.commit()
        await self._session.refresh(link)
        return link

    async def update(self, link: EntityLink, payload: EntityLinkUpdate) -> EntityLink:
        update_data = payload.model_dump(exclude_unset=True)
        if "link_type" in update_data and update_data["link_type"] is not None:
            link.link_type = update_data["link_type"].value
        if "title" in update_data:
            link.title = update_data["title"]
        if "description" in update_data:
            link.description = update_data["description"]
        await self._session.commit()
        await self._session.refresh(link)
        return link

    async def delete(self, link: EntityLink) -> None:
        await self._session.delete(link)
        await self._session.commit()
