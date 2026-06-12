import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import ComplianceSubjectType, ProjectType
from app.modules.compliance.errors import (
    ComplianceSubjectNotFoundError,
    UnsupportedComplianceSubjectTypeError,
)
from app.modules.compliance.validators import (
    SUPPORTED_COMPLIANCE_SUBJECT_TYPES,
    is_supported_compliance_subject_type,
    validate_compliance_subject_exists,
)


def test_supported_compliance_subject_types() -> None:
    assert ComplianceSubjectType.DATA_PRODUCT in SUPPORTED_COMPLIANCE_SUBJECT_TYPES
    assert ComplianceSubjectType.TEAM in SUPPORTED_COMPLIANCE_SUBJECT_TYPES
    assert ComplianceSubjectType.PERSON not in SUPPORTED_COMPLIANCE_SUBJECT_TYPES


def test_is_supported_compliance_subject_type() -> None:
    assert is_supported_compliance_subject_type(ComplianceSubjectType.CAPABILITY) is True
    assert is_supported_compliance_subject_type(ComplianceSubjectType.TOOL) is False


@pytest.mark.asyncio
async def test_validate_compliance_subject_rejects_unsupported_type() -> None:
    session = AsyncMock()
    with pytest.raises(UnsupportedComplianceSubjectTypeError):
        await validate_compliance_subject_exists(
            session,
            ComplianceSubjectType.TOOL,
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_validate_compliance_subject_raises_when_missing() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with pytest.raises(ComplianceSubjectNotFoundError):
        await validate_compliance_subject_exists(
            session,
            ComplianceSubjectType.DATA_PRODUCT,
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_validate_compliance_subject_rejects_client_project_as_internal() -> None:
    session = AsyncMock()
    project = MagicMock()
    project.project_type = ProjectType.CLIENT_PROJECT
    session.get = AsyncMock(return_value=project)
    with pytest.raises(ComplianceSubjectNotFoundError):
        await validate_compliance_subject_exists(
            session,
            ComplianceSubjectType.INTERNAL_PROJECT,
            uuid.uuid4(),
        )
