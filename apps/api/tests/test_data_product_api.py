import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import DataProductStatus, DataProductType, QualityStatus
from app.main import create_app
from app.modules.data_products.router import get_data_product_service
from app.modules.data_products.schemas import DataProductRead, PaginatedDataProductList
from fastapi.testclient import TestClient


@pytest.fixture
def mock_data_product_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_data_product_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_data_product_service] = lambda: mock_data_product_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_product() -> DataProductRead:
    now = datetime.now(UTC)
    return DataProductRead(
        id=uuid.uuid4(),
        name="Sales Dashboard",
        description="Executive sales overview",
        type=DataProductType.DASHBOARD,
        status=DataProductStatus.ACTIVE,
        quality_status=QualityStatus.GOOD,
        business_domain_id=None,
        business_owner_id=None,
        technical_owner_id=None,
        capability_id=None,
        team_id=None,
        refresh_frequency="daily",
        source_systems="CRM",
        consumers="Leadership",
        documentation_url="https://example.com/docs",
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_data_products_path(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/data-products" in paths
    assert "/api/v1/data-products/{data_product_id}" in paths


def test_list_data_products(api_client: TestClient, mock_data_product_service: AsyncMock) -> None:
    product = _sample_product()
    mock_data_product_service.list_data_products.return_value = PaginatedDataProductList(
        items=[product],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/data-products")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Sales Dashboard"


def test_create_data_product(api_client: TestClient, mock_data_product_service: AsyncMock) -> None:
    product = _sample_product()
    mock_data_product_service.create_data_product.return_value = product

    response = api_client.post(
        "/api/v1/data-products",
        json={"name": "Sales Dashboard", "type": "dashboard", "status": "active"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Sales Dashboard"


def test_get_data_product(api_client: TestClient, mock_data_product_service: AsyncMock) -> None:
    product = _sample_product()
    mock_data_product_service.get_data_product.return_value = product

    response = api_client.get(f"/api/v1/data-products/{product.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(product.id)


def test_update_data_product(api_client: TestClient, mock_data_product_service: AsyncMock) -> None:
    product = _sample_product()
    updated = product.model_copy(update={"status": "deprecated"})
    mock_data_product_service.update_data_product.return_value = updated

    response = api_client.patch(
        f"/api/v1/data-products/{product.id}",
        json={"status": "deprecated"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "deprecated"


def test_delete_data_product(api_client: TestClient, mock_data_product_service: AsyncMock) -> None:
    product_id = uuid.uuid4()
    mock_data_product_service.delete_data_product.return_value = None

    response = api_client.delete(f"/api/v1/data-products/{product_id}")

    assert response.status_code == 204
