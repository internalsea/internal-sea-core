import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import FileEntityType, ProjectType
from app.models.catalog import DataProduct
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.files.errors import FileEntityNotFoundError, UnsupportedFileEntityTypeError

SUPPORTED_FILE_ENTITY_TYPES: frozenset[FileEntityType] = frozenset(
    {
        FileEntityType.DATA_PRODUCT,
        FileEntityType.WORK_ITEM,
        FileEntityType.PROJECT,
        FileEntityType.INTERNAL_PROJECT,
    }
)


def is_supported_file_entity_type(entity_type: FileEntityType) -> bool:
    return entity_type in SUPPORTED_FILE_ENTITY_TYPES


async def validate_file_attachment_entity_exists(
    session: AsyncSession,
    entity_type: FileEntityType,
    entity_id: uuid.UUID,
) -> bool:
    if not is_supported_file_entity_type(entity_type):
        raise UnsupportedFileEntityTypeError(entity_type.value)

    exists = await _entity_exists(session, entity_type, entity_id)
    if not exists:
        raise FileEntityNotFoundError(entity_type.value, entity_id)
    return True


async def _entity_exists(
    session: AsyncSession,
    entity_type: FileEntityType,
    entity_id: uuid.UUID,
) -> bool:
    if entity_type == FileEntityType.DATA_PRODUCT:
        return await session.get(DataProduct, entity_id) is not None
    if entity_type == FileEntityType.WORK_ITEM:
        return await session.get(WorkItem, entity_id) is not None
    if entity_type == FileEntityType.PROJECT:
        project = await session.get(Project, entity_id)
        return project is not None and project.project_type != ProjectType.INTERNAL_PROJECT
    if entity_type == FileEntityType.INTERNAL_PROJECT:
        project = await session.get(Project, entity_id)
        return project is not None and project.project_type == ProjectType.INTERNAL_PROJECT
    return False
