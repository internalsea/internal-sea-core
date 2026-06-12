from datetime import datetime

from pydantic import BaseModel, Field


class WorkerStatus(BaseModel):
    worker_enabled: bool
    worker_instance_id: str
    poll_interval_seconds: int
    batch_size: int
    automation_due_count: int
    notification_due_count: int
    last_checked_at: datetime | None = None


class DueWorkSummary(BaseModel):
    due_automation_triggers: int
    due_notifications: int
    locked_automation_triggers: int
    locked_notifications: int


class WorkerCycleResult(BaseModel):
    worker_instance_id: str
    started_at: datetime
    finished_at: datetime
    due_triggers_found: int
    automation_runs_created: int
    notification_messages_found: int
    notifications_processed: int
    failures: list[str] = Field(default_factory=list)
    summary: str
