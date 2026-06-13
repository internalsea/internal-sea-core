import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import (
    ActivityAction,
    AutomationActionType,
    AutomationStatus,
    AutomationTargetType,
    AutomationTriggerType,
)
from app.models.automation import AutomationTrigger
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.automation.errors import (
    AutomationScheduleNotFoundError,
    AutomationTriggerNotFoundError,
    UnsupportedAutomationActionError,
)
from app.modules.automation.repository import (
    AutomationRepository,
    AutomationRunListFilters,
    AutomationScheduleListFilters,
    AutomationTriggerListFilters,
)
from app.modules.automation.runner import MVP_SAFE_ACTION_TYPES, AutomationRunner
from app.modules.automation.schemas import (
    AutomationOverview,
    AutomationRunListResponse,
    AutomationRunRead,
    AutomationRunRequest,
    AutomationRunResult,
    AutomationScheduleCreate,
    AutomationScheduleListItem,
    AutomationScheduleListResponse,
    AutomationScheduleRead,
    AutomationScheduleUpdate,
    AutomationTriggerCreate,
    AutomationTriggerListItem,
    AutomationTriggerListResponse,
    AutomationTriggerRead,
    AutomationTriggerUpdate,
    EntityAutomationsResponse,
)
from app.modules.automation.validators import (
    ensure_automation_target_supported,
    validate_automation_target_exists,
)
from app.worker.scheduler import calculate_next_run_at


def _serialize_payload(data: dict[str, Any]) -> dict[str, Any]:
    serialized: dict[str, Any] = {}
    for key, value in data.items():
        if hasattr(value, "value"):
            serialized[key] = value.value
        else:
            serialized[key] = value
    return serialized


def _target_to_activity_entity(target_type: AutomationTargetType) -> str | None:
    mapping = {
        AutomationTargetType.DATA_PRODUCT: "data_product",
        AutomationTargetType.WORK_ITEM: "work_item",
        AutomationTargetType.PROJECT: "project",
        AutomationTargetType.INTERNAL_PROJECT: "internal_project",
        AutomationTargetType.TEAM: "team",
        AutomationTargetType.CAPABILITY: "capability",
    }
    return mapping.get(target_type)


