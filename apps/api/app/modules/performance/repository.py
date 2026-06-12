import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import MetricStatus, PerformanceSubjectType
from app.models.performance import PerformanceMetricDefinition, PerformanceMetricValue


@dataclass
class PerformanceDefinitionListFilters:
    search: str | None = None
    subject_type: PerformanceSubjectType | None = None
    value_type: str | None = None
    status: MetricStatus | None = None
    owner_id: uuid.UUID | None = None


@dataclass
class PerformanceValueListFilters:
    metric_definition_id: uuid.UUID | None = None
    subject_type: PerformanceSubjectType | None = None
    subject_id: uuid.UUID | None = None
    status: str | None = None
    period_start_from: date | None = None
    period_end_to: date | None = None


class PerformanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_definition_filters(self, query, filters: PerformanceDefinitionListFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    PerformanceMetricDefinition.name.ilike(pattern),
                    PerformanceMetricDefinition.code.ilike(pattern),
                    PerformanceMetricDefinition.description.ilike(pattern),
                )
            )
        if filters.subject_type is not None:
            query = query.where(
                PerformanceMetricDefinition.subject_type == filters.subject_type.value
            )
        if filters.value_type is not None:
            query = query.where(PerformanceMetricDefinition.value_type == filters.value_type)
        if filters.status is not None:
            query = query.where(PerformanceMetricDefinition.status == filters.status.value)
        if filters.owner_id is not None:
            query = query.where(PerformanceMetricDefinition.owner_id == filters.owner_id)
        return query

    def _apply_value_filters(self, query, filters: PerformanceValueListFilters):
        if filters.metric_definition_id is not None:
            query = query.where(
                PerformanceMetricValue.metric_definition_id == filters.metric_definition_id
            )
        if filters.subject_type is not None:
            query = query.where(
                PerformanceMetricValue.subject_type == filters.subject_type.value
            )
        if filters.subject_id is not None:
            query = query.where(PerformanceMetricValue.subject_id == filters.subject_id)
        if filters.status is not None:
            query = query.where(PerformanceMetricValue.status == filters.status)
        if filters.period_start_from is not None:
            query = query.where(
                PerformanceMetricValue.period_start >= filters.period_start_from
            )
        if filters.period_end_to is not None:
            query = query.where(PerformanceMetricValue.period_end <= filters.period_end_to)
        return query

    async def list_definitions(
        self,
        *,
        filters: PerformanceDefinitionListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[PerformanceMetricDefinition], int]:
        base_query = select(PerformanceMetricDefinition)
        filtered_query = self._apply_definition_filters(base_query, filters)
        count_query = self._apply_definition_filters(
            select(func.count(PerformanceMetricDefinition.id)),
            filters,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(PerformanceMetricDefinition.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_definition_by_id(
        self,
        definition_id: uuid.UUID,
    ) -> PerformanceMetricDefinition | None:
        return await self._session.get(PerformanceMetricDefinition, definition_id)

    async def get_definition_by_code(self, code: str) -> PerformanceMetricDefinition | None:
        return await self._session.scalar(
            select(PerformanceMetricDefinition).where(PerformanceMetricDefinition.code == code)
        )

    async def create_definition(self, payload: dict[str, object]) -> PerformanceMetricDefinition:
        definition = PerformanceMetricDefinition(**payload)
        self._session.add(definition)
        await self._session.commit()
        await self._session.refresh(definition)
        return definition

    async def update_definition(
        self,
        definition: PerformanceMetricDefinition,
        payload: dict[str, object],
    ) -> PerformanceMetricDefinition:
        for field, value in payload.items():
            setattr(definition, field, value)
        await self._session.commit()
        await self._session.refresh(definition)
        return definition

    async def delete_definition(self, definition: PerformanceMetricDefinition) -> None:
        await self._session.delete(definition)
        await self._session.commit()

    async def list_values(
        self,
        *,
        filters: PerformanceValueListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[PerformanceMetricValue], int]:
        base_query = select(PerformanceMetricValue)
        filtered_query = self._apply_value_filters(base_query, filters)
        count_query = self._apply_value_filters(
            select(func.count(PerformanceMetricValue.id)),
            filters,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(
                PerformanceMetricValue.period_end.desc().nullslast(),
                PerformanceMetricValue.updated_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def list_values_for_subject(
        self,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[PerformanceMetricValue], int]:
        filters = PerformanceValueListFilters(
            subject_type=subject_type,
            subject_id=subject_id,
        )
        return await self.list_values(filters=filters, offset=offset, limit=limit)

    async def get_value_by_id(self, value_id: uuid.UUID) -> PerformanceMetricValue | None:
        return await self._session.get(PerformanceMetricValue, value_id)

    async def get_latest_value(
        self,
        metric_definition_id: uuid.UUID,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
    ) -> PerformanceMetricValue | None:
        result = await self._session.scalars(
            select(PerformanceMetricValue)
            .where(
                PerformanceMetricValue.metric_definition_id == metric_definition_id,
                PerformanceMetricValue.subject_type == subject_type.value,
                PerformanceMetricValue.subject_id == subject_id,
            )
            .order_by(
                PerformanceMetricValue.period_end.desc().nullslast(),
                PerformanceMetricValue.updated_at.desc(),
            )
            .limit(1)
        )
        return result.first()

    async def get_previous_value(
        self,
        metric_definition_id: uuid.UUID,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        before_period_start: date | None,
    ) -> PerformanceMetricValue | None:
        query = select(PerformanceMetricValue).where(
            PerformanceMetricValue.metric_definition_id == metric_definition_id,
            PerformanceMetricValue.subject_type == subject_type.value,
            PerformanceMetricValue.subject_id == subject_id,
        )
        if before_period_start is not None:
            query = query.where(
                or_(
                    PerformanceMetricValue.period_start < before_period_start,
                    and_(
                        PerformanceMetricValue.period_start.is_(None),
                        PerformanceMetricValue.period_end.is_not(None),
                        PerformanceMetricValue.period_end < before_period_start,
                    ),
                )
            )
        result = await self._session.scalars(
            query.order_by(
                PerformanceMetricValue.period_end.desc().nullslast(),
                PerformanceMetricValue.updated_at.desc(),
            ).limit(1)
        )
        return result.first()

    async def get_duplicate_value(
        self,
        metric_definition_id: uuid.UUID,
        subject_type: PerformanceSubjectType,
        subject_id: uuid.UUID,
        period_start: date | None,
        period_end: date | None,
        *,
        exclude_id: uuid.UUID | None = None,
    ) -> PerformanceMetricValue | None:
        query = select(PerformanceMetricValue).where(
            PerformanceMetricValue.metric_definition_id == metric_definition_id,
            PerformanceMetricValue.subject_type == subject_type.value,
            PerformanceMetricValue.subject_id == subject_id,
        )
        if period_start is None:
            query = query.where(PerformanceMetricValue.period_start.is_(None))
        else:
            query = query.where(PerformanceMetricValue.period_start == period_start)
        if period_end is None:
            query = query.where(PerformanceMetricValue.period_end.is_(None))
        else:
            query = query.where(PerformanceMetricValue.period_end == period_end)
        if exclude_id is not None:
            query = query.where(PerformanceMetricValue.id != exclude_id)
        return await self._session.scalar(query)

    async def create_value(self, payload: dict[str, object]) -> PerformanceMetricValue:
        value = PerformanceMetricValue(**payload)
        self._session.add(value)
        await self._session.commit()
        await self._session.refresh(value)
        return value

    async def update_value(
        self,
        value: PerformanceMetricValue,
        payload: dict[str, object],
    ) -> PerformanceMetricValue:
        for field, field_value in payload.items():
            setattr(value, field, field_value)
        await self._session.commit()
        await self._session.refresh(value)
        return value

    async def delete_value(self, value: PerformanceMetricValue) -> None:
        await self._session.delete(value)
        await self._session.commit()

    def _scorecard_subject_types(self, subject_type: PerformanceSubjectType) -> list[str]:
        if subject_type == PerformanceSubjectType.INTERNAL_PROJECT:
            return [
                PerformanceSubjectType.INTERNAL_PROJECT.value,
                PerformanceSubjectType.PROJECT.value,
            ]
        return [subject_type.value]

    async def get_scorecard_definitions(
        self,
        subject_type: PerformanceSubjectType,
    ) -> list[PerformanceMetricDefinition]:
        subject_types = self._scorecard_subject_types(subject_type)
        result = await self._session.scalars(
            select(PerformanceMetricDefinition)
            .where(
                PerformanceMetricDefinition.subject_type.in_(subject_types),
                PerformanceMetricDefinition.status == MetricStatus.ACTIVE.value,
            )
            .order_by(PerformanceMetricDefinition.name.asc())
        )
        return list(result.all())

    async def get_overview(self) -> dict[str, int]:
        definitions_total = int(
            await self._session.scalar(select(func.count(PerformanceMetricDefinition.id))) or 0
        )
        definitions_active = int(
            await self._session.scalar(
                select(func.count(PerformanceMetricDefinition.id)).where(
                    PerformanceMetricDefinition.status == MetricStatus.ACTIVE.value
                )
            )
            or 0
        )
        values_total = int(
            await self._session.scalar(select(func.count(PerformanceMetricValue.id))) or 0
        )
        scorecards_available = int(
            await self._session.scalar(
                select(
                    func.count(
                        func.distinct(
                            PerformanceMetricValue.subject_type,
                            PerformanceMetricValue.subject_id,
                        )
                    )
                )
            )
            or 0
        )

        async def count_by_subject(subject: PerformanceSubjectType) -> int:
            return int(
                await self._session.scalar(
                    select(func.count(PerformanceMetricValue.id)).where(
                        PerformanceMetricValue.subject_type == subject.value
                    )
                )
                or 0
            )

        return {
            "metric_definitions_total": definitions_total,
            "metric_definitions_active": definitions_active,
            "metric_values_total": values_total,
            "scorecards_available": scorecards_available,
            "people_metrics_count": await count_by_subject(PerformanceSubjectType.PERSON),
            "team_metrics_count": await count_by_subject(PerformanceSubjectType.TEAM),
            "capability_metrics_count": await count_by_subject(PerformanceSubjectType.CAPABILITY),
            "project_metrics_count": await count_by_subject(PerformanceSubjectType.PROJECT),
            "data_product_metrics_count": await count_by_subject(
                PerformanceSubjectType.DATA_PRODUCT
            ),
        }
