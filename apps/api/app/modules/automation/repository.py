import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import get_model
from app.domain.enums import AutomationRunStatus, AutomationStatus
from app.models.automation import AutomationRun, AutomationSchedule, AutomationTrigger


@dataclass
class AutomationScheduleListFilters:
    search: str | None = None
    frequency: str | None = None
    is_active: bool | None = None


@dataclass
class AutomationTriggerListFilters:
    search: str | None = None
    status: str | None = None
    trigger_type: str | None = None
    action_type: str | None = None
    target_type: str | None = None
    target_id: uuid.UUID | None = None
    schedule_id: uuid.UUID | None = None


@dataclass
class AutomationRunListFilters:
    trigger_id: uuid.UUID | None = None
    status: str | None = None
    target_type: str | None = None
    target_id: uuid.UUID | None = None
    action_type: str | None = None


class AutomationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_schedule_filters(
        self, query: Any, filters: AutomationScheduleListFilters
    ) -> Any:
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    AutomationSchedule.name.ilike(pattern),
                    AutomationSchedule.description.ilike(pattern),
                )
            )
        if filters.frequency:
            query = query.where(AutomationSchedule.frequency == filters.frequency)
        if filters.is_active is not None:
            query = query.where(AutomationSchedule.is_active.is_(filters.is_active))
        return query

    def _apply_trigger_filters(
        self, query: Any, filters: AutomationTriggerListFilters
    ) -> Any:
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    AutomationTrigger.name.ilike(pattern),
                    AutomationTrigger.description.ilike(pattern),
                )
            )
        if filters.status:
            query = query.where(AutomationTrigger.status == filters.status)
        if filters.trigger_type:
            query = query.where(AutomationTrigger.trigger_type == filters.trigger_type)
        if filters.action_type:
            query = query.where(AutomationTrigger.action_type == filters.action_type)
        if filters.target_type:
            query = query.where(AutomationTrigger.target_type == filters.target_type)
        if filters.target_id:
            query = query.where(AutomationTrigger.target_id == filters.target_id)
        if filters.schedule_id:
            query = query.where(AutomationTrigger.schedule_id == filters.schedule_id)
        return query

    def _apply_run_filters(self, query: Any, filters: AutomationRunListFilters) -> Any:
        if filters.trigger_id:
            query = query.where(AutomationRun.trigger_id == filters.trigger_id)
        if filters.status:
            query = query.where(AutomationRun.status == filters.status)
        if filters.target_type:
            query = query.where(AutomationRun.target_type == filters.target_type)
        if filters.target_id:
            query = query.where(AutomationRun.target_id == filters.target_id)
        if filters.action_type:
            query = query.where(AutomationRun.action_type == filters.action_type)
        return query

    async def list_schedules(
        self,
        *,
        filters: AutomationScheduleListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[AutomationSchedule], int]:
        base_query = select(AutomationSchedule)
        filtered_query = self._apply_schedule_filters(base_query, filters)
        count_query = self._apply_schedule_filters(
            select(func.count(AutomationSchedule.id)),
            filters,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(
                AutomationSchedule.next_run_at.asc().nulls_last(),
                AutomationSchedule.updated_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_schedule_by_id(self, schedule_id: uuid.UUID) -> AutomationSchedule | None:
        return await get_model(self._session, AutomationSchedule, schedule_id)

    async def create_schedule(self, data: dict[str, object]) -> AutomationSchedule:
        schedule = AutomationSchedule(**data)
        self._session.add(schedule)
        await self._session.commit()
        await self._session.refresh(schedule)
        return schedule

    async def update_schedule(
        self,
        schedule: AutomationSchedule,
        data: dict[str, object],
    ) -> AutomationSchedule:
        for field, value in data.items():
            setattr(schedule, field, value)
        await self._session.commit()
        await self._session.refresh(schedule)
        return schedule

    async def delete_schedule(self, schedule: AutomationSchedule) -> None:
        await self._session.delete(schedule)
        await self._session.commit()

    async def list_triggers(
        self,
        *,
        filters: AutomationTriggerListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[AutomationTrigger], int]:
        base_query = select(AutomationTrigger)
        filtered_query = self._apply_trigger_filters(base_query, filters)
        count_query = self._apply_trigger_filters(
            select(func.count(AutomationTrigger.id)),
            filters,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(
                AutomationTrigger.next_run_at.asc().nulls_last(),
                AutomationTrigger.updated_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def list_triggers_for_target(
        self,
        target_type: str,
        target_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[AutomationTrigger], int]:
        filters = AutomationTriggerListFilters(target_type=target_type, target_id=target_id)
        return await self.list_triggers(filters=filters, offset=offset, limit=limit)

    async def get_trigger_by_id(self, trigger_id: uuid.UUID) -> AutomationTrigger | None:
        return await get_model(self._session, AutomationTrigger, trigger_id)

    async def create_trigger(self, data: dict[str, object]) -> AutomationTrigger:
        trigger = AutomationTrigger(**data)
        self._session.add(trigger)
        await self._session.commit()
        await self._session.refresh(trigger)
        return trigger

    async def update_trigger(
        self,
        trigger: AutomationTrigger,
        data: dict[str, object],
    ) -> AutomationTrigger:
        for field, value in data.items():
            setattr(trigger, field, value)
        await self._session.commit()
        await self._session.refresh(trigger)
        return trigger

    async def delete_trigger(self, trigger: AutomationTrigger) -> None:
        await self._session.delete(trigger)
        await self._session.commit()

    async def list_runs(
        self,
        *,
        filters: AutomationRunListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[AutomationRun], int]:
        base_query = select(AutomationRun)
        filtered_query = self._apply_run_filters(base_query, filters)
        count_query = self._apply_run_filters(
            select(func.count(AutomationRun.id)),
            filters,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(AutomationRun.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def list_runs_for_trigger(
        self,
        trigger_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[AutomationRun], int]:
        filters = AutomationRunListFilters(trigger_id=trigger_id)
        return await self.list_runs(filters=filters, offset=offset, limit=limit)

    async def get_run_by_id(self, run_id: uuid.UUID) -> AutomationRun | None:
        return await get_model(self._session, AutomationRun, run_id)

    async def create_run(self, data: dict[str, object]) -> AutomationRun:
        run = AutomationRun(**data)
        self._session.add(run)
        await self._session.commit()
        await self._session.refresh(run)
        return run

    async def update_run(self, run: AutomationRun, data: dict[str, object]) -> AutomationRun:
        for field, value in data.items():
            setattr(run, field, value)
        await self._session.commit()
        await self._session.refresh(run)
        return run

    async def touch_trigger_run_times(
        self,
        trigger: AutomationTrigger,
        *,
        run_at: datetime | None = None,
    ) -> AutomationTrigger:
        now = run_at or datetime.now(UTC)
        trigger.last_run_at = now
        await self._session.commit()
        await self._session.refresh(trigger)
        return trigger

    async def touch_schedule_run_time(
        self,
        schedule: AutomationSchedule,
        *,
        run_at: datetime | None = None,
    ) -> AutomationSchedule:
        now = run_at or datetime.now(UTC)
        schedule.last_run_at = now
        await self._session.commit()
        await self._session.refresh(schedule)
        return schedule

    async def get_overview(self) -> dict[str, int]:
        schedules_total = int(
            await self._session.scalar(select(func.count(AutomationSchedule.id))) or 0
        )
        schedules_active = int(
            await self._session.scalar(
                select(func.count(AutomationSchedule.id)).where(
                    AutomationSchedule.is_active.is_(True)
                )
            )
            or 0
        )
        triggers_total = int(
            await self._session.scalar(select(func.count(AutomationTrigger.id))) or 0
        )
        triggers_active = int(
            await self._session.scalar(
                select(func.count(AutomationTrigger.id)).where(
                    AutomationTrigger.status == AutomationStatus.ACTIVE.value
                )
            )
            or 0
        )
        triggers_paused = int(
            await self._session.scalar(
                select(func.count(AutomationTrigger.id)).where(
                    AutomationTrigger.status == AutomationStatus.PAUSED.value
                )
            )
            or 0
        )
        runs_total = int(await self._session.scalar(select(func.count(AutomationRun.id))) or 0)
        runs_succeeded = int(
            await self._session.scalar(
                select(func.count(AutomationRun.id)).where(
                    AutomationRun.status == AutomationRunStatus.SUCCEEDED.value
                )
            )
            or 0
        )
        runs_failed = int(
            await self._session.scalar(
                select(func.count(AutomationRun.id)).where(
                    AutomationRun.status == AutomationRunStatus.FAILED.value
                )
            )
            or 0
        )
        runs_simulated = int(
            await self._session.scalar(
                select(func.count(AutomationRun.id)).where(
                    AutomationRun.status == AutomationRunStatus.SIMULATED.value
                )
            )
            or 0
        )
        next_runs_count = int(
            await self._session.scalar(
                select(func.count(AutomationTrigger.id)).where(
                    AutomationTrigger.next_run_at.is_not(None),
                    AutomationTrigger.status == AutomationStatus.ACTIVE.value,
                )
            )
            or 0
        )
        return {
            "schedules_total": schedules_total,
            "schedules_active": schedules_active,
            "triggers_total": triggers_total,
            "triggers_active": triggers_active,
            "triggers_paused": triggers_paused,
            "runs_total": runs_total,
            "runs_succeeded": runs_succeeded,
            "runs_failed": runs_failed,
            "runs_simulated": runs_simulated,
            "next_runs_count": next_runs_count,
        }
