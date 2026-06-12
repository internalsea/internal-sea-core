import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums import (
    NotificationChannelStatus,
    NotificationMessageStatus,
    NotificationTemplateStatus,
)
from app.models.notifications import (
    NotificationChannel,
    NotificationDeliveryAttempt,
    NotificationMessage,
    NotificationPreference,
    NotificationTemplate,
)
from app.modules.notifications.schemas import (
    NotificationChannelFilters,
    NotificationMessageFilters,
    NotificationTemplateFilters,
)


@dataclass
class NotificationPreferenceListFilters:
    user_id: uuid.UUID | None = None
    person_id: uuid.UUID | None = None


class NotificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _enum_value(self, value) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    def _apply_channel_filters(self, query, filters: NotificationChannelFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    NotificationChannel.name.ilike(pattern),
                    NotificationChannel.description.ilike(pattern),
                    NotificationChannel.default_recipient.ilike(pattern),
                )
            )
        if filters.channel_type is not None:
            query = query.where(
                NotificationChannel.channel_type == filters.channel_type.value
            )
        if filters.status is not None:
            query = query.where(NotificationChannel.status == filters.status.value)
        return query

    def _apply_template_filters(self, query, filters: NotificationTemplateFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    NotificationTemplate.name.ilike(pattern),
                    NotificationTemplate.description.ilike(pattern),
                    NotificationTemplate.body_template.ilike(pattern),
                )
            )
        if filters.status is not None:
            query = query.where(NotificationTemplate.status == filters.status.value)
        if filters.event_type is not None:
            query = query.where(NotificationTemplate.event_type == filters.event_type.value)
        return query

    def _apply_message_filters(self, query, filters: NotificationMessageFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    NotificationMessage.subject.ilike(pattern),
                    NotificationMessage.body.ilike(pattern),
                    NotificationMessage.recipient_value.ilike(pattern),
                )
            )
        if filters.status is not None:
            query = query.where(NotificationMessage.status == filters.status.value)
        if filters.priority is not None:
            query = query.where(NotificationMessage.priority == filters.priority.value)
        if filters.event_type is not None:
            query = query.where(NotificationMessage.event_type == filters.event_type.value)
        if filters.channel_id is not None:
            query = query.where(NotificationMessage.channel_id == filters.channel_id)
        if filters.template_id is not None:
            query = query.where(NotificationMessage.template_id == filters.template_id)
        if filters.entity_type is not None:
            query = query.where(NotificationMessage.entity_type == filters.entity_type)
        if filters.entity_id is not None:
            query = query.where(NotificationMessage.entity_id == filters.entity_id)
        if filters.automation_run_id is not None:
            query = query.where(
                NotificationMessage.automation_run_id == filters.automation_run_id
            )
        return query

    async def list_channels(
        self,
        *,
        filters: NotificationChannelFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[NotificationChannel], int]:
        base = select(NotificationChannel)
        filtered = self._apply_channel_filters(base, filters)
        count = self._apply_channel_filters(
            select(func.count(NotificationChannel.id)),
            filters,
        )
        total = int(await self._session.scalar(count) or 0)
        result = await self._session.scalars(
            filtered.order_by(NotificationChannel.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_channel_by_id(self, channel_id: uuid.UUID) -> NotificationChannel | None:
        return await self._session.get(NotificationChannel, channel_id)

    async def get_channel_by_name(self, name: str) -> NotificationChannel | None:
        return await self._session.scalar(
            select(NotificationChannel).where(NotificationChannel.name == name)
        )

    async def create_channel(self, payload: dict[str, object]) -> NotificationChannel:
        channel = NotificationChannel(**payload)
        self._session.add(channel)
        await self._session.commit()
        await self._session.refresh(channel)
        return channel

    async def update_channel(
        self,
        channel: NotificationChannel,
        payload: dict[str, object],
    ) -> NotificationChannel:
        for key, value in payload.items():
            setattr(channel, key, value)
        await self._session.commit()
        await self._session.refresh(channel)
        return channel

    async def delete_channel(self, channel: NotificationChannel) -> None:
        await self._session.delete(channel)
        await self._session.commit()

    async def list_templates(
        self,
        *,
        filters: NotificationTemplateFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[NotificationTemplate], int]:
        base = select(NotificationTemplate)
        filtered = self._apply_template_filters(base, filters)
        count = self._apply_template_filters(
            select(func.count(NotificationTemplate.id)),
            filters,
        )
        total = int(await self._session.scalar(count) or 0)
        result = await self._session.scalars(
            filtered.order_by(NotificationTemplate.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_template_by_id(self, template_id: uuid.UUID) -> NotificationTemplate | None:
        return await self._session.get(NotificationTemplate, template_id)

    async def get_template_by_name(self, name: str) -> NotificationTemplate | None:
        return await self._session.scalar(
            select(NotificationTemplate).where(NotificationTemplate.name == name)
        )

    async def create_template(self, payload: dict[str, object]) -> NotificationTemplate:
        template = NotificationTemplate(**payload)
        self._session.add(template)
        await self._session.commit()
        await self._session.refresh(template)
        return template

    async def update_template(
        self,
        template: NotificationTemplate,
        payload: dict[str, object],
    ) -> NotificationTemplate:
        for key, value in payload.items():
            setattr(template, key, value)
        await self._session.commit()
        await self._session.refresh(template)
        return template

    async def delete_template(self, template: NotificationTemplate) -> None:
        await self._session.delete(template)
        await self._session.commit()

    async def list_preferences(
        self,
        *,
        filters: NotificationPreferenceListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[NotificationPreference], int]:
        query = select(NotificationPreference)
        if filters.user_id is not None:
            query = query.where(NotificationPreference.user_id == filters.user_id)
        if filters.person_id is not None:
            query = query.where(NotificationPreference.person_id == filters.person_id)
        count_query = select(func.count()).select_from(query.subquery())
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            query.order_by(NotificationPreference.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_preference_by_id(
        self,
        preference_id: uuid.UUID,
    ) -> NotificationPreference | None:
        return await self._session.get(NotificationPreference, preference_id)

    async def get_duplicate_preference(
        self,
        *,
        user_id: uuid.UUID | None,
        person_id: uuid.UUID | None,
        channel_type: str,
        event_type: str,
    ) -> NotificationPreference | None:
        return await self._session.scalar(
            select(NotificationPreference).where(
                NotificationPreference.user_id == user_id,
                NotificationPreference.person_id == person_id,
                NotificationPreference.channel_type == channel_type,
                NotificationPreference.event_type == event_type,
            )
        )

    async def create_preference(self, payload: dict[str, object]) -> NotificationPreference:
        preference = NotificationPreference(**payload)
        self._session.add(preference)
        await self._session.commit()
        await self._session.refresh(preference)
        return preference

    async def update_preference(
        self,
        preference: NotificationPreference,
        payload: dict[str, object],
    ) -> NotificationPreference:
        for key, value in payload.items():
            setattr(preference, key, value)
        await self._session.commit()
        await self._session.refresh(preference)
        return preference

    async def delete_preference(self, preference: NotificationPreference) -> None:
        await self._session.delete(preference)
        await self._session.commit()

    async def list_messages(
        self,
        *,
        filters: NotificationMessageFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[NotificationMessage], int]:
        base = select(NotificationMessage)
        filtered = self._apply_message_filters(base, filters)
        count = self._apply_message_filters(
            select(func.count(NotificationMessage.id)),
            filters,
        )
        total = int(await self._session.scalar(count) or 0)
        result = await self._session.scalars(
            filtered.order_by(NotificationMessage.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_message_by_id(self, message_id: uuid.UUID) -> NotificationMessage | None:
        return await self._session.scalar(
            select(NotificationMessage)
            .options(
                selectinload(NotificationMessage.channel),
                selectinload(NotificationMessage.delivery_attempts),
            )
            .where(NotificationMessage.id == message_id)
        )

    async def create_message(self, payload: dict[str, object]) -> NotificationMessage:
        if "metadata" in payload:
            payload["message_metadata"] = payload.pop("metadata")
        message = NotificationMessage(**payload)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def update_message(
        self,
        message: NotificationMessage,
        payload: dict[str, object],
    ) -> NotificationMessage:
        if "metadata" in payload:
            payload["message_metadata"] = payload.pop("metadata")
        for key, value in payload.items():
            setattr(message, key, value)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def delete_message(self, message: NotificationMessage) -> None:
        await self._session.delete(message)
        await self._session.commit()

    async def list_delivery_attempts(
        self,
        *,
        message_id: uuid.UUID | None,
        offset: int,
        limit: int,
    ) -> tuple[list[NotificationDeliveryAttempt], int]:
        query = select(NotificationDeliveryAttempt)
        if message_id is not None:
            query = query.where(NotificationDeliveryAttempt.message_id == message_id)
        count_query = select(func.count()).select_from(query.subquery())
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            query.order_by(NotificationDeliveryAttempt.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def create_delivery_attempt(
        self,
        payload: dict[str, object],
    ) -> NotificationDeliveryAttempt:
        attempt = NotificationDeliveryAttempt(**payload)
        self._session.add(attempt)
        await self._session.commit()
        await self._session.refresh(attempt)
        return attempt

    async def update_delivery_attempt(
        self,
        attempt: NotificationDeliveryAttempt,
        payload: dict[str, object],
    ) -> NotificationDeliveryAttempt:
        for key, value in payload.items():
            setattr(attempt, key, value)
        await self._session.commit()
        await self._session.refresh(attempt)
        return attempt

    async def get_overview(self) -> dict[str, int]:
        channels_total = int(
            await self._session.scalar(select(func.count(NotificationChannel.id))) or 0
        )
        channels_active = int(
            await self._session.scalar(
                select(func.count(NotificationChannel.id)).where(
                    NotificationChannel.status == NotificationChannelStatus.ACTIVE.value
                )
            )
            or 0
        )
        templates_total = int(
            await self._session.scalar(select(func.count(NotificationTemplate.id))) or 0
        )
        templates_active = int(
            await self._session.scalar(
                select(func.count(NotificationTemplate.id)).where(
                    NotificationTemplate.status == NotificationTemplateStatus.ACTIVE.value
                )
            )
            or 0
        )
        messages_total = int(
            await self._session.scalar(select(func.count(NotificationMessage.id))) or 0
        )
        messages_sent = int(
            await self._session.scalar(
                select(func.count(NotificationMessage.id)).where(
                    NotificationMessage.status == NotificationMessageStatus.SENT.value
                )
            )
            or 0
        )
        messages_simulated = int(
            await self._session.scalar(
                select(func.count(NotificationMessage.id)).where(
                    NotificationMessage.status == NotificationMessageStatus.SIMULATED.value
                )
            )
            or 0
        )
        messages_failed = int(
            await self._session.scalar(
                select(func.count(NotificationMessage.id)).where(
                    NotificationMessage.status == NotificationMessageStatus.FAILED.value
                )
            )
            or 0
        )
        delivery_attempts_total = int(
            await self._session.scalar(select(func.count(NotificationDeliveryAttempt.id))) or 0
        )
        delivery_attempts_failed = int(
            await self._session.scalar(
                select(func.count(NotificationDeliveryAttempt.id)).where(
                    NotificationDeliveryAttempt.status == "failed"
                )
            )
            or 0
        )
        return {
            "channels_total": channels_total,
            "channels_active": channels_active,
            "templates_total": templates_total,
            "templates_active": templates_active,
            "messages_total": messages_total,
            "messages_sent": messages_sent,
            "messages_simulated": messages_simulated,
            "messages_failed": messages_failed,
            "delivery_attempts_total": delivery_attempts_total,
            "delivery_attempts_failed": delivery_attempts_failed,
        }
