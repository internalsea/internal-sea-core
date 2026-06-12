import uuid

from app.core.errors import ConflictError, NotFoundError


class PersonNotFoundError(NotFoundError):
    """Raised when a person does not exist."""

    def __init__(self, person_id: uuid.UUID) -> None:
        super().__init__(f"Person {person_id} not found")


class PersonConflictError(ConflictError):
    """Raised when a person operation conflicts with existing data."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
