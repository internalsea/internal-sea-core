"""Safe MVP notification dispatch — simulation by default, no external calls."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.domain.enums import (
    NotificationChannelType,
    NotificationDeliveryStatus,
    NotificationMessageStatus,
)
from app.models.notifications import NotificationDeliveryAttempt, NotificationMessage
from app.modules.notifications.schemas import (
    NotificationDeliveryAttemptRead,
    NotificationMessageRead,
    NotificationSendResult,
)
from app.modules.notifications.validators import is_external_channel_type


class NotificationDispatcher:
    async def send_message(
        self,
        session: AsyncSession,
        message: NotificationMessage,
        *,
        simulate: bool = True,
        recipient_override: str | None = None,
        worker_instance_id: str | None = None,
    ) -> NotificationSendResult:
        terminal_statuses = {
            NotificationMessageStatus.SENT.value,
            NotificationMessageStatus.SIMULATED.value,
            NotificationMessageStatus.CANCELLED.value,
        }
        if message.status in terminal_statuses:
            latest = message.delivery_attempts[-1] if message.delivery_attempts else None
            if latest is not None:
                return NotificationSendResult(
                    message=NotificationMessageRead.model_validate(message),
                    delivery_attempt=NotificationDeliveryAttemptRead.model_validate(latest),
                    simulated=message.status == NotificationMessageStatus.SIMULATED.value,
                    result_summary="Message already processed; skipped.",
                )

        settings = get_settings()
        if not simulate and not settings.notification_external_delivery_enabled:
            channel_type_preview = (
                message.channel.channel_type
                if message.channel is not None
                else NotificationChannelType.IN_APP.value
            )
            if is_external_channel_type(channel_type_preview):
                simulate = settings.notification_worker_simulate_external

        now = datetime.now(UTC)
        channel_type = (
            message.channel.channel_type
            if message.channel is not None
            else NotificationChannelType.IN_APP.value
        )
        recipient = (
            recipient_override
            or message.recipient_value
            or (message.channel.default_recipient if message.channel else None)
        )

        attempt = NotificationDeliveryAttempt(
            id=uuid.uuid4(),
            message_id=message.id,
            status=NotificationDeliveryStatus.PENDING.value,
            attempt_number=len(message.delivery_attempts) + 1,
            provider=channel_type,
            worker_instance_id=worker_instance_id,
            started_at=now,
            created_at=now,
            updated_at=now,
            request_payload={
                "simulate": simulate,
                "channel_type": channel_type,
                "recipient": recipient,
                "subject": message.subject,
                "body_preview": (message.body[:200] + "…")
                if len(message.body) > 200
                else message.body,
            },
        )
        session.add(attempt)

        if simulate:
            message.status = NotificationMessageStatus.SIMULATED.value
            message.simulated_at = now
            message.error_message = None
            attempt.status = NotificationDeliveryStatus.SIMULATED.value
            attempt.finished_at = now
            attempt.response_payload = {"mode": "simulation", "delivered": False}
            result_summary = "Notification simulated successfully."
        elif channel_type == NotificationChannelType.IN_APP.value:
            message.status = NotificationMessageStatus.SENT.value
            message.sent_at = now
            message.error_message = None
            attempt.status = NotificationDeliveryStatus.SENT.value
            attempt.finished_at = now
            attempt.response_payload = {"mode": "in_app", "delivered": True}
            result_summary = "In-app notification recorded as sent."
        elif is_external_channel_type(channel_type):
            error = "External delivery is not implemented in MVP."
            message.status = NotificationMessageStatus.FAILED.value
            message.error_message = error
            attempt.status = NotificationDeliveryStatus.FAILED.value
            attempt.error_message = error
            attempt.finished_at = now
            attempt.response_payload = {"mode": "external_blocked", "delivered": False}
            result_summary = error
        else:
            error = "Unsupported channel type for delivery."
            message.status = NotificationMessageStatus.FAILED.value
            message.error_message = error
            attempt.status = NotificationDeliveryStatus.FAILED.value
            attempt.error_message = error
            attempt.finished_at = now
            result_summary = error

        await session.commit()
        await session.refresh(message)
        await session.refresh(attempt)

        return NotificationSendResult(
            message=NotificationMessageRead.model_validate(message),
            delivery_attempt=NotificationDeliveryAttemptRead.model_validate(attempt),
            simulated=simulate,
            result_summary=result_summary,
        )
