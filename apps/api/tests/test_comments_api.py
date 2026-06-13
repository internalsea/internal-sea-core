import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.main import create_app
from app.modules.comments.router import get_comment_service
from app.modules.comments.schemas import CommentListResponse, CommentRead
from fastapi.testclient import TestClient


@pytest.fixture
def mock_comment_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_comment_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_comment_service] = lambda: mock_comment_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_comment() -> CommentRead:
    now = datetime.now(UTC)
    return CommentRead(
        id=uuid.uuid4(),
        body="Looks good.",
        author_id=None,
        data_product_id=uuid.uuid4(),
        work_item_id=None,
        project_id=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_comments_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/data-products/{data_product_id}/comments" in paths
    assert "/api/v1/work-items/{work_item_id}/comments" in paths
    assert "/api/v1/projects/{project_id}/comments" in paths
    assert "/api/v1/internal-projects/{project_id}/comments" in paths
    assert "/api/v1/comments/{comment_id}" in paths


def test_list_data_product_comments(
    api_client: TestClient, mock_comment_service: AsyncMock
) -> None:
    comment = _sample_comment()
    mock_comment_service.list_data_product_comments.return_value = CommentListResponse(
        items=[comment],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )
    response = api_client.get(f"/api/v1/data-products/{comment.data_product_id}/comments")
    assert response.status_code == 200
    assert response.json()["total"] == 1
