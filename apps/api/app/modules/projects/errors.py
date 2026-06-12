import uuid

from app.core.errors import NotFoundError


class ProjectNotFoundError(NotFoundError):
    """Raised when a project does not exist."""

    def __init__(self, project_id: uuid.UUID) -> None:
        super().__init__(f"Project {project_id} not found")
