import uuid

from app.core.errors import NotFoundError


class DataProductNotFoundError(NotFoundError):
    """Raised when a data product does not exist."""

    def __init__(self, data_product_id: uuid.UUID) -> None:
        super().__init__(f"Data product {data_product_id} not found")
