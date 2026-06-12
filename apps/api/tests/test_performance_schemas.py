from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.enums import PerformanceSubjectType
from app.modules.performance.schemas import (
    PerformanceMetricDefinitionCreate,
    PerformanceMetricValueCreate,
)


def test_metric_definition_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        PerformanceMetricDefinitionCreate(
            name="",
            subject_type=PerformanceSubjectType.DATA_PRODUCT,
        )


def test_metric_value_create_requires_at_least_one_value_field() -> None:
    with pytest.raises(ValidationError):
        PerformanceMetricValueCreate(
            metric_definition_id=uuid4(),
            subject_type=PerformanceSubjectType.DATA_PRODUCT,
            subject_id=uuid4(),
        )


def test_metric_value_create_period_validation() -> None:
    with pytest.raises(ValidationError):
        PerformanceMetricValueCreate(
            metric_definition_id=uuid4(),
            subject_type=PerformanceSubjectType.DATA_PRODUCT,
            subject_id=uuid4(),
            period_start=date(2026, 6, 30),
            period_end=date(2026, 6, 1),
            value_numeric=Decimal("90"),
        )


def test_metric_value_create_accepts_numeric_value() -> None:
    payload = PerformanceMetricValueCreate(
        metric_definition_id=uuid4(),
        subject_type=PerformanceSubjectType.TEAM,
        subject_id=uuid4(),
        value_numeric=Decimal("82"),
    )
    assert payload.value_numeric == Decimal("82")
