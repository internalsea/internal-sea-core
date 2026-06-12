import uuid

from app.core.errors import ConflictError, NotFoundError


class TeamNotFoundError(NotFoundError):
    """Raised when a team does not exist."""

    def __init__(self, team_id: uuid.UUID) -> None:
        super().__init__(f"Team {team_id} not found")


class TeamConflictError(ConflictError):
    """Raised when a team operation conflicts with existing data."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
