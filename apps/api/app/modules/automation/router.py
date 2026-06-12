import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import AutomationTargetType
from app.modules.activity.dependencies import get_activity_service
from app.modules.activity.service import ActivityService
from app.modules.automation.repository import AutomationRepository
from app.modules.automation.schemas import (
    AutomationOverview,
    AutomationRunListResponse,
    AutomationRunRequest,
    AutomationRunResult,
    AutomationScheduleCreate,
    AutomationScheduleListResponse,
    AutomationScheduleRead,
    AutomationScheduleUpdate,
    AutomationTriggerCreate,
    AutomationTriggerListResponse,
    AutomationTriggerRead,
    AutomationTriggerUpdate,
    EntityAutomationsResponse,
)
from app.modules.automation.service import AutomationService

router = APIRouter(prefix="/automation", tags=["Automation"])


def get_automation_service(
    db: AsyncSession = Depends(get_db),
    activity_service: ActivityService = Depends(get_activity_service),
) -> AutomationService:
    return AutomationService(AutomationRepository(db), activity_service, db)


@router.get("/overview", response_model=AutomationOverview)
async def get_automation_overview(
    _user: ViewerUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationOverview:
    return await service.get_overview()


@router.get("/schedules", response_model=AutomationScheduleListResponse)
async def list_schedules(
    _user: ViewerUser,
    search: str | None = None,
    frequency: str | None = None,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: AutomationService = Depends(get_automation_service),
) -> AutomationScheduleListResponse:
    return await service.list_schedules(
        search=search,
        frequency=frequency,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@router.post("/schedules", response_model=AutomationScheduleRead, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    payload: AutomationScheduleCreate,
    user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationScheduleRead:
    return await service.create_schedule(payload, created_by_id=user.id)


@router.get("/schedules/{schedule_id}", response_model=AutomationScheduleRead)
async def get_schedule(
    schedule_id: uuid.UUID,
    _user: ViewerUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationScheduleRead:
    return await service.get_schedule(schedule_id)


@router.patch("/schedules/{schedule_id}", response_model=AutomationScheduleRead)
async def update_schedule(
    schedule_id: uuid.UUID,
    payload: AutomationScheduleUpdate,
    _user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationScheduleRead:
    return await service.update_schedule(schedule_id, payload)


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: uuid.UUID,
    _user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> None:
    await service.delete_schedule(schedule_id)


@router.get("/triggers", response_model=AutomationTriggerListResponse)
async def list_triggers(
    _user: ViewerUser,
    search: str | None = None,
    status: str | None = None,
    trigger_type: str | None = None,
    action_type: str | None = None,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    schedule_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: AutomationService = Depends(get_automation_service),
) -> AutomationTriggerListResponse:
    return await service.list_triggers(
        search=search,
        status=status,
        trigger_type=trigger_type,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        schedule_id=schedule_id,
        page=page,
        page_size=page_size,
    )


@router.post("/triggers", response_model=AutomationTriggerRead, status_code=status.HTTP_201_CREATED)
async def create_trigger(
    payload: AutomationTriggerCreate,
    user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationTriggerRead:
    return await service.create_trigger(payload, created_by_id=user.id)


@router.get("/entity/{target_type}/{target_id}", response_model=EntityAutomationsResponse)
async def get_entity_automations(
    target_type: AutomationTargetType,
    target_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: AutomationService = Depends(get_automation_service),
) -> EntityAutomationsResponse:
    return await service.get_entity_automations(
        target_type,
        target_id,
        page=page,
        page_size=page_size,
    )


@router.get("/triggers/{trigger_id}", response_model=AutomationTriggerRead)
async def get_trigger(
    trigger_id: uuid.UUID,
    _user: ViewerUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationTriggerRead:
    return await service.get_trigger(trigger_id)


@router.patch("/triggers/{trigger_id}", response_model=AutomationTriggerRead)
async def update_trigger(
    trigger_id: uuid.UUID,
    payload: AutomationTriggerUpdate,
    _user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationTriggerRead:
    return await service.update_trigger(trigger_id, payload)


@router.delete("/triggers/{trigger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trigger(
    trigger_id: uuid.UUID,
    _user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> None:
    await service.delete_trigger(trigger_id)


@router.get("/runs", response_model=AutomationRunListResponse)
async def list_runs(
    _user: ViewerUser,
    trigger_id: uuid.UUID | None = None,
    status: str | None = None,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    action_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: AutomationService = Depends(get_automation_service),
) -> AutomationRunListResponse:
    return await service.list_runs(
        trigger_id=trigger_id,
        status=status,
        target_type=target_type,
        target_id=target_id,
        action_type=action_type,
        page=page,
        page_size=page_size,
    )


@router.get("/triggers/{trigger_id}/runs", response_model=AutomationRunListResponse)
async def list_trigger_runs(
    trigger_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: AutomationService = Depends(get_automation_service),
) -> AutomationRunListResponse:
    return await service.list_trigger_runs(trigger_id, page=page, page_size=page_size)


@router.post("/triggers/{trigger_id}/run", response_model=AutomationRunResult)
async def run_trigger(
    trigger_id: uuid.UUID,
    payload: AutomationRunRequest,
    user: EditorUser,
    service: AutomationService = Depends(get_automation_service),
) -> AutomationRunResult:
    return await service.run_trigger(
        trigger_id,
        payload,
        executed_by_id=user.id,
    )
