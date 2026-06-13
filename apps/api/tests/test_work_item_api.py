import uuid
from datetime import UTC, date, datetime
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.main import create_app
from app.modules.work_items.router import get_work_item_service
from app.modules.work_items.schemas import (
    PaginatedWorkItemList,
    WorkItemBoardColumn,
    WorkItemBoardResponse,
    WorkItemRead,
)
from fastapi.testclient import TestClient


@pytest.fixture
def mock_work_item_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_work_item_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_work_item_service] = lambda: mock_work_item_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_work_item() -> WorkItemRead:
    now = datetime.now(UTC)
    return WorkItemRead(
        id=uuid.uuid4(),
        title="Fix dashboard refresh",
        description="Investigate stale cache",
        type=WorkItemType.BUG,
        status=WorkItemStatus.IN_PROGRESS,
        priority=WorkItemPriority.HIGH,
        assignee_id=None,
        reporter_id=None,
        data_product_id=None,
        capability_id=None,
        team_id=None,
        project_id=None,
        due_date=date(2026, 6, 15),
        estimate_points=3,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_work_items_path(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/work-items" in paths
    assert "/api/v1/work-items/board" in paths
    assert "/api/v1/work-items/{work_item_id}" in paths


def test_list_work_items(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item = _sample_work_item()
    mock_work_item_service.list_work_items.return_value = PaginatedWorkItemList(
        items=[item],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/work-items")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Fix dashboard refresh"


def test_get_work_item_board(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item = _sample_work_item()
    mock_work_item_service.get_work_item_board.return_value = WorkItemBoardResponse(
        columns=[
            WorkItemBoardColumn(
                status=WorkItemStatus.IN_PROGRESS,
                title="In Progress",
                items=[item],
                count=1,
            )
        ]
    )

    response = api_client.get("/api/v1/work-items/board")

    assert response.status_code == 200
    data = response.json()
    assert data["columns"][0]["count"] == 1
    assert data["columns"][0]["items"][0]["title"] == "Fix dashboard refresh"


def test_create_work_item(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item = _sample_work_item()
    mock_work_item_service.create_work_item.return_value = item

    response = api_client.post(
        "/api/v1/work-items",
        json={"title": "Fix dashboard refresh", "type": "bug", "priority": "high"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Fix dashboard refresh"


def test_get_work_item(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item = _sample_work_item()
    mock_work_item_service.get_work_item.return_value = item

    response = api_client.get(f"/api/v1/work-items/{item.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(item.id)


def test_update_work_item(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item = _sample_work_item()
    updated = item.model_copy(update={"status": WorkItemStatus.REVIEW})
    mock_work_item_service.update_work_item.return_value = updated

    response = api_client.patch(
        f"/api/v1/work-items/{item.id}",
        json={"status": "review"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "review"


def test_list_work_items_with_project_filter(
    api_client: TestClient,
    mock_work_item_service: AsyncMock,
) -> None:
    item = _sample_work_item()
    mock_work_item_service.list_work_items.return_value = PaginatedWorkItemList(
        items=[item],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )
    project_id = uuid.uuid4()

    response = api_client.get(f"/api/v1/work-items?project_id={project_id}")

    assert response.status_code == 200
    mock_work_item_service.list_work_items.assert_awaited_once()
    call_kwargs = mock_work_item_service.list_work_items.await_args.kwargs
    assert call_kwargs["filters"].project_id == project_id


def test_delete_work_item(api_client: TestClient, mock_work_item_service: AsyncMock) -> None:
    item_id = uuid.uuid4()
    mock_work_item_service.delete_work_item.return_value = None

    response = api_client.delete(f"/api/v1/work-items/{item_id}")

    assert response.status_code == 204
