import re
import uuid
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.enums import (
    NotificationChannelStatus,
    NotificationChannelType,
    NotificationEventType,
    NotificationMessageStatus,
    NotificationPriority,
    NotificationRecipientType,
    NotificationTemplateStatus,
)

SECRET_KEY_PATTERN = re.compile(
    r"(token|secret|password|api[_-]?key)",
    re.IGNORECASE,
)


def _reject_secret_keys(config: dict[str, Any] | None) -> None:
    if not config:
        return
    for key in config:
        if SECRET_KEY_PATTERN.search(key):
            raise ValueError(
                f"provider_config must not contain secret-like keys (found: {key}). "
                "Use environment variables or a future secret manager."
            )


class NotificationChannelBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    channel_type: NotificationChannelType
    status: NotificationChannelStatus = NotificationChannelStatus.DRAFT
    description: str | None = None
    endpoint_url: str | None = None
    default_recipient: str | None = None
    provider_config: dict[str, Any] | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @field_validator("provider_config")
    @classmethod
    def validate_provider_config(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        _reject_secret_keys(value)
        return value


class NotificationChannelCreate(NotificationChannelBase):
    pass


class NotificationChannelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    channel_type: NotificationChannelType | None = None
    status: NotificationChannelStatus | None = None
    description: str | None = None
    endpoint_url: str | None = None
    default_recipient: str | None = None
    provider_config: dict[str, Any] | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @field_validator("provider_config")
    @classmethod
    def validate_provider_config(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        _reject_secret_keys(value)
        return value


class NotificationChannelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    channel_type: str
    status: str
    description: str | None
    endpoint_url: str | None
    default_recipient: str | None
    provider_config: dict[str, Any] | None
    created_by_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class NotificationChannelListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    channel_type: str
    status: str
    default_recipient: str | None
    updated_at: datetime


class NotificationChannelListResponse(BaseModel):
    items: list[NotificationChannelListItem]
    total: int
    page: int
    page_size: int
    pages: int


class NotificationChannelFilters(BaseModel):
    search: str | None = None
    channel_type: NotificationChannelType | None = None
    status: NotificationChannelStatus | None = None


class NotificationTemplateBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    status: NotificationTemplateStatus = NotificationTemplateStatus.DRAFT
    event_type: NotificationEventType | None = None
    subject_template: str | None = None
    body_template: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @field_validator("body_template")
    @classmethod
    def body_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("body_template cannot be empty")
        return value


class NotificationTemplateCreate(NotificationTemplateBase):
    pass


class NotificationTemplateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: NotificationTemplateStatus | None = None
    event_type: NotificationEventType | None = None
    subject_template: str | None = None
    body_template: str | None = None
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name cannot be empty")
        return value

    @field_validator("body_template")
    @classmethod
    def body_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("body_template cannot be empty")
        return value


class NotificationTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    status: str
    event_type: str | None
    subject_template: str | None
    body_template: str
    description: str | None
    created_by_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class NotificationTemplateListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    status: str
    event_type: str | None
    updated_at: datetime


class NotificationTemplateListResponse(BaseModel):
    items: list[NotificationTemplateListItem]
    total: int
    page: int
    page_size: int
    pages: int


class NotificationTemplateFilters(BaseModel):
    search: str | None = None
    status: NotificationTemplateStatus | None = None
    event_type: NotificationEventType | None = None


class NotificationPreferenceBase(BaseModel):
    user_id: uuid.UUID | None = None
    person_id: uuid.UUID | None = None
    channel_type: NotificationChannelType
    event_type: NotificationEventType
    is_enabled: bool = True

    @model_validator(mode="after")
    def require_user_or_person(self) -> Self:
        if self.user_id is None and self.person_id is None:
            raise ValueError("At least one of user_id or person_id must be provided")
        return self


class NotificationPreferenceCreate(NotificationPreferenceBase):
    pass


class NotificationPreferenceUpdate(BaseModel):
    is_enabled: bool | None = None


class NotificationPreferenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID | None
    person_id: uuid.UUID | None
    channel_type: str
    event_type: str
    is_enabled: bool
    created_at: datetime
    updated_at: datetime


class NotificationMessageBase(BaseModel):
    channel_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    status: NotificationMessageStatus = NotificationMessageStatus.DRAFT
    priority: NotificationPriority = NotificationPriority.NORMAL
    event_type: NotificationEventType = NotificationEventType.MANUAL
    subject: str | None = None
    body: str
    recipient_type: NotificationRecipientType | None = None
    recipient_value: str | None = None
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    automation_run_id: uuid.UUID | None = None
    scheduled_at: datetime | None = None
    metadata: dict[str, Any] | None = None

    @field_validator("body")
    @classmethod
    def body_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("body cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_recipient_and_entity(self) -> Self:
        if self.recipient_type is not None and not self.recipient_value:
            raise ValueError("recipient_value is required when recipient_type is provided")
        if self.entity_type is not None and self.entity_id is None:
            raise ValueError("entity_id is required when entity_type is provided")
        if self.entity_id is not None and self.entity_type is None:
            raise ValueError("entity_type is required when entity_id is provided")
        return self


class NotificationMessageCreate(NotificationMessageBase):
    pass


class NotificationMessageUpdate(BaseModel):
    channel_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    status: NotificationMessageStatus | None = None
    priority: NotificationPriority | None = None
    event_type: NotificationEventType | None = None
    subject: str | None = None
    body: str | None = None
    recipient_type: NotificationRecipientType | None = None
    recipient_value: str | None = None
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    automation_run_id: uuid.UUID | None = None
    scheduled_at: datetime | None = None
    metadata: dict[str, Any] | None = None

    @field_validator("body")
    @classmethod
    def body_not_empty(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("body cannot be empty")
        return value


class NotificationMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    channel_id: uuid.UUID | None
    template_id: uuid.UUID | None
    status: str
    priority: str
    event_type: str
    subject: str | None
    body: str
    recipient_type: str | None
    recipient_value: str | None
    entity_type: str | None
    entity_id: uuid.UUID | None
    automation_run_id: uuid.UUID | None
    created_by_id: uuid.UUID | None
    scheduled_at: datetime | None
    sent_at: datetime | None
    simulated_at: datetime | None
    error_message: str | None
    metadata: dict[str, Any] | None = Field(validation_alias="message_metadata")
    created_at: datetime
    updated_at: datetime


class NotificationMessageListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    channel_id: uuid.UUID | None
    template_id: uuid.UUID | None
    status: str
    priority: str
    event_type: str
    subject: str | None
    recipient_type: str | None
    recipient_value: str | None
    entity_type: str | None
    entity_id: uuid.UUID | None
    automation_run_id: uuid.UUID | None
    scheduled_at: datetime | None
    sent_at: datetime | None
    simulated_at: datetime | None
    updated_at: datetime


class NotificationMessageListResponse(BaseModel):
    items: list[NotificationMessageListItem]
    total: int
    page: int
    page_size: int
    pages: int


class NotificationMessageFilters(BaseModel):
    search: str | None = None
    status: NotificationMessageStatus | None = None
    priority: NotificationPriority | None = None
    event_type: NotificationEventType | None = None
    channel_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    automation_run_id: uuid.UUID | None = None


class NotificationDeliveryAttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    message_id: uuid.UUID
    status: str
    attempt_number: int
    provider: str | None
    provider_message_id: str | None
    request_payload: dict[str, Any] | None
    response_payload: dict[str, Any] | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
    worker_instance_id: str | None = None
    created_at: datetime
    updated_at: datetime


class NotificationDeliveryAttemptListResponse(BaseModel):
    items: list[NotificationDeliveryAttemptRead]
    total: int
    page: int
    page_size: int
    pages: int


class NotificationSendRequest(BaseModel):
    simulate: bool = True
    recipient_override: str | None = None
    context: dict[str, Any] | None = None


class NotificationSendResult(BaseModel):
    message: NotificationMessageRead
    delivery_attempt: NotificationDeliveryAttemptRead
    simulated: bool
    result_summary: str


class NotificationRenderRequest(BaseModel):
    template_id: uuid.UUID
    context: dict[str, Any] | None = None


class NotificationRenderResult(BaseModel):
    subject: str | None
    body: str


class NotificationOverview(BaseModel):
    channels_total: int = 0
    channels_active: int = 0
    templates_total: int = 0
    templates_active: int = 0
    messages_total: int = 0
    messages_sent: int = 0
    messages_simulated: int = 0
    messages_failed: int = 0
    delivery_attempts_total: int = 0
    delivery_attempts_failed: int = 0


class EntityNotificationsResponse(BaseModel):
    entity_type: str
    entity_id: uuid.UUID
    messages: list[NotificationMessageListItem]
    total: int
