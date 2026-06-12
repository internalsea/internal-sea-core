import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class PerformanceMetricDefinitionNotFoundError(NotFoundError):
    def __init__(self, definition_id: uuid.UUID) -> None:
        super().__init__(f"Performance metric definition not found: {definition_id}")


class PerformanceMetricValueNotFoundError(NotFoundError):
    def __init__(self, value_id: uuid.UUID) -> None:
        super().__init__(f"Performance metric value not found: {value_id}")


class PerformanceMetricConflictError(ConflictError):
    def __init__(self, message: str = "Performance metric operation conflict") -> None:
        super().__init__(message)


class UnsupportedPerformanceSubjectTypeError(ValidationError):
    def __init__(self, subject_type: str) -> None:
        super().__init__(f"Unsupported performance subject type: {subject_type}")


class PerformanceSubjectNotFoundError(NotFoundError):
    def __init__(self, subject_type: str, subject_id: uuid.UUID) -> None:
        super().__init__(f"{subject_type} not found: {subject_id}")


class PerformanceValidationError(ValidationError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
