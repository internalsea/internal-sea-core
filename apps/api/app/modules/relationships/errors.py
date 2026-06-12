import uuid

from app.core.errors import ConflictError, NotFoundError, ValidationError


class EntityLinkNotFoundError(NotFoundError):
    def __init__(self, link_id: uuid.UUID) -> None:
        super().__init__(f"Entity link {link_id} not found")


class EntityLinkConflictError(ConflictError):
    def __init__(self, message: str = "Relationship already exists") -> None:
        super().__init__(message)


class UnsupportedEntityTypeError(ValidationError):
    def __init__(self, entity_type: str) -> None:
        super().__init__(f"Entity type '{entity_type}' is not supported yet")


class EntityNotFoundError(NotFoundError):
    def __init__(self, entity_type: str, entity_id: uuid.UUID) -> None:
        super().__init__(f"{entity_type} {entity_id} not found")


class InvalidEntityLinkError(ValidationError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
