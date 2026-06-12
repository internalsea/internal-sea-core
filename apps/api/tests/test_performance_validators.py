import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import PerformanceSubjectType
from app.modules.performance.errors import (
    PerformanceSubjectNotFoundError,
    UnsupportedPerformanceSubjectTypeError,
)
from app.modules.performance.validators import (
    SUPPORTED_PERFORMANCE_SUBJECT_TYPES,
    validate_performance_subject_exists,
)


@pytest.mark.asyncio
async def test_unsupported_subject_type_validation(monkeypatch) -> None:
    session = AsyncMock()
    monkeypatch.setattr(
        "app.modules.performance.validators.is_supported_performance_subject_type",
        lambda _subject_type: False,
    )

    with pytest.raises(UnsupportedPerformanceSubjectTypeError):
        await validate_performance_subject_exists(
            session,
            PerformanceSubjectType.PERSON,
            uuid.uuid4(),
        )


def test_supported_subject_types_include_core_entities() -> None:
    assert PerformanceSubjectType.PERSON in SUPPORTED_PERFORMANCE_SUBJECT_TYPES
    assert PerformanceSubjectType.DATA_PRODUCT in SUPPORTED_PERFORMANCE_SUBJECT_TYPES


@pytest.mark.asyncio
async def test_subject_not_found_raises() -> None:
    session = AsyncMock()
    session.get.return_value = None
    subject_id = uuid.uuid4()

    with pytest.raises(PerformanceSubjectNotFoundError):
        await validate_performance_subject_exists(
            session,
            PerformanceSubjectType.TEAM,
            subject_id,
        )