class AutomationService:
    def __init__(
        self,
        repository: AutomationRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._session = session
        self._runner = AutomationRunner(session, repository)

    async def list_schedules(
        self,
        *,
        search: str | None = None,
        frequency: str | None = None,
        is_active: bool | None = None,
        page: int,
        page_size: int,
    ) -> AutomationScheduleListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        filters = AutomationScheduleListFilters(
            search=search,
            frequency=frequency,
            is_active=is_active,
        )
        items, total = await self._repository.list_schedules(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return AutomationScheduleListResponse(
            items=[AutomationScheduleListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_schedule(self, schedule_id: uuid.UUID) -> AutomationScheduleRead:
        schedule = await self._repository.get_schedule_by_id(schedule_id)
        if schedule is None:
            raise AutomationScheduleNotFoundError(schedule_id)
        return AutomationScheduleRead.model_validate(schedule)

    async def create_schedule(
        self,
        payload: AutomationScheduleCreate,
        *,
        created_by_id: uuid.UUID | None = None,
    ) -> AutomationScheduleRead:
        data = _serialize_payload(payload.model_dump())
        data["created_by_id"] = created_by_id
        schedule = await self._repository.create_schedule(data)
        return AutomationScheduleRead.model_validate(schedule)

    async def update_schedule(
        self,
        schedule_id: uuid.UUID,
        payload: AutomationScheduleUpdate,
    ) -> AutomationScheduleRead:
        schedule = await self._repository.get_schedule_by_id(schedule_id)
        if schedule is None:
            raise AutomationScheduleNotFoundError(schedule_id)
        data = _serialize_payload(payload.model_dump(exclude_unset=True))
        if data.get("start_at") and data.get("end_at") and data["end_at"] < data["start_at"]:
            from app.core.errors import ValidationError

            raise ValidationError("end_at must not be before start_at")
        updated = await self._repository.update_schedule(schedule, data)
        return AutomationScheduleRead.model_validate(updated)

    async def delete_schedule(self, schedule_id: uuid.UUID) -> None:
        schedule = await self._repository.get_schedule_by_id(schedule_id)
        if schedule is None:
            raise AutomationScheduleNotFoundError(schedule_id)
        await self._repository.delete_schedule(schedule)

    async def list_triggers(
        self,
        *,
        search: str | None = None,
        status: str | None = None,
        trigger_type: str | None = None,
        action_type: str | None = None,
        target_type: str | None = None,
        target_id: uuid.UUID | None = None,
        schedule_id: uuid.UUID | None = None,
        page: int,
        page_size: int,
    ) -> AutomationTriggerListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        filters = AutomationTriggerListFilters(
            search=search,
            status=status,
            trigger_type=trigger_type,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            schedule_id=schedule_id,
        )
        items, total = await self._repository.list_triggers(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return AutomationTriggerListResponse(
            items=[AutomationTriggerListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_trigger(self, trigger_id: uuid.UUID) -> AutomationTriggerRead:
        trigger = await self._repository.get_trigger_by_id(trigger_id)
        if trigger is None:
            raise AutomationTriggerNotFoundError(trigger_id)
        return AutomationTriggerRead.model_validate(trigger)

    async def _validate_trigger_payload(
        self,
        *,
        target_type: AutomationTargetType | None,
        target_id: uuid.UUID | None,
        schedule_id: uuid.UUID | None,
        trigger_type: AutomationTriggerType | None,
        action_type: AutomationActionType | None,
    ) -> None:
        if target_type is not None and target_id is not None:
            await ensure_automation_target_supported(target_type)
            await validate_automation_target_exists(self._session, target_type, target_id)
        if schedule_id is not None:
            schedule = await self._repository.get_schedule_by_id(schedule_id)
            if schedule is None:
                raise AutomationScheduleNotFoundError(schedule_id)
        if trigger_type == AutomationTriggerType.SCHEDULE and schedule_id is None:
            from app.core.errors import ValidationError

            raise ValidationError("schedule_id is required for schedule triggers")
        if action_type is not None and action_type not in AutomationActionType:
            raise UnsupportedAutomationActionError(str(action_type))

    async def create_trigger(
        self,
        payload: AutomationTriggerCreate,
        *,
        created_by_id: uuid.UUID | None = None,
    ) -> AutomationTriggerRead:
        await self._validate_trigger_payload(
            target_type=payload.target_type,
            target_id=payload.target_id,
            schedule_id=payload.schedule_id,
            trigger_type=payload.trigger_type,
            action_type=payload.action_type,
        )
        data = _serialize_payload(payload.model_dump())
        data["created_by_id"] = created_by_id
        if data.get("next_run_at") is None and data.get("status") == AutomationStatus.ACTIVE.value:
            data["next_run_at"] = await self._resolve_initial_next_run_at(
                schedule_id=data.get("schedule_id"),
                trigger_type=data.get("trigger_type"),
            )
        trigger = await self._repository.create_trigger(data)
        await self._record_trigger_activity(
            trigger,
            title="Automation trigger created",
            description=trigger.name,
        )
        return AutomationTriggerRead.model_validate(trigger)

    async def update_trigger(
        self,
        trigger_id: uuid.UUID,
        payload: AutomationTriggerUpdate,
    ) -> AutomationTriggerRead:
        trigger = await self._repository.get_trigger_by_id(trigger_id)
        if trigger is None:
            raise AutomationTriggerNotFoundError(trigger_id)

        update_data = payload.model_dump(exclude_unset=True)
        merged_target_type = update_data.get("target_type", trigger.target_type)
        merged_target_id = update_data.get("target_id", trigger.target_id)
        merged_schedule_id = update_data.get("schedule_id", trigger.schedule_id)
        merged_trigger_type = update_data.get("trigger_type", trigger.trigger_type)
        merged_action_type = update_data.get("action_type", trigger.action_type)

        target_type_enum = AutomationTargetType(merged_target_type) if merged_target_type else None
        trigger_type_enum = AutomationTriggerType(merged_trigger_type)
        action_type_enum = AutomationActionType(merged_action_type)

        await self._validate_trigger_payload(
            target_type=target_type_enum,
            target_id=merged_target_id,
            schedule_id=merged_schedule_id,
            trigger_type=trigger_type_enum,
            action_type=action_type_enum,
        )

        data = _serialize_payload(update_data)
        if (
            data.get("next_run_at") is None
            and data.get("status", trigger.status) == AutomationStatus.ACTIVE.value
            and trigger.next_run_at is None
            and (data.get("schedule_id") or trigger.schedule_id)
        ):
            data["next_run_at"] = await self._resolve_initial_next_run_at(
                schedule_id=data.get("schedule_id", trigger.schedule_id),
                trigger_type=data.get("trigger_type", trigger.trigger_type),
            )
        updated = await self._repository.update_trigger(trigger, data)
        await self._record_trigger_activity(
            updated,
            title="Automation trigger updated",
            description=updated.name,
        )
        return AutomationTriggerRead.model_validate(updated)

    async def delete_trigger(self, trigger_id: uuid.UUID) -> None:
        trigger = await self._repository.get_trigger_by_id(trigger_id)
        if trigger is None:
            raise AutomationTriggerNotFoundError(trigger_id)
        await self._repository.delete_trigger(trigger)

    async def get_entity_automations(
        self,
        target_type: AutomationTargetType,
        target_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> EntityAutomationsResponse:
        await ensure_automation_target_supported(target_type)
        await validate_automation_target_exists(self._session, target_type, target_id)
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_triggers_for_target(
            target_type.value,
            target_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return EntityAutomationsResponse(
            target_type=target_type,
            target_id=target_id,
            triggers=[AutomationTriggerListItem.model_validate(item) for item in items],
            total=total,
        )

    async def list_runs(
        self,
        *,
        trigger_id: uuid.UUID | None = None,
        status: str | None = None,
        target_type: str | None = None,
        target_id: uuid.UUID | None = None,
        action_type: str | None = None,
        page: int,
        page_size: int,
    ) -> AutomationRunListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        filters = AutomationRunListFilters(
            trigger_id=trigger_id,
            status=status,
            target_type=target_type,
            target_id=target_id,
            action_type=action_type,
        )
        items, total = await self._repository.list_runs(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return AutomationRunListResponse(
            items=[AutomationRunRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def list_trigger_runs(
        self,
        trigger_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> AutomationRunListResponse:
        trigger = await self._repository.get_trigger_by_id(trigger_id)
        if trigger is None:
            raise AutomationTriggerNotFoundError(trigger_id)
        return await self.list_runs(trigger_id=trigger_id, page=page, page_size=page_size)

    async def run_trigger(
        self,
        trigger_id: uuid.UUID,
        payload: AutomationRunRequest,
        *,
        executed_by_id: uuid.UUID | None,
    ) -> AutomationRunResult:
        trigger = await self._repository.get_trigger_by_id(trigger_id)
        if trigger is None:
            raise AutomationTriggerNotFoundError(trigger_id)

        if not payload.simulate:
            action_type = AutomationActionType(trigger.action_type)
            if action_type not in MVP_SAFE_ACTION_TYPES:
                from app.modules.automation.errors import AutomationRunError

                raise AutomationRunError("Action type is not implemented in MVP.")

        result = await self._runner.run_trigger(
            trigger,
            executed_by_id=executed_by_id,
            simulate=payload.simulate,
        )

        mode = "simulated" if payload.simulate else result.run.status
        await self._record_trigger_activity(
            trigger,
            title="Automation trigger run",
            description=f"Manual run ({mode}): {trigger.name}",
        )
        return result

    async def get_overview(self) -> AutomationOverview:
        data = await self._repository.get_overview()
        return AutomationOverview.model_validate(data)

    async def _resolve_initial_next_run_at(
        self,
        *,
        schedule_id: uuid.UUID | None,
        trigger_type: str | None,
    ) -> datetime | None:
        from app.domain.enums import AutomationTriggerType

        if trigger_type != AutomationTriggerType.SCHEDULE.value or schedule_id is None:
            return None
        schedule = await self._repository.get_schedule_by_id(schedule_id)
        if schedule is None:
            return None
        if schedule.next_run_at is not None:
            return schedule.next_run_at
        now = datetime.now(UTC)
        if schedule.start_at and schedule.start_at > now:
            return schedule.start_at
        return calculate_next_run_at(schedule, now) or now

    async def _record_trigger_activity(
        self,
        trigger: AutomationTrigger,
        *,
        title: str,
        description: str,
    ) -> None:
        if not trigger.target_type or not trigger.target_id:
            return
        try:
            target_type = AutomationTargetType(trigger.target_type)
        except ValueError:
            return
        entity_type = _target_to_activity_entity(target_type)
        if entity_type is None:
            return
        from app.domain.enums import ActivityEntityType

        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=ActivityEntityType(entity_type),
                entity_id=trigger.target_id,
                action=ActivityAction.UPDATED,
                title=title,
                description=description,
            )
        )
