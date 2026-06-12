import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class NotificationChannelNotFoundError(NotFoundError):
    def __init__(self, channel_id: uuid.UUID) -> None:
        super().__init__(f"Notification channel not found: {channel_id}")


class NotificationTemplateNotFoundError(NotFoundError):
    def __init__(self, template_id: uuid.UUID) -> None:
        super().__init__(f"Notification template not found: {template_id}")


class NotificationPreferenceNotFoundError(NotFoundError):
    def __init__(self, preference_id: uuid.UUID) -> None:
        super().__init__(f"Notification preference not found: {preference_id}")


class NotificationMessageNotFoundError(NotFoundError):
    def __init__(self, message_id: uuid.UUID) -> None:
        super().__init__(f"Notification message not found: {message_id}")


class NotificationConflictError(ConflictError):
    def __init__(self, message: str = "Notification operation conflict") -> None:
        super().__init__(message)


class NotificationValidationError(ValidationError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnsupportedNotificationEntityTypeError(ValidationError):
    def __init__(self, entity_type: str) -> None:
        super().__init__(f"Unsupported notification entity type: {entity_type}")


class NotificationEntityNotFoundError(NotFoundError):
    def __init__(self, entity_type: str, entity_id: uuid.UUID) -> None:
        super().__init__(f"{entity_type} not found: {entity_id}")


class NotificationDeliveryError(ValidationError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
