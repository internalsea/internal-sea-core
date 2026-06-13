import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import (
    ActivityAction,
    ActivityEntityType,
    MetricDirection,
    MetricFrequency,
    MetricStatus,
    MetricValueStatus,
    MetricValueType,
    PerformanceSubjectType,
)
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.performance.errors import (
    PerformanceMetricConflictError,
    PerformanceMetricDefinitionNotFoundError,
    PerformanceMetricValueNotFoundError,
    PerformanceValidationError,
    UnsupportedPerformanceSubjectTypeError,
)
from app.modules.performance.repository import (
    PerformanceDefinitionListFilters,
    PerformanceRepository,
    PerformanceValueListFilters,
)
from app.modules.performance.schemas import (
    PerformanceMetricDefinitionCreate,
    PerformanceMetricDefinitionFilters,
    PerformanceMetricDefinitionListItem,
    PerformanceMetricDefinitionListResponse,
    PerformanceMetricDefinitionRead,
    PerformanceMetricDefinitionUpdate,
    PerformanceMetricValueCreate,
    PerformanceMetricValueFilters,
    PerformanceMetricValueListItem,
    PerformanceMetricValueListResponse,
    PerformanceMetricValueRead,
    PerformanceMetricValueUpdate,
    PerformanceOverview,
    PerformanceScorecard,
    PerformanceScorecardMetric,
)
from app.modules.performance.scoring import (
    calculate_metric_score,
    calculate_trend,
    interpret_metric,
)
from app.modules.performance.validators import (
    is_supported_performance_subject_type,
    validate_performance_subject_exists,
)


