import uuid

from app.core.errors import ConflictError, NotFoundError


class CapabilityNotFoundError(NotFoundError):
    """Raised when a capability does not exist."""

    def __init__(self, capability_id: uuid.UUID) -> None:
        super().__init__(f"Capability {capability_id} not found")


class CapabilityConflictError(ConflictError):
    """Raised when a capability operation conflicts with existing data."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
