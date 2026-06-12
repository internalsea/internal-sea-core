from pydantic import BaseModel, Field

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


class PaginationParams(BaseModel):
    """Query parameters for paginated list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description="Number of items per page",
    )

    @property
    def offset(self) -> int:
        page, page_size = normalize_pagination(self.page, self.page_size)
        return (page - 1) * page_size


def normalize_pagination(page: int, page_size: int) -> tuple[int, int]:
    """Clamp page and page_size to valid bounds."""
    normalized_page = max(page, 1)
    normalized_page_size = min(max(page_size, 1), MAX_PAGE_SIZE)
    return normalized_page, normalized_page_size


def calculate_pages(total: int, page_size: int) -> int:
    """Return total number of pages for a result set."""
    if total <= 0:
        return 0
    _, normalized_page_size = normalize_pagination(1, page_size)
    return (total + normalized_page_size - 1) // normalized_page_size
