import uuid

from app.core.errors import NotFoundError


class WorkItemNotFoundError(NotFoundError):
    """Raised when a work item does not exist."""

    def __init__(self, work_item_id: uuid.UUID) -> None:
        super().__init__(f"Work item {work_item_id} not found")
