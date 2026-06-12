import uuid

from app.modules.search.schemas import SearchResultType


class SearchEntityNotFoundError(Exception):
    def __init__(self, entity_type: SearchResultType, entity_id: uuid.UUID) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type.value} {entity_id} not found")
