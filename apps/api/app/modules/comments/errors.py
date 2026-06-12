import uuid

from app.core.errors import NotFoundError


class CommentNotFoundError(NotFoundError):
    """Raised when a comment does not exist."""

    def __init__(self, comment_id: uuid.UUID) -> None:
        super().__init__(f"Comment {comment_id} not found")
