import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, NotificationMessageStatus
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.notifications.dispatcher import NotificationDispatcher
from app.modules.notifications.errors import (
    NotificationChannelNotFoundError,
    NotificationConflictError,
    NotificationMessageNotFoundError,
    NotificationPreferenceNotFoundError,
    NotificationTemplateNotFoundError,
)
from app.modules.notifications.renderer import DEFAULT_CONTEXT_KEYS, render_notification_template
from app.modules.notifications.repository import (
    NotificationPreferenceListFilters,
    NotificationRepository,
)
from app.modules.notifications.schemas import (
    EntityNotificationsResponse,
    NotificationChannelCreate,
    NotificationChannelFilters,
    NotificationChannelListItem,
    NotificationChannelListResponse,
    NotificationChannelRead,
    NotificationChannelUpdate,
    NotificationDeliveryAttemptListResponse,
    NotificationDeliveryAttemptRead,
    NotificationMessageCreate,
    NotificationMessageFilters,
    NotificationMessageListItem,
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
    NotificationTemplateListItem,
    NotificationTemplateListResponse,
    NotificationTemplateRead,
    NotificationTemplateUpdate,
)
from app.modules.notifications.validators import (
    validate_channel_exists,
    validate_notification_entity_exists,
    validate_user_or_person_exists,
)


