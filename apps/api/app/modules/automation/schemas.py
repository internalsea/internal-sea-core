import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.enums import (
    AutomationActionType,
    AutomationRunStatus,
    AutomationStatus,
    AutomationTargetType,
    AutomationTriggerType,
    ScheduleFrequency,
)


class AutomationScheduleBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    frequency: ScheduleFrequency = ScheduleFrequency.MONTHLY
    timezone: str | None = "UTC"
    start_at: datetime | None = None
    end_at: datetime | None = None
    next_run_at: datetime | None = None
    cron_expression: str | None = None
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_dates_and_cron(self) -> AutomationScheduleBase:
        if self.start_at and self.end_at and self.end_at < self.start_at:
            raise ValueError("end_at must not be before start_at")
        if self.cron_expression and self.frequency != ScheduleFrequency.CUSTOM:
            raise ValueError("cron_expression is only allowed when frequency is custom")
        return self


class AutomationScheduleCreate(AutomationScheduleBase):
    pass


class AutomationScheduleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    frequency: ScheduleFrequency | None = None
    timezone: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    next_run_at: datetime | None = None
    cron_expression: str | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_dates_and_cron(self) -> AutomationScheduleUpdate:
        if self.start_at and self.end_at and self.end_at < self.start_at:
            raise ValueError("end_at must not be before start_at")
        if self.cron_expression and self.frequency not in (None, ScheduleFrequency.CUSTOM):
            raise ValueError("cron_expression is only allowed when frequency is custom")
        return self


class AutomationScheduleRead(AutomationScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    last_run_at: datetime | None
    created_by_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class AutomationScheduleListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    frequency: str
    next_run_at: datetime | None
    last_run_at: datetime | None
    is_active: bool
    updated_at: datetime


class AutomationScheduleListResponse(BaseModel):
    items: list[AutomationScheduleListItem]
    total: int
    page: int
    page_size: int
    pages: int


class AutomationTriggerBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: AutomationStatus = AutomationStatus.DRAFT
    trigger_type: AutomationTriggerType = AutomationTriggerType.SCHEDULE
    action_type: AutomationActionType
    schedule_id: uuid.UUID | None = None
    target_type: AutomationTargetType | None = None
    target_id: uuid.UUID | None = None
    conditions: dict[str, Any] | None = None
    action_config: dict[str, Any] | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_target_and_schedule(self) -> AutomationTriggerBase:
        if (self.target_type is None) != (self.target_id is None):
            raise ValueError("target_type and target_id must be provided together")
        if self.trigger_type == AutomationTriggerType.SCHEDULE and self.schedule_id is None:
            raise ValueError("schedule_id is required for schedule triggers")
        return self


class AutomationTriggerCreate(AutomationTriggerBase):
    pass


class AutomationTriggerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: AutomationStatus | None = None
    trigger_type: AutomationTriggerType | None = None
    action_type: AutomationActionType | None = None
    schedule_id: uuid.UUID | None = None
    target_type: AutomationTargetType | None = None
    target_id: uuid.UUID | None = None
    conditions: dict[str, Any] | None = None
    action_config: dict[str, Any] | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value


class AutomationTriggerRead(AutomationTriggerBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_by_id: uuid.UUID | None
    last_run_at: datetime | None
    next_run_at: datetime | None
    locked_at: datetime | None = None
    locked_by: str | None = None
    lock_expires_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AutomationTriggerListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    status: str
    trigger_type: str
    action_type: str
    schedule_id: uuid.UUID | None
    target_type: str | None
    target_id: uuid.UUID | None
    last_run_at: datetime | None
    next_run_at: datetime | None
    updated_at: datetime


class AutomationTriggerListResponse(BaseModel):
    items: list[AutomationTriggerListItem]
    total: int
    page: int
    page_size: int
    pages: int


class AutomationTriggerFilters(BaseModel):
    search: str | None = None
    status: AutomationStatus | None = None
    trigger_type: AutomationTriggerType | None = None
    action_type: AutomationActionType | None = None
    target_type: AutomationTargetType | None = None
    target_id: uuid.UUID | None = None
    schedule_id: uuid.UUID | None = None


class AutomationRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trigger_id: uuid.UUID
    status: str
    started_at: datetime | None
    finished_at: datetime | None
    target_type: str | None
    target_id: uuid.UUID | None
    action_type: str | None
    result_summary: str | None
    result_details: dict[str, Any] | None
    error_message: str | None
    executed_by_id: uuid.UUID | None
    worker_instance_id: str | None = None
    created_at: datetime
    updated_at: datetime


class AutomationRunListResponse(BaseModel):
    items: list[AutomationRunRead]
    total: int
    page: int
    page_size: int
    pages: int


class AutomationRunRequest(BaseModel):
    simulate: bool = True


class AutomationRunResult(BaseModel):
    run: AutomationRunRead
    created_work_item_id: uuid.UUID | None = None
    created_comment_id: uuid.UUID | None = None
    created_activity_event_id: uuid.UUID | None = None
    message: str


class EntityAutomationsResponse(BaseModel):
    target_type: AutomationTargetType
    target_id: uuid.UUID
    triggers: list[AutomationTriggerListItem]
    total: int


class AutomationOverview(BaseModel):
    schedules_total: int = 0
    schedules_active: int = 0
    triggers_total: int = 0
    triggers_active: int = 0
    triggers_paused: int = 0
    runs_total: int = 0
    runs_succeeded: int = 0
    runs_failed: int = 0
    runs_simulated: int = 0
    next_runs_count: int = 0
