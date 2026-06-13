"""Due work discovery and schedule next-run calculation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast

from dateutil.relativedelta import relativedelta
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import AutomationStatus, AutomationTriggerType, NotificationMessageStatus
from app.models.automation import AutomationSchedule, AutomationTrigger
from app.models.notifications import NotificationMessage


def calculate_next_run_at(
    schedule: AutomationSchedule,
    from_datetime: datetime,
) -> datetime | None:
    frequency = schedule.frequency
    if frequency == "once":
        return None
    if frequency == "custom":
        return schedule.next_run_at
    if frequency == "daily":
        return cast(datetime, from_datetime + relativedelta(days=1))
    if frequency == "weekly":
        return cast(datetime, from_datetime + relativedelta(weeks=1))
    if frequency == "monthly":
        return cast(datetime, from_datetime + relativedelta(months=1))
    if frequency == "quarterly":
        return cast(datetime, from_datetime + relativedelta(months=3))
    if frequency == "yearly":
        return cast(datetime, from_datetime + relativedelta(years=1))
    return None


async def find_due_automation_triggers(
    session: AsyncSession,
    limit: int,
) -> list[AutomationTrigger]:
    now = datetime.now(UTC)
    stmt = (
        select(AutomationTrigger)
        .where(
            AutomationTrigger.status == AutomationStatus.ACTIVE.value,
            AutomationTrigger.trigger_type == AutomationTriggerType.SCHEDULE.value,
            AutomationTrigger.next_run_at.is_not(None),
            AutomationTrigger.next_run_at <= now,
            or_(
                AutomationTrigger.locked_at.is_(None),
                AutomationTrigger.lock_expires_at < now,
            ),
        )
        .order_by(AutomationTrigger.next_run_at.asc(), AutomationTrigger.updated_at.asc())
        .limit(limit)
    )
    result = await session.scalars(stmt)
    return list(result.all())


async def find_due_notification_messages(
    session: AsyncSession,
    limit: int,
) -> list[NotificationMessage]:
    now = datetime.now(UTC)
    stmt = (
        select(NotificationMessage)
        .where(
            NotificationMessage.status == NotificationMessageStatus.QUEUED.value,
            or_(
                NotificationMessage.scheduled_at.is_(None),
                NotificationMessage.scheduled_at <= now,
            ),
            or_(
                NotificationMessage.locked_at.is_(None),
                NotificationMessage.lock_expires_at < now,
            ),
        )
        .order_by(
            NotificationMessage.scheduled_at.asc().nulls_first(),
            NotificationMessage.created_at.asc(),
        )
        .limit(limit)
    )
    result = await session.scalars(stmt)
    return list(result.all())


async def count_due_automation_triggers(session: AsyncSession) -> int:
    now = datetime.now(UTC)
    from sqlalchemy import func

    result = await session.scalar(
        select(func.count())
        .select_from(AutomationTrigger)
        .where(
            AutomationTrigger.status == AutomationStatus.ACTIVE.value,
            AutomationTrigger.trigger_type == AutomationTriggerType.SCHEDULE.value,
            AutomationTrigger.next_run_at.is_not(None),
            AutomationTrigger.next_run_at <= now,
            or_(
                AutomationTrigger.locked_at.is_(None),
                AutomationTrigger.lock_expires_at < now,
            ),
        )
    )
    return int(result or 0)


async def count_due_notification_messages(session: AsyncSession) -> int:
    now = datetime.now(UTC)
    from sqlalchemy import func

    result = await session.scalar(
        select(func.count())
        .select_from(NotificationMessage)
        .where(
            NotificationMessage.status == NotificationMessageStatus.QUEUED.value,
            or_(
                NotificationMessage.scheduled_at.is_(None),
                NotificationMessage.scheduled_at <= now,
            ),
            or_(
                NotificationMessage.locked_at.is_(None),
                NotificationMessage.lock_expires_at < now,
            ),
        )
    )
    return int(result or 0)


async def update_trigger_next_run(
    session: AsyncSession,
    trigger: AutomationTrigger,
    schedule: AutomationSchedule | None,
    *,
    run_at: datetime,
) -> None:
    trigger.last_run_at = run_at
    if schedule is not None:
        schedule.last_run_at = run_at
        trigger.next_run_at = calculate_next_run_at(schedule, run_at)
        schedule.next_run_at = trigger.next_run_at
    else:
        trigger.next_run_at = None
    await session.commit()
