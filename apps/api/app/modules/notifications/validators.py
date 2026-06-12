from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import NotificationChannelType
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck
from app.models.identity import User
from app.models.notifications import (
    NotificationChannel,
    NotificationMessage,
    NotificationTemplate,
)
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.notifications.errors import (
    NotificationChannelNotFoundError,
    NotificationEntityNotFoundError,
    NotificationMessageNotFoundError,
    NotificationTemplateNotFoundError,
    UnsupportedNotificationEntityTypeError,
)

SUPPORTED_ENTITY_TYPES: dict[str, type] = {
    "data_product": DataProduct,
    "work_item": WorkItem,
    "project": Project,
    "internal_project": Project,
    "person": Person,
    "team": Team,
    "capability": Capability,
    "compliance_check": ComplianceCheck,
}


def is_supported_notification_entity_type(entity_type: str) -> bool:
    return entity_type in SUPPORTED_ENTITY_TYPES


async def validate_channel_exists(
    session: AsyncSession,
    channel_id: uuid.UUID,
) -> NotificationChannel:
    channel = await session.get(NotificationChannel, channel_id)
    if channel is None:
        raise NotificationChannelNotFoundError(channel_id)
    return channel


async def validate_template_exists(
    session: AsyncSession,
    template_id: uuid.UUID,
) -> NotificationTemplate:
    template = await session.get(NotificationTemplate, template_id)
    if template is None:
        raise NotificationTemplateNotFoundError(template_id)
    return template


async def validate_message_exists(
    session: AsyncSession,
    message_id: uuid.UUID,
) -> NotificationMessage:
    message = await session.get(NotificationMessage, message_id)
    if message is None:
        raise NotificationMessageNotFoundError(message_id)
    return message


async def validate_user_or_person_exists(
    session: AsyncSession,
    *,
    user_id: uuid.UUID | None,
    person_id: uuid.UUID | None,
) -> None:
    if user_id is not None:
        user = await session.get(User, user_id)
        if user is None:
            raise NotificationEntityNotFoundError("user", user_id)
    if person_id is not None:
        person = await session.get(Person, person_id)
        if person is None:
            raise NotificationEntityNotFoundError("person", person_id)


async def validate_notification_entity_exists(
    session: AsyncSession,
    entity_type: str,
    entity_id: uuid.UUID,
) -> None:
    if not is_supported_notification_entity_type(entity_type):
        raise UnsupportedNotificationEntityTypeError(entity_type)

    model = SUPPORTED_ENTITY_TYPES[entity_type]
    entity = await session.get(model, entity_id)
    if entity is None:
        raise NotificationEntityNotFoundError(entity_type, entity_id)

    if entity_type == "internal_project" and getattr(entity, "project_type", None) != "internal":
        raise NotificationEntityNotFoundError(entity_type, entity_id)
    if entity_type == "project" and getattr(entity, "project_type", None) == "internal":
        raise NotificationEntityNotFoundError(entity_type, entity_id)


def is_external_channel_type(channel_type: str | NotificationChannelType) -> bool:
    value = channel_type.value if hasattr(channel_type, "value") else str(channel_type)
    return value not in {NotificationChannelType.IN_APP.value}
