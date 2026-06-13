import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import EntityType, ProjectType
from app.models.catalog import DataProduct
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.relationships.errors import EntityNotFoundError, UnsupportedEntityTypeError

SUPPORTED_ENTITY_TYPES: frozenset[EntityType] = frozenset(
    {
        EntityType.DATA_PRODUCT,
        EntityType.WORK_ITEM,
        EntityType.PROJECT,
        EntityType.INTERNAL_PROJECT,
        EntityType.PERSON,
        EntityType.TEAM,
        EntityType.CAPABILITY,
    }
)


def is_supported_entity_type(entity_type: EntityType) -> bool:
    return entity_type in SUPPORTED_ENTITY_TYPES


async def validate_entity_exists(
    session: AsyncSession,
    entity_type: EntityType,
    entity_id: uuid.UUID,
) -> bool:
    if not is_supported_entity_type(entity_type):
        raise UnsupportedEntityTypeError(entity_type.value)

    exists = await _entity_exists(session, entity_type, entity_id)
    if not exists:
        raise EntityNotFoundError(entity_type.value, entity_id)
    return True


async def _entity_exists(
    session: AsyncSession,
    entity_type: EntityType,
    entity_id: uuid.UUID,
) -> bool:
    if entity_type == EntityType.DATA_PRODUCT:
        return await session.get(DataProduct, entity_id) is not None
    if entity_type == EntityType.WORK_ITEM:
        return await session.get(WorkItem, entity_id) is not None
    if entity_type == EntityType.PROJECT:
        project = await session.get(Project, entity_id)
        return project is not None and project.project_type != ProjectType.INTERNAL_PROJECT
    if entity_type == EntityType.INTERNAL_PROJECT:
        project = await session.get(Project, entity_id)
        return project is not None and project.project_type == ProjectType.INTERNAL_PROJECT
    if entity_type == EntityType.PERSON:
        return await session.get(Person, entity_id) is not None
    if entity_type == EntityType.TEAM:
        return await session.get(Team, entity_id) is not None
    if entity_type == EntityType.CAPABILITY:
        return await session.get(Capability, entity_id) is not None
    return False


async def get_entity_display_name(
    session: AsyncSession,
    entity_type: EntityType,
    entity_id: uuid.UUID,
) -> str | None:
    if entity_type == EntityType.DATA_PRODUCT:
        data_product = await session.get(DataProduct, entity_id)
        return data_product.name if data_product else None
    if entity_type == EntityType.WORK_ITEM:
        work_item = await session.get(WorkItem, entity_id)
        return work_item.title if work_item else None
    if entity_type in (EntityType.PROJECT, EntityType.INTERNAL_PROJECT):
        project = await session.get(Project, entity_id)
        return project.name if project else None
    if entity_type == EntityType.PERSON:
        person = await session.get(Person, entity_id)
        return person.full_name if person else None
    if entity_type == EntityType.TEAM:
        team = await session.get(Team, entity_id)
        return team.name if team else None
    if entity_type == EntityType.CAPABILITY:
        capability = await session.get(Capability, entity_id)
        return capability.name if capability else None
    return None
