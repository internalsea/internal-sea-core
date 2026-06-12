import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import (
    NotificationChannelStatus,
    NotificationChannelType,
    NotificationEventType,
    NotificationMessageStatus,
    NotificationPriority,
    NotificationTemplateStatus,
)
from app.modules.activity.dependencies import build_activity_service
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import (
    EntityNotificationsResponse,
    NotificationChannelCreate,
    NotificationChannelFilters,
    NotificationChannelListResponse,
    NotificationChannelRead,
    NotificationChannelUpdate,
    NotificationDeliveryAttemptListResponse,
    NotificationMessageCreate,
    NotificationMessageFilters,
    NotificationMessageListResponse,
    NotificationMessageRead,
    NotificationMessageUpdate,
    NotificationOverview,
    NotificationPreferenceCreate,
    NotificationPreferenceRead,
    NotificationPreferenceUpdate,
    NotificationRenderRequest,
    NotificationRenderResult,
    NotificationSendRequest,
    NotificationSendResult,
    NotificationTemplateCreate,
    NotificationTemplateFilters,
    NotificationTemplateListResponse,
    NotificationTemplateRead,
    NotificationTemplateUpdate,
)
from app.modules.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(
        NotificationRepository(db),
        build_activity_service(db),
        db,
    )


@router.get("/overview", response_model=NotificationOverview)
async def get_notification_overview(
    _user: ViewerUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationOverview:
    return await service.get_overview()


@router.get("/channels", response_model=NotificationChannelListResponse)
async def list_channels(
    _user: ViewerUser,
    search: str | None = None,
    channel_type: NotificationChannelType | None = None,
    status: NotificationChannelStatus | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationChannelListResponse:
    filters = NotificationChannelFilters(
        search=search,
        channel_type=channel_type,
        status=status,
    )
    return await service.list_channels(filters=filters, page=page, page_size=page_size)


@router.post("/channels", response_model=NotificationChannelRead, status_code=status.HTTP_201_CREATED)
async def create_channel(
    payload: NotificationChannelCreate,
    user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationChannelRead:
    return await service.create_channel(payload, created_by_id=user.id)


@router.get("/channels/{channel_id}", response_model=NotificationChannelRead)
async def get_channel(
    channel_id: uuid.UUID,
    _user: ViewerUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationChannelRead:
    return await service.get_channel(channel_id)


@router.patch("/channels/{channel_id}", response_model=NotificationChannelRead)
async def update_channel(
    channel_id: uuid.UUID,
    payload: NotificationChannelUpdate,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationChannelRead:
    return await service.update_channel(channel_id, payload)


@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: uuid.UUID,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> None:
    await service.delete_channel(channel_id)


@router.get("/templates", response_model=NotificationTemplateListResponse)
async def list_templates(
    _user: ViewerUser,
    search: str | None = None,
    status: NotificationTemplateStatus | None = None,
    event_type: NotificationEventType | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationTemplateListResponse:
    filters = NotificationTemplateFilters(
        search=search,
        status=status,
        event_type=event_type,
    )
    return await service.list_templates(filters=filters, page=page, page_size=page_size)


@router.post(
    "/templates",
    response_model=NotificationTemplateRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    payload: NotificationTemplateCreate,
    user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationTemplateRead:
    return await service.create_template(payload, created_by_id=user.id)


@router.get("/templates/{template_id}", response_model=NotificationTemplateRead)
async def get_template(
    template_id: uuid.UUID,
    _user: ViewerUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationTemplateRead:
    return await service.get_template(template_id)


@router.patch("/templates/{template_id}", response_model=NotificationTemplateRead)
async def update_template(
    template_id: uuid.UUID,
    payload: NotificationTemplateUpdate,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationTemplateRead:
    return await service.update_template(template_id, payload)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: uuid.UUID,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> None:
    await service.delete_template(template_id)


@router.post("/templates/render", response_model=NotificationRenderResult)
async def render_template(
    payload: NotificationRenderRequest,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationRenderResult:
    return await service.render_template(payload)


@router.get("/preferences", response_model=list[NotificationPreferenceRead])
async def list_preferences(
    _user: ViewerUser,
    user_id: uuid.UUID | None = None,
    person_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> list[NotificationPreferenceRead]:
    return await service.list_preferences(
        user_id=user_id,
        person_id=person_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/preferences",
    response_model=NotificationPreferenceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_preference(
    payload: NotificationPreferenceCreate,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationPreferenceRead:
    return await service.create_preference(payload)


@router.patch("/preferences/{preference_id}", response_model=NotificationPreferenceRead)
async def update_preference(
    preference_id: uuid.UUID,
    payload: NotificationPreferenceUpdate,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationPreferenceRead:
    return await service.update_preference(preference_id, payload)


@router.delete("/preferences/{preference_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preference(
    preference_id: uuid.UUID,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> None:
    await service.delete_preference(preference_id)


@router.get("/messages", response_model=NotificationMessageListResponse)
async def list_messages(
    _user: ViewerUser,
    search: str | None = None,
    status: NotificationMessageStatus | None = None,
    priority: NotificationPriority | None = None,
    event_type: NotificationEventType | None = None,
    channel_id: uuid.UUID | None = None,
    template_id: uuid.UUID | None = None,
    entity_type: str | None = None,
    entity_id: uuid.UUID | None = None,
    automation_run_id: uuid.UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationMessageListResponse:
    filters = NotificationMessageFilters(
        search=search,
        status=status,
        priority=priority,
        event_type=event_type,
        channel_id=channel_id,
        template_id=template_id,
        entity_type=entity_type,
        entity_id=entity_id,
        automation_run_id=automation_run_id,
    )
    return await service.list_messages(filters=filters, page=page, page_size=page_size)


@router.post("/messages", response_model=NotificationMessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    payload: NotificationMessageCreate,
    user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationMessageRead:
    return await service.create_message(payload, created_by_id=user.id)


@router.get("/messages/{message_id}", response_model=NotificationMessageRead)
async def get_message(
    message_id: uuid.UUID,
    _user: ViewerUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationMessageRead:
    return await service.get_message(message_id)


@router.patch("/messages/{message_id}", response_model=NotificationMessageRead)
async def update_message(
    message_id: uuid.UUID,
    payload: NotificationMessageUpdate,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationMessageRead:
    return await service.update_message(message_id, payload)


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: uuid.UUID,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> None:
    await service.delete_message(message_id)


@router.post("/messages/{message_id}/send", response_model=NotificationSendResult)
async def send_message(
    message_id: uuid.UUID,
    payload: NotificationSendRequest,
    user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationSendResult:
    return await service.send_message(message_id, payload, created_by_id=user.id)


@router.post("/messages/{message_id}/queue", response_model=NotificationMessageRead)
async def queue_message(
    message_id: uuid.UUID,
    _user: EditorUser,
    service: NotificationService = Depends(get_notification_service),
) -> NotificationMessageRead:
    return await service.queue_message(message_id)


@router.get(
    "/messages/{message_id}/delivery-attempts",
    response_model=NotificationDeliveryAttemptListResponse,
)
async def list_message_delivery_attempts(
    message_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationDeliveryAttemptListResponse:
    return await service.list_delivery_attempts(
        message_id=message_id,
        page=page,
        page_size=page_size,
    )


@router.get("/delivery-attempts", response_model=NotificationDeliveryAttemptListResponse)
async def list_delivery_attempts(
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationDeliveryAttemptListResponse:
    return await service.list_delivery_attempts(
        message_id=None,
        page=page,
        page_size=page_size,
    )


@router.get("/entity/{entity_type}/{entity_id}", response_model=EntityNotificationsResponse)
async def get_entity_notifications(
    entity_type: str,
    entity_id: uuid.UUID,
    _user: ViewerUser,
    service: NotificationService = Depends(get_notification_service),
) -> EntityNotificationsResponse:
    return await service.get_entity_notifications(entity_type, entity_id)