class NotificationService:
    def __init__(
        self,
        repository: NotificationRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._session = session
        self._dispatcher = NotificationDispatcher()

    def _enum_value(self, value) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    def _build_default_context(self, context: dict[str, Any] | None) -> dict[str, Any]:
        merged = {key: "" for key in DEFAULT_CONTEXT_KEYS}
        merged["app_name"] = get_settings().app_name
        if context:
            merged.update(context)
        return merged

    def _to_activity_entity_type(self, entity_type: str) -> ActivityEntityType | None:
        try:
            return ActivityEntityType(entity_type)
        except ValueError:
            return None

    async def _record_notification_activity(
        self,
        message: Any,
        *,
        simulated: bool,
    ) -> None:
        if not message.entity_type or not message.entity_id:
            return
        activity_entity = self._to_activity_entity_type(message.entity_type)
        if activity_entity is None:
            return
        title = "Notification simulated" if simulated else "Notification sent"
        description = message.subject or message.event_type
        await self._activity.create(
            ActivityEventCreateInternal(
                entity_type=activity_entity,
                entity_id=message.entity_id,
                action=ActivityAction.UPDATED,
                actor_id=message.created_by_id,
                title=title,
                description=description,
                details={"notification_message_id": str(message.id)},
            )
        )

    async def get_overview(self) -> NotificationOverview:
        data = await self._repository.get_overview()
        return NotificationOverview.model_validate(data)

    async def list_channels(
        self,
        *,
        filters: NotificationChannelFilters,
        page: int,
        page_size: int,
    ) -> NotificationChannelListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_channels(
            filters=filters,
            offset=offset,
            limit=page_size,
        )
        return NotificationChannelListResponse(
            items=[NotificationChannelListItem.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_channel(self, channel_id: uuid.UUID) -> NotificationChannelRead:
        channel = await self._repository.get_channel_by_id(channel_id)
        if channel is None:
            raise NotificationChannelNotFoundError(channel_id)
        return NotificationChannelRead.model_validate(channel)

    async def create_channel(
        self,
        payload: NotificationChannelCreate,
        *,
        created_by_id: uuid.UUID | None,
    ) -> NotificationChannelRead:
        existing = await self._repository.get_channel_by_name(payload.name)
        if existing is not None:
            raise NotificationConflictError(f"Channel name already exists: {payload.name}")
        data = payload.model_dump()
        data["channel_type"] = self._enum_value(payload.channel_type)
        data["status"] = self._enum_value(payload.status)
        data["created_by_id"] = created_by_id
        channel = await self._repository.create_channel(data)
        return NotificationChannelRead.model_validate(channel)

    async def update_channel(
        self,
        channel_id: uuid.UUID,
        payload: NotificationChannelUpdate,
    ) -> NotificationChannelRead:
        channel = await self._repository.get_channel_by_id(channel_id)
        if channel is None:
            raise NotificationChannelNotFoundError(channel_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            existing = await self._repository.get_channel_by_name(data["name"])
            if existing is not None and existing.id != channel_id:
                raise NotificationConflictError(f"Channel name already exists: {data['name']}")
        if "channel_type" in data:
            data["channel_type"] = self._enum_value(data["channel_type"])
        if "status" in data:
            data["status"] = self._enum_value(data["status"])
        channel = await self._repository.update_channel(channel, data)
        return NotificationChannelRead.model_validate(channel)

    async def delete_channel(self, channel_id: uuid.UUID) -> None:
        channel = await self._repository.get_channel_by_id(channel_id)
        if channel is None:
            raise NotificationChannelNotFoundError(channel_id)
        await self._repository.delete_channel(channel)

    async def list_templates(
        self,
        *,
        filters: NotificationTemplateFilters,
        page: int,
        page_size: int,
    ) -> NotificationTemplateListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_templates(
            filters=filters,
            offset=offset,
            limit=page_size,
        )
        return NotificationTemplateListResponse(
            items=[NotificationTemplateListItem.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_template(self, template_id: uuid.UUID) -> NotificationTemplateRead:
        template = await self._repository.get_template_by_id(template_id)
        if template is None:
            raise NotificationTemplateNotFoundError(template_id)
        return NotificationTemplateRead.model_validate(template)

    async def create_template(
        self,
        payload: NotificationTemplateCreate,
        *,
        created_by_id: uuid.UUID | None,
    ) -> NotificationTemplateRead:
        existing = await self._repository.get_template_by_name(payload.name)
        if existing is not None:
            raise NotificationConflictError(f"Template name already exists: {payload.name}")
        data = payload.model_dump()
        data["status"] = self._enum_value(payload.status)
        data["event_type"] = self._enum_value(payload.event_type)
        data["created_by_id"] = created_by_id
        template = await self._repository.create_template(data)
        return NotificationTemplateRead.model_validate(template)

    async def update_template(
        self,
        template_id: uuid.UUID,
        payload: NotificationTemplateUpdate,
    ) -> NotificationTemplateRead:
        template = await self._repository.get_template_by_id(template_id)
        if template is None:
            raise NotificationTemplateNotFoundError(template_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            existing = await self._repository.get_template_by_name(data["name"])
            if existing is not None and existing.id != template_id:
                raise NotificationConflictError(f"Template name already exists: {data['name']}")
        if "status" in data:
            data["status"] = self._enum_value(data["status"])
        if "event_type" in data:
            data["event_type"] = self._enum_value(data["event_type"])
        template = await self._repository.update_template(template, data)
        return NotificationTemplateRead.model_validate(template)

    async def delete_template(self, template_id: uuid.UUID) -> None:
        template = await self._repository.get_template_by_id(template_id)
        if template is None:
            raise NotificationTemplateNotFoundError(template_id)
        await self._repository.delete_template(template)

    async def render_template(self, payload: NotificationRenderRequest) -> NotificationRenderResult:
        template = await self._repository.get_template_by_id(payload.template_id)
        if template is None:
            raise NotificationTemplateNotFoundError(payload.template_id)
        context = self._build_default_context(payload.context)
        subject, body = render_notification_template(template, context)
        return NotificationRenderResult(subject=subject, body=body)

    async def list_preferences(
        self,
        *,
        user_id: uuid.UUID | None,
        person_id: uuid.UUID | None,
        page: int,
        page_size: int,
    ) -> list[NotificationPreferenceRead]:
        page, page_size, offset = normalize_pagination(page, page_size)
        items, _total = await self._repository.list_preferences(
            filters=NotificationPreferenceListFilters(user_id=user_id, person_id=person_id),
            offset=offset,
            limit=page_size,
        )
        return [NotificationPreferenceRead.model_validate(item) for item in items]

    async def create_preference(
        self,
        payload: NotificationPreferenceCreate,
    ) -> NotificationPreferenceRead:
        await validate_user_or_person_exists(
            self._session,
            user_id=payload.user_id,
            person_id=payload.person_id,
        )
        channel_type = self._enum_value(payload.channel_type)
        event_type = self._enum_value(payload.event_type)
        duplicate = await self._repository.get_duplicate_preference(
            user_id=payload.user_id,
            person_id=payload.person_id,
            channel_type=channel_type,
            event_type=event_type,
        )
        if duplicate is not None:
            raise NotificationConflictError("Notification preference already exists")
        data = payload.model_dump()
        data["channel_type"] = channel_type
        data["event_type"] = event_type
        preference = await self._repository.create_preference(data)
        return NotificationPreferenceRead.model_validate(preference)

    async def update_preference(
        self,
        preference_id: uuid.UUID,
        payload: NotificationPreferenceUpdate,
    ) -> NotificationPreferenceRead:
        preference = await self._repository.get_preference_by_id(preference_id)
        if preference is None:
            raise NotificationPreferenceNotFoundError(preference_id)
        data = payload.model_dump(exclude_unset=True)
        preference = await self._repository.update_preference(preference, data)
        return NotificationPreferenceRead.model_validate(preference)

    async def delete_preference(self, preference_id: uuid.UUID) -> None:
        preference = await self._repository.get_preference_by_id(preference_id)
        if preference is None:
            raise NotificationPreferenceNotFoundError(preference_id)
        await self._repository.delete_preference(preference)

    async def list_messages(
        self,
        *,
        filters: NotificationMessageFilters,
        page: int,
        page_size: int,
    ) -> NotificationMessageListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_messages(
            filters=filters,
            offset=offset,
            limit=page_size,
        )
        return NotificationMessageListResponse(
            items=[NotificationMessageListItem.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_message(self, message_id: uuid.UUID) -> NotificationMessageRead:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)
        return NotificationMessageRead.model_validate(message)

    async def create_message(
        self,
        payload: NotificationMessageCreate,
        *,
        created_by_id: uuid.UUID | None,
    ) -> NotificationMessageRead:
        if payload.channel_id is not None:
            await validate_channel_exists(self._session, payload.channel_id)
        if payload.template_id is not None:
            template = await self._repository.get_template_by_id(payload.template_id)
            if template is None:
                raise NotificationTemplateNotFoundError(payload.template_id)
        if payload.entity_type and payload.entity_id:
            await validate_notification_entity_exists(
                self._session,
                payload.entity_type,
                payload.entity_id,
            )
        data = payload.model_dump()
        data["status"] = self._enum_value(payload.status)
        data["priority"] = self._enum_value(payload.priority)
        data["event_type"] = self._enum_value(payload.event_type)
        data["recipient_type"] = self._enum_value(payload.recipient_type)
        data["created_by_id"] = created_by_id
        message = await self._repository.create_message(data)
        return NotificationMessageRead.model_validate(message)

    async def update_message(
        self,
        message_id: uuid.UUID,
        payload: NotificationMessageUpdate,
    ) -> NotificationMessageRead:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)
        data = payload.model_dump(exclude_unset=True)
        if "channel_id" in data and data["channel_id"] is not None:
            await validate_channel_exists(self._session, data["channel_id"])
        if "template_id" in data and data["template_id"] is not None:
            template = await self._repository.get_template_by_id(data["template_id"])
            if template is None:
                raise NotificationTemplateNotFoundError(data["template_id"])
        entity_type = data.get("entity_type", message.entity_type)
        entity_id = data.get("entity_id", message.entity_id)
        if entity_type and entity_id:
            await validate_notification_entity_exists(self._session, entity_type, entity_id)
        for key in ("status", "priority", "event_type", "recipient_type"):
            if key in data and data[key] is not None:
                data[key] = self._enum_value(data[key])
        message = await self._repository.update_message(message, data)
        return NotificationMessageRead.model_validate(message)

    async def delete_message(self, message_id: uuid.UUID) -> None:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)
        await self._repository.delete_message(message)

    async def send_message(
        self,
        message_id: uuid.UUID,
        payload: NotificationSendRequest,
        *,
        created_by_id: uuid.UUID | None,
    ) -> NotificationSendResult:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)

        if message.template_id and payload.context:
            template = await self._repository.get_template_by_id(message.template_id)
            if template is not None:
                context = self._build_default_context(payload.context)
                subject, body = render_notification_template(template, context)
                await self._repository.update_message(
                    message,
                    {"subject": subject, "body": body},
                )
                message = await self._repository.get_message_by_id(message_id)
                if message is None:
                    raise NotificationMessageNotFoundError(message_id)

        result = await self._dispatcher.send_message(
            self._session,
            message,
            simulate=payload.simulate,
            recipient_override=payload.recipient_override,
            worker_instance_id=None,
        )
        await self._record_notification_activity(result.message, simulated=payload.simulate)
        return result

    async def list_delivery_attempts(
        self,
        *,
        message_id: uuid.UUID | None,
        page: int,
        page_size: int,
    ) -> NotificationDeliveryAttemptListResponse:
        page, page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_delivery_attempts(
            message_id=message_id,
            offset=offset,
            limit=page_size,
        )
        return NotificationDeliveryAttemptListResponse(
            items=[NotificationDeliveryAttemptRead.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=calculate_pages(total, page_size),
        )

    async def get_entity_notifications(
        self,
        entity_type: str,
        entity_id: uuid.UUID,
    ) -> EntityNotificationsResponse:
        await validate_notification_entity_exists(self._session, entity_type, entity_id)
        filters = NotificationMessageFilters(entity_type=entity_type, entity_id=entity_id)
        items, total = await self._repository.list_messages(
            filters=filters,
            offset=0,
            limit=50,
        )
        return EntityNotificationsResponse(
            entity_type=entity_type,
            entity_id=entity_id,
            messages=[NotificationMessageListItem.model_validate(item) for item in items],
            total=total,
        )

    async def queue_message(self, message_id: uuid.UUID) -> NotificationMessageRead:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)
        if message.status not in (
            NotificationMessageStatus.DRAFT.value,
            NotificationMessageStatus.FAILED.value,
        ):
            from app.core.errors import ValidationError

            raise ValidationError("Only draft or failed messages can be queued")
        updated = await self._repository.update_message(
            message,
            {"status": NotificationMessageStatus.QUEUED.value},
        )
        return NotificationMessageRead.model_validate(updated)

    async def process_queued_message(
        self,
        message_id: uuid.UUID,
        *,
        worker_instance_id: str | None = None,
    ) -> NotificationSendResult:
        message = await self._repository.get_message_by_id(message_id)
        if message is None:
            raise NotificationMessageNotFoundError(message_id)
        if message.status != NotificationMessageStatus.QUEUED.value:
            latest = message.delivery_attempts[-1] if message.delivery_attempts else None
            if latest is not None:
                return NotificationSendResult(
                    message=NotificationMessageRead.model_validate(message),
                    delivery_attempt=NotificationDeliveryAttemptRead.model_validate(latest),
                    simulated=message.status == NotificationMessageStatus.SIMULATED.value,
                    result_summary="Message already processed; skipped.",
                )
            from app.core.errors import ValidationError

            raise ValidationError(f"Message is not queued (status={message.status})")

        settings = get_settings()
        channel_type = (
            message.channel.channel_type if message.channel is not None else "in_app"
        )
        from app.modules.notifications.validators import is_external_channel_type

        simulate = settings.notification_worker_simulate_external
        if channel_type == "in_app":
            simulate = False
        elif is_external_channel_type(channel_type):
            simulate = (
                not settings.notification_external_delivery_enabled
                or settings.notification_worker_simulate_external
            )

        result = await self._dispatcher.send_message(
            self._session,
            message,
            simulate=simulate,
            worker_instance_id=worker_instance_id,
        )
        await self._record_notification_activity(result.message, simulated=result.simulated)
        return result

    async def create_and_send_message(
        self,
        payload: NotificationMessageCreate,
        *,
        simulate: bool = True,
        recipient_override: str | None = None,
        context: dict[str, Any] | None = None,
        created_by_id: uuid.UUID | None,
    ) -> NotificationSendResult:
        """Create a message and send it — used by automation integration."""
        if payload.template_id is not None and context:
            template = await self._repository.get_template_by_id(payload.template_id)
            if template is not None:
                merged_context = self._build_default_context(context)
                subject, body = render_notification_template(template, merged_context)
                payload = payload.model_copy(
                    update={"subject": subject or payload.subject, "body": body}
                )
        if payload.status == NotificationMessageStatus.DRAFT:
            payload = payload.model_copy(
                update={"status": NotificationMessageStatus.QUEUED}
            )
        message_read = await self.create_message(payload, created_by_id=created_by_id)
        return await self.send_message(
            message_read.id,
            NotificationSendRequest(
                simulate=simulate,
                recipient_override=recipient_override,
                context=context,
            ),
            created_by_id=created_by_id,
        )
