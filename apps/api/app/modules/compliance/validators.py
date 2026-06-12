import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import ComplianceSubjectType, ProjectType
from app.models.catalog import DataProduct
from app.models.people import Capability, Team
from app.models.projects import Project
from app.modules.compliance.errors import (
    ComplianceSubjectNotFoundError,
    UnsupportedComplianceSubjectTypeError,
)

SUPPORTED_COMPLIANCE_SUBJECT_TYPES: frozenset[ComplianceSubjectType] = frozenset(
    {
        ComplianceSubjectType.DATA_PRODUCT,
        ComplianceSubjectType.PROJECT,
        ComplianceSubjectType.INTERNAL_PROJECT,
        ComplianceSubjectType.TEAM,
        ComplianceSubjectType.CAPABILITY,
    }
)


def is_supported_compliance_subject_type(subject_type: ComplianceSubjectType) -> bool:
    return subject_type in SUPPORTED_COMPLIANCE_SUBJECT_TYPES


async def validate_compliance_subject_exists(
    session: AsyncSession,
    subject_type: ComplianceSubjectType,
    subject_id: uuid.UUID,
) -> bool:
    if not is_supported_compliance_subject_type(subject_type):
        raise UnsupportedComplianceSubjectTypeError(subject_type.value)

    exists = await _subject_exists(session, subject_type, subject_id)
    if not exists:
        raise ComplianceSubjectNotFoundError(subject_type.value, subject_id)
    return True


async def _subject_exists(
    session: AsyncSession,
    subject_type: ComplianceSubjectType,
    subject_id: uuid.UUID,
) -> bool:
    if subject_type == ComplianceSubjectType.DATA_PRODUCT:
        return await session.get(DataProduct, subject_id) is not None
    if subject_type == ComplianceSubjectType.PROJECT:
        project = await session.get(Project, subject_id)
        return project is not None and project.project_type != ProjectType.INTERNAL_PROJECT
    if subject_type == ComplianceSubjectType.INTERNAL_PROJECT:
        project = await session.get(Project, subject_id)
        return project is not None and project.project_type == ProjectType.INTERNAL_PROJECT
    if subject_type == ComplianceSubjectType.TEAM:
        return await session.get(Team, subject_id) is not None
    if subject_type == ComplianceSubjectType.CAPABILITY:
        return await session.get(Capability, subject_id) is not None
    return False