class PerformanceService:
    def __init__(
        self,
        repository: PerformanceRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._session = session

    def _enum_value(self, value: object) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    def _to_activity_entity_type(
        self,
        subject_type: PerformanceSubjectType,
    ) -> ActivityEntityType | None:
        try:
            return ActivityEntityType(subject_type.value)
        except ValueError:
            return None

    def _definition_to_list_item(
        self, definition: PerformanceMetricDefinition
    ) -> PerformanceMetricDefinitionListItem:
        return PerformanceMetricDefinitionListItem(
            id=definition.id,
            name=definition.name,
            code=definition.code,
            subject_type=PerformanceSubjectType(definition.subject_type),
            value_type=MetricValueType(definition.value_type),
            direction=MetricDirection(definition.direction),
            frequency=MetricFrequency(definition.frequency) if definition.frequency else None,
            status=MetricStatus(definition.status),
            unit=definition.unit,
            target_value=definition.target_value,
            owner_id=definition.owner_id,
            updated_at=definition.updated_at,
        )

    def _value_to_list_item(self, value: PerformanceMetricValue) -> PerformanceMetricValueListItem:
        return PerformanceMetricValueListItem(
            id=value.id,
            metric_definition_id=value.metric_definition_id,
            subject_type=PerformanceSubjectType(value.subject_type),
            subject_id=value.subject_id,
            period_start=value.period_start,
            period_end=value.period_end,
            value_numeric=value.value_numeric,
            value_text=value.value_text,
            value_bool=value.value_bool,
            status=MetricValueStatus(value.status),
            source=value.source,
            updated_at=value.updated_at,
        )

    def _health_status_from_score(self, average_score: Decimal | None) -> str | None:
        if average_score is None:
            return "unknown"
        if average_score >= Decimal("90"):
            return "good"
        if average_score >= Decimal("70"):
            return "warning"
        return "critical"

    async def list_definitions(
        self,
        *,
        filters: PerformanceMetricDefinitionFilters,
        page: int,
        page_size: int,
    ) -> PerformanceMetricDefinitionListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        repo_filters = PerformanceDefinitionListFilters(
            search=filters.search,
            subject_type=filters.subject_type,
            value_type=self._enum_value(filters.value_type),
            status=filters.status,
            owner_id=filters.owner_id,
        )
        definitions, total = await self._repository.list_definitions(
            filters=repo_filters,
            offset=offset,
            limit=page_size,
        )
        return PerformanceMetricDefinitionListResponse(
            items=[self._definition_to_list_item(item) for item in definitions],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_definition(self, definition_id: uuid.UUID) -> PerformanceMetricDefinitionRead:
        definition = await self._repository.get_definition_by_id(definition_id)
        if definition is None:
            raise PerformanceMetricDefinitionNotFoundError(definition_id)
        return PerformanceMetricDefinitionRead.model_validate(definition)

    async def create_definition(
        self,
        payload: PerformanceMetricDefinitionCreate,
    ) -> PerformanceMetricDefinitionRead:
        if payload.code:
            existing = await self._repository.get_definition_by_code(payload.code)
            if existing is not None:
                raise PerformanceMetricConflictError(
                    f"Metric definition with code {payload.code} already exists"
                )

        data = payload.model_dump()
        for key in ("subject_type", "value_type", "direction", "frequency", "status"):
            data[key] = self._enum_value(data[key])
        definition = await self._repository.create_definition(data)
        return PerformanceMetricDefinitionRead.model_validate(definition)

    async def update_definition(
        self,
        definition_id: uuid.UUID,
        payload: PerformanceMetricDefinitionUpdate,
    ) -> PerformanceMetricDefinitionRead:
        definition = await self._repository.get_definition_by_id(definition_id)
        if definition is None:
            raise PerformanceMetricDefinitionNotFoundError(definition_id)

        update_data = payload.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"]:
            existing = await self._repository.get_definition_by_code(update_data["code"])
            if existing is not None and existing.id != definition_id:
                raise PerformanceMetricConflictError(
                    f"Metric definition with code {update_data['code']} already exists"
                )

        for key in ("subject_type", "value_type", "direction", "frequency", "status"):
            if key in update_data and update_data[key] is not None:
                update_data[key] = self._enum_value(update_data[key])

        definition = await self._repository.update_definition(definition, update_data)
        return PerformanceMetricDefinitionRead.model_validate(definition)

    async def delete_definition(self, definition_id: uuid.UUID) -> None:
        definition = await self._repository.get_definition_by_id(definition_id)
        if definition is None:
            raise PerformanceMetricDefinitionNotFoundError(definition_id)
        await self._repository.delete_definition(definition)

    async def _validate_value_payload(
        self,
        *,
        metric_definition_id: uuid.UUID,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        period_start: date | None,
        period_end: date | None,
        exclude_value_id: uuid.UUID | None = None,
        require_value_field: bool = False,
        value_numeric: Decimal | None = None,
        value_text: str | None = None,
        value_bool: bool | None = None,
    ) -> None:
        if not is_supported_performance_subject_type(subject_type):
            raise UnsupportedPerformanceSubjectTypeError(subject_type.value)

        await validate_performance_subject_exists(self._session, subject_type, subject_id)

        definition = await self._repository.get_definition_by_id(metric_definition_id)
        if definition is None:
            raise PerformanceMetricDefinitionNotFoundError(metric_definition_id)

        allowed_subject_types = {definition.subject_type}
        if definition.subject_type == PerformanceSubjectType.PROJECT.value:
            allowed_subject_types.add(PerformanceSubjectType.INTERNAL_PROJECT.value)
        if subject_type.value not in allowed_subject_types:
            raise PerformanceValidationError(
                "Metric value subject_type must match metric definition subject_type"
            )

        duplicate = await self._repository.get_duplicate_value(
            metric_definition_id,
            subject_type,
            subject_id,
            period_start,
            period_end,
            exclude_id=exclude_value_id,
        )
        if duplicate is not None:
            raise PerformanceMetricConflictError(
                "A metric value already exists for this subject and period"
            )

        if (
            require_value_field
            and value_numeric is None
            and value_text is None
            and value_bool is None
        ):
            raise PerformanceValidationError("At least one value field must be provided")

    async def list_values(
        self,
        *,
        filters: PerformanceMetricValueFilters,
        page: int,
        page_size: int,
    ) -> PerformanceMetricValueListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        repo_filters = PerformanceValueListFilters(
            metric_definition_id=filters.metric_definition_id,
            subject_type=filters.subject_type,
            subject_id=filters.subject_id,
            status=self._enum_value(filters.status),
            period_start_from=filters.period_start_from,
            period_end_to=filters.period_end_to,
        )
        values, total = await self._repository.list_values(
            filters=repo_filters,
            offset=offset,
            limit=page_size,
        )
        return PerformanceMetricValueListResponse(
            items=[self._value_to_list_item(item) for item in values],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_value(self, value_id: uuid.UUID) -> PerformanceMetricValueRead:
        value = await self._repository.get_value_by_id(value_id)
        if value is None:
            raise PerformanceMetricValueNotFoundError(value_id)
        return PerformanceMetricValueRead.model_validate(value)

    async def _record_value_activity(
        self,
        *,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        metric_name: str,
        value_display: str,
    ) -> None:
        entity_type = self._to_activity_entity_type(subject_type)
        if entity_type is None:
            return
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=entity_type,
                entity_id=subject_id,
                action=ActivityAction.UPDATED,
                title="Performance metric updated",
                description=f"{metric_name}: {value_display}",
            )
        )

    def _format_value_display(self, value: PerformanceMetricValue) -> str:
        if value.value_numeric is not None:
            return str(value.value_numeric)
        if value.value_text is not None:
            return value.value_text
        if value.value_bool is not None:
            return "true" if value.value_bool else "false"
        return "—"

    async def create_value(
        self,
        payload: PerformanceMetricValueCreate,
    ) -> PerformanceMetricValueRead:
        await self._validate_value_payload(
            metric_definition_id=payload.metric_definition_id,
            subject_type=payload.subject_type,
            subject_id=payload.subject_id,
            period_start=payload.period_start,
            period_end=payload.period_end,
        )

        data = payload.model_dump()
        data["subject_type"] = self._enum_value(data["subject_type"])
        data["status"] = self._enum_value(data["status"])
        value = await self._repository.create_value(data)

        definition = await self._repository.get_definition_by_id(payload.metric_definition_id)
        if definition is not None:
            await self._record_value_activity(
                subject_type=payload.subject_type,
                subject_id=payload.subject_id,
                metric_name=definition.name,
                value_display=self._format_value_display(value),
            )

        return PerformanceMetricValueRead.model_validate(value)

    async def update_value(
        self,
        value_id: uuid.UUID,
        payload: PerformanceMetricValueUpdate,
    ) -> PerformanceMetricValueRead:
        value = await self._repository.get_value_by_id(value_id)
        if value is None:
            raise PerformanceMetricValueNotFoundError(value_id)

        update_data = payload.model_dump(exclude_unset=True)
        metric_definition_id = update_data.get("metric_definition_id", value.metric_definition_id)
        subject_type = PerformanceSubjectType(update_data.get("subject_type", value.subject_type))
        subject_id = update_data.get("subject_id", value.subject_id)
        period_start = update_data.get("period_start", value.period_start)
        period_end = update_data.get("period_end", value.period_end)

        merged_numeric = update_data.get("value_numeric", value.value_numeric)
        merged_text = update_data.get("value_text", value.value_text)
        merged_bool = update_data.get("value_bool", value.value_bool)

        await self._validate_value_payload(
            metric_definition_id=metric_definition_id,
            subject_type=subject_type,
            subject_id=subject_id,
            period_start=period_start,
            period_end=period_end,
            exclude_value_id=value_id,
            require_value_field=True,
            value_numeric=merged_numeric,
            value_text=merged_text,
            value_bool=merged_bool,
        )

        if "subject_type" in update_data:
            update_data["subject_type"] = self._enum_value(update_data["subject_type"])
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = self._enum_value(update_data["status"])

        value = await self._repository.update_value(value, update_data)

        definition = await self._repository.get_definition_by_id(value.metric_definition_id)
        if definition is not None:
            await self._record_value_activity(
                subject_type=PerformanceSubjectType(value.subject_type),
                subject_id=value.subject_id,
                metric_name=definition.name,
                value_display=self._format_value_display(value),
            )

        return PerformanceMetricValueRead.model_validate(value)

    async def delete_value(self, value_id: uuid.UUID) -> None:
        value = await self._repository.get_value_by_id(value_id)
        if value is None:
            raise PerformanceMetricValueNotFoundError(value_id)
        await self._repository.delete_value(value)

    async def get_entity_scorecard(
        self,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
    ) -> PerformanceScorecard:
        if not is_supported_performance_subject_type(subject_type):
            raise UnsupportedPerformanceSubjectTypeError(subject_type.value)
        await validate_performance_subject_exists(self._session, subject_type, subject_id)

        definitions = await self._repository.get_scorecard_definitions(subject_type)
        metrics: list[PerformanceScorecardMetric] = []
        scores: list[Decimal] = []
        latest_updated = None

        for definition in definitions:
            current = await self._repository.get_latest_value(
                definition.id,
                subject_type,
                subject_id,
            )
            previous = None
            if current is not None:
                previous = await self._repository.get_previous_value(
                    definition.id,
                    subject_type,
                    subject_id,
                    current.period_start,
                )
                if latest_updated is None or current.updated_at > latest_updated:
                    latest_updated = current.updated_at

            current_numeric = (
                Decimal(str(current.value_numeric))
                if current is not None and current.value_numeric is not None
                else None
            )
            previous_numeric = (
                Decimal(str(previous.value_numeric))
                if previous is not None and previous.value_numeric is not None
                else None
            )
            direction = MetricDirection(definition.direction)
            score = calculate_metric_score(definition, current)
            if score is not None:
                scores.append(score)

            metrics.append(
                PerformanceScorecardMetric(
                    metric_definition_id=definition.id,
                    name=definition.name,
                    code=definition.code,
                    value_type=MetricValueType(definition.value_type),
                    direction=direction,
                    unit=definition.unit,
                    target_value=definition.target_value,
                    current_value_numeric=current.value_numeric if current else None,
                    current_value_text=current.value_text if current else None,
                    current_value_bool=current.value_bool if current else None,
                    previous_value_numeric=previous.value_numeric if previous else None,
                    trend=calculate_trend(current_numeric, previous_numeric, direction),
                    status=current.status if current else None,
                    period_start=current.period_start if current else None,
                    period_end=current.period_end if current else None,
                    score=score,
                    interpretation=interpret_metric(definition, current, score),
                )
            )

        average_score = None
        if scores:
            average_score = (sum(scores) / Decimal(len(scores))).quantize(Decimal("0.01"))

        metrics_with_values = sum(
            1 for metric in metrics if metric.current_value_numeric is not None
        )

        return PerformanceScorecard(
            subject_type=subject_type,
            subject_id=subject_id,
            metrics=metrics,
            metrics_total=len(definitions),
            metrics_with_values=metrics_with_values,
            average_score=average_score,
            health_status=self._health_status_from_score(average_score),
            updated_at=latest_updated,
        )

    async def list_entity_values(
        self,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> PerformanceMetricValueListResponse:
        if not is_supported_performance_subject_type(subject_type):
            raise UnsupportedPerformanceSubjectTypeError(subject_type.value)
        await validate_performance_subject_exists(self._session, subject_type, subject_id)

        page, page_size, offset = normalize_pagination(page, page_size)
        values, total = await self._repository.list_values_for_subject(
            subject_type,
            subject_id,
            offset=offset,
            limit=page_size,
        )
        return PerformanceMetricValueListResponse(
            items=[self._value_to_list_item(item) for item in values],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_overview(self) -> PerformanceOverview:
        data = await self._repository.get_overview()
        return PerformanceOverview(**data)
