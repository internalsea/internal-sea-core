import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import PerformanceSubjectType, ProjectType
from app.models.catalog import DataProduct
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.modules.performance.errors import (
    PerformanceSubjectNotFoundError,
    UnsupportedPerformanceSubjectTypeError,
)

SUPPORTED_PERFORMANCE_SUBJECT_TYPES: frozenset[PerformanceSubjectType] = frozenset(
    {
        PerformanceSubjectType.PERSON,
        PerformanceSubjectType.TEAM,
        PerformanceSubjectType.CAPABILITY,
        PerformanceSubjectType.PROJECT,
        PerformanceSubjectType.INTERNAL_PROJECT,
        PerformanceSubjectType.DATA_PRODUCT,
    }
)


def is_supported_performance_subject_type(subject_type: PerformanceSubjectType) -> bool:
    return subject_type in SUPPORTED_PERFORMANCE_SUBJECT_TYPES


async def validate_performance_subject_exists(
    session: AsyncSession,
    subject_type: PerformanceSubjectType,
    subject_id: uuid.UUID,
) -> bool:
    if not is_supported_performance_subject_type(subject_type):
        raise UnsupportedPerformanceSubjectTypeError(subject_type.value)

    exists = await _subject_exists(session, subject_type, subject_id)
    if not exists:
        raise PerformanceSubjectNotFoundError(subject_type.value, subject_id)
    return True


async def _subject_exists(
    session: AsyncSession,
    subject_type: PerformanceSubjectType,
    subject_id: uuid.UUID,
) -> bool:
    if subject_type == PerformanceSubjectType.PERSON:
        return await session.get(Person, subject_id) is not None
    if subject_type == PerformanceSubjectType.TEAM:
        return await session.get(Team, subject_id) is not None
    if subject_type == PerformanceSubjectType.CAPABILITY:
        return await session.get(Capability, subject_id) is not None
    if subject_type == PerformanceSubjectType.DATA_PRODUCT:
        return await session.get(DataProduct, subject_id) is not None
    if subject_type == PerformanceSubjectType.PROJECT:
        project = await session.get(Project, subject_id)
        return project is not None and project.project_type != ProjectType.INTERNAL_PROJECT
    if subject_type == PerformanceSubjectType.INTERNAL_PROJECT:
        project = await session.get(Project, subject_id)
        return project is not None and project.project_type == ProjectType.INTERNAL_PROJECT
    return False
