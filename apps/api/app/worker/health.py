from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.worker.locks import count_locked_automation_triggers, count_locked_notification_messages
from app.worker.scheduler import count_due_automation_triggers, count_due_notification_messages
from app.worker.schemas import DueWorkSummary, WorkerStatus


def resolve_worker_instance_id(instance_id: str | None = None) -> str:
    settings = get_settings()
    return instance_id or settings.worker_instance_id or "local-worker"


async def get_worker_status(
    session: AsyncSession,
    *,
    instance_id: str | None = None,
) -> WorkerStatus:
    settings = get_settings()
    return WorkerStatus(
        worker_enabled=settings.worker_enabled,
        worker_instance_id=resolve_worker_instance_id(instance_id),
        poll_interval_seconds=settings.worker_poll_interval_seconds,
        batch_size=settings.worker_batch_size,
        automation_due_count=await count_due_automation_triggers(session),
        notification_due_count=await count_due_notification_messages(session),
        last_checked_at=datetime.now(timezone.utc),
    )


async def get_due_work_summary(session: AsyncSession) -> DueWorkSummary:
    return DueWorkSummary(
        due_automation_triggers=await count_due_automation_triggers(session),
        due_notifications=await count_due_notification_messages(session),
        locked_automation_triggers=await count_locked_automation_triggers(session),
        locked_notifications=await count_locked_notification_messages(session),
    )
