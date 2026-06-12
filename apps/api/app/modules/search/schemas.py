import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SearchResultType(StrEnum):
    DATA_PRODUCT = "data_product"
    WORK_ITEM = "work_item"
    PROJECT = "project"
    INTERNAL_PROJECT = "internal_project"
    PERSON = "person"
    TEAM = "team"
    CAPABILITY = "capability"
    FILE = "file"
    POLICY = "policy"
    COMPLIANCE_CHECK = "compliance_check"
    AUTOMATION_TRIGGER = "automation_trigger"
    NOTIFICATION_TEMPLATE = "notification_template"
    NOTIFICATION_MESSAGE = "notification_message"


DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 50
MIN_SEARCH_QUERY_LENGTH = 2


class SearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: SearchResultType
    title: str
    description: str | None = None
    status: str | None = None
    secondary_status: str | None = None
    url: str
    matched_field: str | None = None
    updated_at: datetime | None = None


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchResult]


class EntityLookupResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: SearchResultType
    title: str
    description: str | None = None
    status: str | None = None
    secondary_status: str | None = None
    url: str


class SearchFilters(BaseModel):
    q: str
    types: list[SearchResultType] | None = None
    limit: int = Field(default=DEFAULT_SEARCH_LIMIT, ge=1, le=MAX_SEARCH_LIMIT)

    @field_validator("q")
    @classmethod
    def validate_query(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Query must not be empty")
        if len(stripped) < MIN_SEARCH_QUERY_LENGTH:
            raise ValueError("Query must be at least 2 characters")
        return stripped
