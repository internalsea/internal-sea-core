"""Worker cycle orchestration."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import get_settings
from app.models.automation import AutomationTrigger
from app.modules.activity.dependencies import build_activity_service
from app.modules.automation.repository import AutomationRepository
from app.modules.automation.runner import AutomationRunner
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.service import NotificationService
from app.worker.health import resolve_worker_instance_id
from app.worker.locks import (
    acquire_automation_trigger_lock,
    acquire_notification_message_lock,
    release_automation_trigger_lock,
    release_notification_message_lock,
)
from app.worker.scheduler import (
    find_due_automation_triggers,
    find_due_notification_messages,
    update_trigger_next_run,
)
from app.worker.schemas import WorkerCycleResult

logger = logging.getLogger(__name__)


class WorkerRunner:
    def __init__(
        self,
        session: AsyncSession,
        *,
        instance_id: str | None = None,
        batch_size: int | None = None,
    ) -> None:
        self._session = session
        self._settings = get_settings()
        self._instance_id = resolve_worker_instance_id(instance_id)
        self._batch_size = batch_size or self._settings.worker_batch_size
        self._lock_timeout = self._settings.worker_lock_timeout_seconds
        self._automation_repo = AutomationRepository(session)
        self._automation_runner = AutomationRunner(session, self._automation_repo)
        self._notification_service = NotificationService(
            NotificationRepository(session),
            build_activity_service(session),
            session,
        )

    async def run_once(self) -> WorkerCycleResult:
        started_at = datetime.now(UTC)
        failures: list[str] = []
        due_trigger_items = await find_due_automation_triggers(self._session, self._batch_size)
        due_message_items = await find_due_notification_messages(self._session, self._batch_size)
        automation_runs_created = await self.process_due_automation_triggers(failures)
        notifications_processed = await self.process_due_notifications(failures)
        finished_at = datetime.now(UTC)

        due_triggers = len(due_trigger_items)
        due_notifications = len(due_message_items)
        summary = (
            f"Worker cycle complete: {automation_runs_created} automation run(s), "
            f"{notifications_processed} notification(s) processed"
        )
        if failures:
            summary += f", {len(failures)} failure(s)"

        return WorkerCycleResult(
            worker_instance_id=self._instance_id,
            started_at=started_at,
            finished_at=finished_at,
            due_triggers_found=due_triggers,
            automation_runs_created=automation_runs_created,
            notification_messages_found=due_notifications,
            notifications_processed=notifications_processed,
            failures=failures,
            summary=summary,
        )

    async def run_loop(self, interval_seconds: int | None = None) -> None:
        import asyncio

        interval = interval_seconds or self._settings.worker_poll_interval_seconds
        logger.info(
            "Worker loop started (instance=%s, interval=%ss, batch=%s)",
            self._instance_id,
            interval,
            self._batch_size,
        )
        try:
            while True:
                try:
                    result = await self.run_once()
                    logger.info(result.summary)
                except Exception as exc:
                    logger.exception("Worker cycle failed: %s", exc)
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Worker loop stopped")

    @classmethod
    async def run_loop_with_session_factory(
        cls,
        sessionmaker: async_sessionmaker[AsyncSession],
        *,
        instance_id: str | None = None,
        batch_size: int | None = None,
        interval_seconds: int | None = None,
    ) -> None:
        """Run continuous cycles with a fresh session per iteration."""
        import asyncio

        settings = get_settings()
        interval = interval_seconds or settings.worker_poll_interval_seconds
        resolved_id = resolve_worker_instance_id(instance_id)
        logger.info(
            "Worker loop started (instance=%s, interval=%ss)",
            resolved_id,
            interval,
        )
        try:
            while True:
                try:
                    async with sessionmaker() as session:
                        runner = cls(
                            session,
                            instance_id=resolved_id,
                            batch_size=batch_size,
                        )
                        result = await runner.run_once()
                        logger.info(result.summary)
                except Exception as exc:
                    logger.exception("Worker cycle failed: %s", exc)
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Worker loop stopped")

    async def process_due_automation_triggers(self, failures: list[str] | None = None) -> int:
        error_list = failures if failures is not None else []
        due_triggers = await find_due_automation_triggers(self._session, self._batch_size)
        runs_created = 0

        for trigger in due_triggers:
            locked = await acquire_automation_trigger_lock(
                self._session,
                trigger.id,
                self._instance_id,
                self._lock_timeout,
            )
            if not locked:
                continue

            try:
                await self._session.refresh(trigger)
                simulate = self._should_simulate_trigger(trigger)
                result = await self._automation_runner.run_trigger(
                    trigger,
                    executed_by_id=None,
                    simulate=simulate,
                    worker_instance_id=self._instance_id,
                )
                runs_created += 1

                schedule = None
                if trigger.schedule_id:
                    schedule = await self._automation_repo.get_schedule_by_id(trigger.schedule_id)
                run_at = result.run.finished_at or datetime.now(UTC)
                await update_trigger_next_run(
                    self._session,
                    trigger,
                    schedule,
                    run_at=run_at,
                )
            except Exception as exc:
                error_list.append(f"trigger {trigger.id}: {exc}")
                logger.exception("Failed to process automation trigger %s", trigger.id)
            finally:
                await release_automation_trigger_lock(self._session, trigger.id)

        return runs_created

    async def process_due_notifications(self, failures: list[str] | None = None) -> int:
        error_list = failures if failures is not None else []
        due_messages = await find_due_notification_messages(self._session, self._batch_size)
        processed = 0

        for message in due_messages:
            locked = await acquire_notification_message_lock(
                self._session,
                message.id,
                self._instance_id,
                self._lock_timeout,
            )
            if not locked:
                continue

            try:
                await self._session.refresh(message)
                await self._notification_service.process_queued_message(
                    message.id,
                    worker_instance_id=self._instance_id,
                )
                processed += 1
            except Exception as exc:
                error_list.append(f"message {message.id}: {exc}")
                logger.exception("Failed to process notification message %s", message.id)
            finally:
                await release_notification_message_lock(self._session, message.id)

        return processed

    def _should_simulate_trigger(self, trigger: AutomationTrigger) -> bool:
        if not self._settings.automation_real_run_enabled:
            return True
        if self._settings.automation_default_simulate:
            return True
        return False
