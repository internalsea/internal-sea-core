"""Simple database-backed locking for worker item claiming."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.automation import AutomationTrigger
from app.models.notifications import NotificationMessage


def is_lock_expired(lock_expires_at: datetime | None) -> bool:
    if lock_expires_at is None:
        return True
    return lock_expires_at < datetime.now(timezone.utc)


async def acquire_automation_trigger_lock(
    session: AsyncSession,
    trigger_id: uuid.UUID,
    worker_instance_id: str,
    timeout_seconds: int,
) -> bool:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=timeout_seconds)
    stmt = (
        update(AutomationTrigger)
        .where(
            AutomationTrigger.id == trigger_id,
            or_(
                AutomationTrigger.locked_at.is_(None),
                AutomationTrigger.lock_expires_at < now,
            ),
        )
        .values(
            locked_at=now,
            locked_by=worker_instance_id,
            lock_expires_at=expires,
        )
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount == 1


async def release_automation_trigger_lock(
    session: AsyncSession,
    trigger_id: uuid.UUID,
) -> None:
    stmt = (
        update(AutomationTrigger)
        .where(AutomationTrigger.id == trigger_id)
        .values(locked_at=None, locked_by=None, lock_expires_at=None)
    )
    await session.execute(stmt)
    await session.commit()


async def acquire_notification_message_lock(
    session: AsyncSession,
    message_id: uuid.UUID,
    worker_instance_id: str,
    timeout_seconds: int,
) -> bool:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=timeout_seconds)
    stmt = (
        update(NotificationMessage)
        .where(
            NotificationMessage.id == message_id,
            or_(
                NotificationMessage.locked_at.is_(None),
                NotificationMessage.lock_expires_at < now,
            ),
        )
        .values(
            locked_at=now,
            locked_by=worker_instance_id,
            lock_expires_at=expires,
        )
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount == 1


async def release_notification_message_lock(
    session: AsyncSession,
    message_id: uuid.UUID,
) -> None:
    stmt = (
        update(NotificationMessage)
        .where(NotificationMessage.id == message_id)
        .values(locked_at=None, locked_by=None, lock_expires_at=None)
    )
    await session.execute(stmt)
    await session.commit()


async def count_locked_automation_triggers(session: AsyncSession) -> int:
    now = datetime.now(timezone.utc)
    from sqlalchemy import func, select

    result = await session.scalar(
        select(func.count())
        .select_from(AutomationTrigger)
        .where(
            and_(
                AutomationTrigger.locked_at.is_not(None),
                AutomationTrigger.lock_expires_at >= now,
            )
        )
    )
    return int(result or 0)


async def count_locked_notification_messages(session: AsyncSession) -> int:
    now = datetime.now(timezone.utc)
    from sqlalchemy import func, select

    result = await session.scalar(
        select(func.count())
        .select_from(NotificationMessage)
        .where(
            and_(
                NotificationMessage.locked_at.is_not(None),
                NotificationMessage.lock_expires_at >= now,
            )
        )
    )
    return int(result or 0)
