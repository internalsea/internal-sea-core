import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class FileStorageNotFoundError(NotFoundError):
    def __init__(self, storage_id: uuid.UUID) -> None:
        super().__init__(f"File storage not found: {storage_id}")


class FileAssetNotFoundError(NotFoundError):
    def __init__(self, file_id: uuid.UUID) -> None:
        super().__init__(f"File not found: {file_id}")


class FileAttachmentNotFoundError(NotFoundError):
    def __init__(self, attachment_id: uuid.UUID) -> None:
        super().__init__(f"File attachment not found: {attachment_id}")


class FileAttachmentConflictError(ConflictError):
    def __init__(self, message: str = "File is already attached to this entity") -> None:
        super().__init__(message)


class UnsupportedFileEntityTypeError(ValidationError):
    def __init__(self, entity_type: str) -> None:
        super().__init__(f"Unsupported file entity type: {entity_type}")


class FileEntityNotFoundError(NotFoundError):
    def __init__(self, entity_type: str, entity_id: uuid.UUID) -> None:
        super().__init__(f"{entity_type} not found: {entity_id}")


class FileStorageConflictError(ConflictError):
    def __init__(self, message: str = "File storage is in use and cannot be deleted") -> None:
        super().__init__(message)
