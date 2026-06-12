import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class AutomationScheduleNotFoundError(NotFoundError):
    def __init__(self, schedule_id: uuid.UUID) -> None:
        super().__init__(f"Automation schedule not found: {schedule_id}")


class AutomationTriggerNotFoundError(NotFoundError):
    def __init__(self, trigger_id: uuid.UUID) -> None:
        super().__init__(f"Automation trigger not found: {trigger_id}")


class AutomationRunNotFoundError(NotFoundError):
    def __init__(self, run_id: uuid.UUID) -> None:
        super().__init__(f"Automation run not found: {run_id}")


class AutomationConflictError(ConflictError):
    def __init__(self, message: str = "Automation operation conflict") -> None:
        super().__init__(message)


class UnsupportedAutomationTargetTypeError(ValidationError):
    def __init__(self, target_type: str) -> None:
        super().__init__(f"Unsupported automation target type: {target_type}")


class AutomationTargetNotFoundError(NotFoundError):
    def __init__(self, target_type: str, target_id: uuid.UUID) -> None:
        super().__init__(f"{target_type} not found: {target_id}")


class UnsupportedAutomationActionError(ValidationError):
    def __init__(self, action_type: str) -> None:
        super().__init__(f"Unsupported automation action type: {action_type}")


class AutomationRunError(ValidationError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
