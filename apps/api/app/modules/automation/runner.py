from __future__ import annotations

import uuid
from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.domain.enums import (
    ActivityAction,
    ActivityEntityType,
    AutomationActionType,
    AutomationRunStatus,
    AutomationTargetType,
    ComplianceSubjectType,
    NotificationChannelType,
    NotificationEventType,
    NotificationMessageStatus,
    NotificationPriority,
    NotificationRecipientType,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.models.automation import AutomationRun, AutomationTrigger
from app.models.compliance import ComplianceCheck
from app.models.work import Comment, WorkItem
from app.modules.activity.dependencies import build_activity_service
from app.modules.activity.repository import ActivityRepository
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.automation.repository import AutomationRepository
from app.modules.automation.schemas import AutomationRunRead, AutomationRunResult
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import NotificationMessageCreate
from app.modules.notifications.service import NotificationService
from app.modules.notifications.validators import is_external_channel_type

MVP_SAFE_ACTION_TYPES: set[AutomationActionType] = {
    AutomationActionType.CREATE_WORK_ITEM,
    AutomationActionType.ADD_COMMENT,
    AutomationActionType.CREATE_ACTIVITY_EVENT,
    AutomationActionType.SEND_NOTIFICATION,
}

AUTOMATION_TARGET_TO_ENTITY: dict[AutomationTargetType, str] = {
    AutomationTargetType.DATA_PRODUCT: "data_product",
    AutomationTargetType.WORK_ITEM: "work_item",
    AutomationTargetType.PROJECT: "project",
    AutomationTargetType.INTERNAL_PROJECT: "internal_project",
    AutomationTargetType.TEAM: "team",
    AutomationTargetType.CAPABILITY: "capability",
    AutomationTargetType.COMPLIANCE_CHECK: "compliance_check",
}

COMMENT_TARGET_TYPES: set[AutomationTargetType] = {
    AutomationTargetType.DATA_PRODUCT,
    AutomationTargetType.WORK_ITEM,
    AutomationTargetType.PROJECT,
    AutomationTargetType.INTERNAL_PROJECT,
}


def _enum_value(value: object) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _resolve_activity_entity(
    target_type: AutomationTargetType | None,
    target_id: uuid.UUID | None,
    session_entity: Any | None = None,
) -> tuple[ActivityEntityType, uuid.UUID] | None:
    if target_type is None or target_id is None:
        return None

    mapping = {
        AutomationTargetType.DATA_PRODUCT: ActivityEntityType.DATA_PRODUCT,
        AutomationTargetType.WORK_ITEM: ActivityEntityType.WORK_ITEM,
        AutomationTargetType.PROJECT: ActivityEntityType.PROJECT,
        AutomationTargetType.INTERNAL_PROJECT: ActivityEntityType.INTERNAL_PROJECT,
        AutomationTargetType.TEAM: ActivityEntityType.TEAM,
        AutomationTargetType.CAPABILITY: ActivityEntityType.CAPABILITY,
    }
    if target_type in mapping:
        return mapping[target_type], target_id

    if target_type == AutomationTargetType.COMPLIANCE_CHECK and session_entity is not None:
        subject_type = getattr(session_entity, "subject_type", None)
        subject_id = getattr(session_entity, "subject_id", None)
        if subject_type and subject_id:
            try:
                compliance_subject = ComplianceSubjectType(subject_type)
            except ValueError:
                return None
            subject_mapping = {
                ComplianceSubjectType.DATA_PRODUCT: ActivityEntityType.DATA_PRODUCT,
                ComplianceSubjectType.PROJECT: ActivityEntityType.PROJECT,
                ComplianceSubjectType.INTERNAL_PROJECT: ActivityEntityType.INTERNAL_PROJECT,
                ComplianceSubjectType.TEAM: ActivityEntityType.TEAM,
                ComplianceSubjectType.CAPABILITY: ActivityEntityType.CAPABILITY,
            }
            if subject_type == "work_item":
                return ActivityEntityType.WORK_ITEM, subject_id
            if compliance_subject in subject_mapping:
                return subject_mapping[compliance_subject], subject_id
    return None


class AutomationRunner:
    def __init__(
        self,
        session: AsyncSession,
        repository: AutomationRepository,
    ) -> None:
        self._session = session
        self._repository = repository
        self._activity_repository = ActivityRepository(session)

    async def run_trigger(
        self,
        trigger: AutomationTrigger,
        *,
        executed_by_id: uuid.UUID | None,
        simulate: bool = True,
        worker_instance_id: str | None = None,
    ) -> AutomationRunResult:
        now = datetime.now(UTC)
        action_type = AutomationActionType(trigger.action_type)
        target_type = AutomationTargetType(trigger.target_type) if trigger.target_type else None

        run = await self._repository.create_run(
            {
                "trigger_id": trigger.id,
                "status": AutomationRunStatus.RUNNING.value,
                "started_at": now,
                "target_type": trigger.target_type,
                "target_id": trigger.target_id,
                "action_type": trigger.action_type,
                "executed_by_id": executed_by_id,
                "worker_instance_id": worker_instance_id,
            }
        )

        created_work_item_id: uuid.UUID | None = None
        created_comment_id: uuid.UUID | None = None
        created_activity_event_id: uuid.UUID | None = None
        message = ""
        result_details: dict[str, Any] = {}

        try:
            if action_type == AutomationActionType.SEND_NOTIFICATION:
                (
                    status,
                    result_summary,
                    result_details,
                    created_work_item_id,
                    created_comment_id,
                    created_activity_event_id,
                    message,
                ) = await self._send_notification(
                    trigger=trigger,
                    run=run,
                    target_type=target_type,
                    config=trigger.action_config or {},
                    executed_by_id=executed_by_id,
                    automation_simulate=simulate,
                )
            elif simulate:
                status = AutomationRunStatus.SIMULATED
                result_summary = f"Simulated {action_type.value} for trigger {trigger.name}"
                result_details = {
                    "simulate": True,
                    "action_type": action_type.value,
                    "target_type": trigger.target_type,
                    "target_id": str(trigger.target_id) if trigger.target_id else None,
                    "action_config": trigger.action_config,
                    "would_execute": action_type.value in {a.value for a in MVP_SAFE_ACTION_TYPES},
                }
                message = "Simulation completed. No business objects were created."
            elif action_type not in MVP_SAFE_ACTION_TYPES:
                status = AutomationRunStatus.SKIPPED
                result_summary = "Action type is not implemented in MVP."
                result_details = {"action_type": action_type.value}
                message = result_summary
            else:
                (
                    status,
                    result_summary,
                    result_details,
                    created_work_item_id,
                    created_comment_id,
                    created_activity_event_id,
                    message,
                ) = await self._execute_safe_action(
                    trigger=trigger,
                    action_type=action_type,
                    target_type=target_type,
                    executed_by_id=executed_by_id,
                )
        except Exception as exc:
            status = AutomationRunStatus.FAILED
            result_summary = "Automation run failed"
            result_details = {"error_type": type(exc).__name__}
            message = str(exc)
            run = await self._repository.update_run(
                run,
                {
                    "status": status.value,
                    "finished_at": datetime.now(UTC),
                    "result_summary": result_summary,
                    "result_details": result_details,
                    "error_message": message,
                },
            )
            await self._repository.touch_trigger_run_times(trigger, run_at=now)
            if trigger.schedule_id:
                schedule = await self._repository.get_schedule_by_id(trigger.schedule_id)
                if schedule:
                    await self._repository.touch_schedule_run_time(schedule, run_at=now)
            return AutomationRunResult(
                run=AutomationRunRead.model_validate(run),
                message=message,
            )

        finished_at = datetime.now(UTC)
        run = await self._repository.update_run(
            run,
            {
                "status": status.value,
                "finished_at": finished_at,
                "result_summary": result_summary,
                "result_details": result_details,
                "error_message": None if status != AutomationRunStatus.FAILED else message,
            },
        )
        await self._repository.touch_trigger_run_times(trigger, run_at=finished_at)
        if trigger.schedule_id:
            schedule = await self._repository.get_schedule_by_id(trigger.schedule_id)
            if schedule:
                await self._repository.touch_schedule_run_time(schedule, run_at=finished_at)

        return AutomationRunResult(
            run=AutomationRunRead.model_validate(run),
            created_work_item_id=created_work_item_id,
            created_comment_id=created_comment_id,
            created_activity_event_id=created_activity_event_id,
            message=message,
        )

    async def _execute_safe_action(
        self,
        *,
        trigger: AutomationTrigger,
        action_type: AutomationActionType,
        target_type: AutomationTargetType | None,
        executed_by_id: uuid.UUID | None,
    ) -> tuple[
        AutomationRunStatus,
        str,
        dict[str, Any],
        uuid.UUID | None,
        uuid.UUID | None,
        uuid.UUID | None,
        str,
    ]:
        config = trigger.action_config or {}

        if action_type == AutomationActionType.CREATE_WORK_ITEM:
            return await self._create_work_item(trigger, target_type, config, executed_by_id)
        if action_type == AutomationActionType.ADD_COMMENT:
            return await self._add_comment(trigger, target_type, config, executed_by_id)
        if action_type == AutomationActionType.CREATE_ACTIVITY_EVENT:
            return await self._create_activity_event(trigger, target_type, config, executed_by_id)
        if action_type == AutomationActionType.SEND_NOTIFICATION:
            raise ValueError("send_notification must be handled via _send_notification")

        return (
            AutomationRunStatus.SKIPPED,
            "Action type is not implemented in MVP.",
            {"action_type": action_type.value},
            None,
            None,
            None,
            "Action type is not implemented in MVP.",
        )

    async def _create_work_item(
        self,
        trigger: AutomationTrigger,
        target_type: AutomationTargetType | None,
        config: dict[str, Any],
        executed_by_id: uuid.UUID | None,
    ) -> tuple[
        AutomationRunStatus,
        str,
        dict[str, Any],
        uuid.UUID | None,
        uuid.UUID | None,
        uuid.UUID | None,
        str,
    ]:
        if target_type is None or trigger.target_id is None:
            raise ValueError("create_work_item requires target_type and target_id")

        title = config.get("title") or f"Automation task: {trigger.name}"
        description = config.get("description")
        priority = WorkItemPriority(config.get("priority", WorkItemPriority.MEDIUM.value))
        item_type = WorkItemType(config.get("type", WorkItemType.TASK.value))
        due_in_days = config.get("due_in_days")
        due_date = date.today() + timedelta(days=int(due_in_days)) if due_in_days else None

        work_item_data: dict[str, Any] = {
            "title": title,
            "description": description,
            "type": item_type,
            "status": WorkItemStatus.BACKLOG,
            "priority": priority,
            "reporter_id": executed_by_id,
            "due_date": due_date,
        }
        if config.get("assignee_id"):
            work_item_data["assignee_id"] = uuid.UUID(str(config["assignee_id"]))

        if target_type == AutomationTargetType.DATA_PRODUCT:
            work_item_data["data_product_id"] = trigger.target_id
        elif target_type in (AutomationTargetType.PROJECT, AutomationTargetType.INTERNAL_PROJECT):
            work_item_data["project_id"] = trigger.target_id
        elif target_type == AutomationTargetType.TEAM:
            work_item_data["team_id"] = trigger.target_id
        elif target_type == AutomationTargetType.CAPABILITY:
            work_item_data["capability_id"] = trigger.target_id

        work_item = WorkItem(**work_item_data)
        self._session.add(work_item)
        await self._session.commit()
        await self._session.refresh(work_item)

        return (
            AutomationRunStatus.SUCCEEDED,
            f"Created work item: {work_item.title}",
            {"work_item_id": str(work_item.id), "title": work_item.title},
            work_item.id,
            None,
            None,
            f"Work item created: {work_item.title}",
        )

    async def _add_comment(
        self,
        trigger: AutomationTrigger,
        target_type: AutomationTargetType | None,
        config: dict[str, Any],
        executed_by_id: uuid.UUID | None,
    ) -> tuple[
        AutomationRunStatus,
        str,
        dict[str, Any],
        uuid.UUID | None,
        uuid.UUID | None,
        uuid.UUID | None,
        str,
    ]:
        if target_type is None or trigger.target_id is None:
            raise ValueError("add_comment requires target_type and target_id")
        if target_type not in COMMENT_TARGET_TYPES:
            return (
                AutomationRunStatus.SKIPPED,
                f"Comments are not supported for target type {target_type.value}",
                {"target_type": target_type.value},
                None,
                None,
                None,
                f"Comments are not supported for target type {target_type.value}",
            )

        body = config.get("body") or f"Automation reminder from {trigger.name}"
        comment_data: dict[str, Any] = {
            "body": body,
            "author_id": executed_by_id,
        }
        if target_type == AutomationTargetType.DATA_PRODUCT:
            comment_data["data_product_id"] = trigger.target_id
        elif target_type == AutomationTargetType.WORK_ITEM:
            comment_data["work_item_id"] = trigger.target_id
        elif target_type in (AutomationTargetType.PROJECT, AutomationTargetType.INTERNAL_PROJECT):
            comment_data["project_id"] = trigger.target_id

        comment = Comment(**comment_data)
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)

        return (
            AutomationRunStatus.SUCCEEDED,
            "Comment added",
            {"comment_id": str(comment.id), "body": body},
            None,
            comment.id,
            None,
            "Comment added successfully",
        )

    async def _create_activity_event(
        self,
        trigger: AutomationTrigger,
        target_type: AutomationTargetType | None,
        config: dict[str, Any],
        executed_by_id: uuid.UUID | None,
    ) -> tuple[
        AutomationRunStatus,
        str,
        dict[str, Any],
        uuid.UUID | None,
        uuid.UUID | None,
        uuid.UUID | None,
        str,
    ]:
        if target_type is None or trigger.target_id is None:
            raise ValueError("create_activity_event requires target_type and target_id")

        session_entity = None
        if target_type == AutomationTargetType.COMPLIANCE_CHECK:
            session_entity = await self._session.get(ComplianceCheck, trigger.target_id)

        resolved = _resolve_activity_entity(target_type, trigger.target_id, session_entity)
        if resolved is None:
            return (
                AutomationRunStatus.SKIPPED,
                f"Activity events are not supported for target type {target_type.value}",
                {"target_type": target_type.value},
                None,
                None,
                None,
                f"Activity events are not supported for target type {target_type.value}",
            )

        entity_type, entity_id = resolved
        title = config.get("title") or "Automation executed"
        description = config.get("description") or trigger.name

        event = await self._activity_repository.create(
            ActivityEventCreateInternal(
                entity_type=entity_type,
                entity_id=entity_id,
                action=ActivityAction.UPDATED,
                actor_id=executed_by_id,
                title=title,
                description=description,
                details={"trigger_id": str(trigger.id), "trigger_name": trigger.name},
            )
        )

        return (
            AutomationRunStatus.SUCCEEDED,
            f"Activity event created: {title}",
            {"activity_event_id": str(event.id), "title": title},
            None,
            None,
            event.id,
            f"Activity event created: {title}",
        )

    async def _send_notification(
        self,
        *,
        trigger: AutomationTrigger,
        run: AutomationRun,
        target_type: AutomationTargetType | None,
        config: dict[str, Any],
        executed_by_id: uuid.UUID | None,
        automation_simulate: bool,
    ) -> tuple[
        AutomationRunStatus,
        str,
        dict[str, Any],
        uuid.UUID | None,
        uuid.UUID | None,
        uuid.UUID | None,
        str,
    ]:
        notification_service = NotificationService(
            NotificationRepository(self._session),
            build_activity_service(self._session),
            self._session,
        )

        entity_type = None
        entity_id = trigger.target_id
        if target_type is not None and target_type in AUTOMATION_TARGET_TO_ENTITY:
            entity_type = AUTOMATION_TARGET_TO_ENTITY[target_type]

        channel_id = uuid.UUID(str(config["channel_id"])) if config.get("channel_id") else None
        template_id = uuid.UUID(str(config["template_id"])) if config.get("template_id") else None
        recipient_type = config.get("recipient_type")
        recipient_value = config.get("recipient_value")
        priority = NotificationPriority(config.get("priority", NotificationPriority.NORMAL.value))
        event_type = NotificationEventType(
            config.get("event_type", NotificationEventType.AUTOMATION_RUN.value)
        )
        settings = get_settings()
        notify_simulate = bool(config.get("simulate", True))
        if automation_simulate:
            notify_simulate = True
        elif not settings.notification_external_delivery_enabled:
            channel = None
            if channel_id:
                channel = await NotificationRepository(self._session).get_channel_by_id(channel_id)
            channel_type = channel.channel_type if channel else NotificationChannelType.IN_APP.value
            if is_external_channel_type(channel_type):
                notify_simulate = True

        subject = config.get("subject")
        body = config.get("body") or f"Automation notification from {trigger.name}"

        context: dict[str, Any] = {
            "title": subject or trigger.name,
            "status": trigger.status,
            "event_type": event_type.value,
        }
        if entity_type and entity_id:
            context["entity_type"] = entity_type
            context["entity_id"] = str(entity_id)

        message_payload = NotificationMessageCreate(
            channel_id=channel_id,
            template_id=template_id,
            status=NotificationMessageStatus.QUEUED,
            priority=priority,
            event_type=event_type,
            subject=subject,
            body=body,
            recipient_type=NotificationRecipientType(recipient_type) if recipient_type else None,
            recipient_value=recipient_value,
            entity_type=entity_type,
            entity_id=entity_id,
            automation_run_id=run.id,
        )

        send_result = await notification_service.create_and_send_message(
            message_payload,
            simulate=notify_simulate,
            context=context,
            created_by_id=executed_by_id,
        )

        run_status = (
            AutomationRunStatus.SIMULATED
            if automation_simulate or notify_simulate
            else AutomationRunStatus.SUCCEEDED
        )
        if send_result.message.status == "failed":
            run_status = AutomationRunStatus.FAILED

        result_summary = send_result.result_summary
        result_details = {
            "notification_message_id": str(send_result.message.id),
            "delivery_attempt_id": str(send_result.delivery_attempt.id),
            "simulated": notify_simulate,
        }
        message = result_summary
        return run_status, result_summary, result_details, None, None, None, message
