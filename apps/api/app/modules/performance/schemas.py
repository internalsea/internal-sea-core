import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import (
    MetricDirection,
    MetricFrequency,
    MetricStatus,
    MetricValueStatus,
    MetricValueType,
    PerformanceSubjectType,
    PerformanceTrend,
)


class PerformanceMetricDefinitionBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    code: str | None = Field(default=None, max_length=100)
    description: str | None = None
    subject_type: PerformanceSubjectType
    value_type: MetricValueType = MetricValueType.NUMBER
    direction: MetricDirection = MetricDirection.NEUTRAL
    frequency: MetricFrequency | None = None
    status: MetricStatus = MetricStatus.ACTIVE
    unit: str | None = Field(default=None, max_length=50)
    target_value: Decimal | None = None
    warning_threshold: Decimal | None = None
    critical_threshold: Decimal | None = None
    owner_id: uuid.UUID | None = None


class PerformanceMetricDefinitionCreate(PerformanceMetricDefinitionBase):
    pass


class PerformanceMetricDefinitionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, max_length=100)
    description: str | None = None
    subject_type: PerformanceSubjectType | None = None
    value_type: MetricValueType | None = None
    direction: MetricDirection | None = None
    frequency: MetricFrequency | None = None
    status: MetricStatus | None = None
    unit: str | None = Field(default=None, max_length=50)
    target_value: Decimal | None = None
    warning_threshold: Decimal | None = None
    critical_threshold: Decimal | None = None
    owner_id: uuid.UUID | None = None


class PerformanceMetricDefinitionRead(PerformanceMetricDefinitionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PerformanceMetricDefinitionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    code: str | None
    subject_type: PerformanceSubjectType
    value_type: MetricValueType
    direction: MetricDirection
    frequency: MetricFrequency | None
    status: MetricStatus
    unit: str | None
    target_value: Decimal | None
    owner_id: uuid.UUID | None
    updated_at: datetime


class PerformanceMetricDefinitionListResponse(BaseModel):
    items: list[PerformanceMetricDefinitionListItem]
    total: int
    page: int
    page_size: int
    pages: int


class PerformanceMetricDefinitionFilters(BaseModel):
    search: str | None = None
    subject_type: PerformanceSubjectType | None = None
    value_type: MetricValueType | None = None
    status: MetricStatus | None = None
    owner_id: uuid.UUID | None = None


class PerformanceMetricValueBase(BaseModel):
    metric_definition_id: uuid.UUID
    subject_type: PerformanceSubjectType
    subject_id: uuid.UUID
    period_start: date | None = None
    period_end: date | None = None
    value_numeric: Decimal | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    status: MetricValueStatus = MetricValueStatus.SUBMITTED
    source: str | None = None
    comment: str | None = None
    submitted_by_id: uuid.UUID | None = None
    approved_by_id: uuid.UUID | None = None
    approved_at: datetime | None = None

    @model_validator(mode="after")
    def validate_value_fields(self) -> "PerformanceMetricValueBase":
        if (
            self.value_numeric is None
            and self.value_text is None
            and self.value_bool is None
        ):
            raise ValueError("At least one value field must be provided")
        if (
            self.period_start is not None
            and self.period_end is not None
            and self.period_end < self.period_start
        ):
            raise ValueError("period_end must not be before period_start")
        return self


class PerformanceMetricValueCreate(PerformanceMetricValueBase):
    pass


class PerformanceMetricValueUpdate(BaseModel):
    metric_definition_id: uuid.UUID | None = None
    subject_type: PerformanceSubjectType | None = None
    subject_id: uuid.UUID | None = None
    period_start: date | None = None
    period_end: date | None = None
    value_numeric: Decimal | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    status: MetricValueStatus | None = None
    source: str | None = None
    comment: str | None = None
    submitted_by_id: uuid.UUID | None = None
    approved_by_id: uuid.UUID | None = None
    approved_at: datetime | None = None

    @model_validator(mode="after")
    def validate_period(self) -> "PerformanceMetricValueUpdate":
        if (
            self.period_start is not None
            and self.period_end is not None
            and self.period_end < self.period_start
        ):
            raise ValueError("period_end must not be before period_start")
        return self


class PerformanceMetricValueRead(PerformanceMetricValueBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PerformanceMetricValueListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    metric_definition_id: uuid.UUID
    subject_type: PerformanceSubjectType
    subject_id: uuid.UUID
    period_start: date | None
    period_end: date | None
    value_numeric: Decimal | None
    value_text: str | None
    value_bool: bool | None
    status: MetricValueStatus
    source: str | None
    updated_at: datetime


class PerformanceMetricValueListResponse(BaseModel):
    items: list[PerformanceMetricValueListItem]
    total: int
    page: int
    page_size: int
    pages: int


class PerformanceMetricValueFilters(BaseModel):
    metric_definition_id: uuid.UUID | None = None
    subject_type: PerformanceSubjectType | None = None
    subject_id: uuid.UUID | None = None
    status: MetricValueStatus | None = None
    period_start_from: date | None = None
    period_end_to: date | None = None


class PerformanceScorecardMetric(BaseModel):
    metric_definition_id: uuid.UUID
    name: str
    code: str | None
    value_type: MetricValueType
    direction: MetricDirection
    unit: str | None
    target_value: Decimal | None
    current_value_numeric: Decimal | None
    current_value_text: str | None
    current_value_bool: bool | None
    previous_value_numeric: Decimal | None
    trend: PerformanceTrend
    status: str | None
    period_start: date | None
    period_end: date | None
    score: Decimal | None
    interpretation: str | None


class PerformanceScorecard(BaseModel):
    subject_type: PerformanceSubjectType
    subject_id: uuid.UUID
    metrics: list[PerformanceScorecardMetric]
    metrics_total: int
    metrics_with_values: int
    average_score: Decimal | None
    health_status: str | None
    updated_at: datetime | None


class PerformanceOverview(BaseModel):
    metric_definitions_total: int = 0
    metric_definitions_active: int = 0
    metric_values_total: int = 0
    scorecards_available: int = 0
    people_metrics_count: int = 0
    team_metrics_count: int = 0
    capability_metrics_count: int = 0
    project_metrics_count: int = 0
    data_product_metrics_count: int = 0
