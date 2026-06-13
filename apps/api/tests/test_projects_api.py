import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import ProjectStatus, ProjectType
from app.main import create_app
from app.modules.internal_projects.router import get_project_service as get_internal_project_service
from app.modules.projects.router import get_project_service
from app.modules.projects.schemas import ProjectListItem, ProjectListResponse, ProjectRead
from fastapi.testclient import TestClient


@pytest.fixture
def mock_project_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_project_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_project_service] = lambda: mock_project_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_project(*, project_type: ProjectType = ProjectType.CLIENT_PROJECT) -> ProjectRead:
    now = datetime.now(UTC)
    return ProjectRead(
        id=uuid.uuid4(),
        name="Finance Data Platform Migration",
        description="Client migration project",
        project_type=project_type,
        status=ProjectStatus.ACTIVE,
        client_name="Example Client",
        account_name=None,
        owner_id=None,
        team_id=None,
        capability_id=None,
        start_date=None,
        target_end_date=None,
        actual_end_date=None,
        budget_amount=None,
        budget_currency="EUR",
        priority=None,
        health_status="healthy",
        delivery_notes=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_projects_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/projects" in paths
    assert "/api/v1/projects/{project_id}" in paths
    assert "/api/v1/projects/{project_id}/summary" in paths
    assert "/api/v1/internal-projects" in paths
    assert "/api/v1/internal-projects/{project_id}" in paths


def test_list_projects(api_client: TestClient, mock_project_service: AsyncMock) -> None:
    project = _sample_project()
    mock_project_service.list_projects.return_value = ProjectListResponse(
        items=[ProjectListItem.model_validate(project)],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/projects")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Finance Data Platform Migration"


def test_create_project(api_client: TestClient, mock_project_service: AsyncMock) -> None:
    project = _sample_project()
    mock_project_service.create_project.return_value = project

    response = api_client.post(
        "/api/v1/projects",
        json={
            "name": "Finance Data Platform Migration",
            "project_type": "client_project",
            "status": "active",
            "client_name": "Example Client",
            "health_status": "healthy",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Finance Data Platform Migration"


def test_get_project(api_client: TestClient, mock_project_service: AsyncMock) -> None:
    project = _sample_project()
    mock_project_service.get_project.return_value = project

    response = api_client.get(f"/api/v1/projects/{project.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(project.id)


def test_create_internal_project_forces_type(
    api_client: TestClient,
    mock_project_service: AsyncMock,
) -> None:
    project = _sample_project(project_type=ProjectType.INTERNAL_PROJECT)
    mock_project_service.create_project.return_value = project

    app = api_client.app
    app.dependency_overrides[get_internal_project_service] = lambda: mock_project_service

    response = api_client.post(
        "/api/v1/internal-projects",
        json={
            "name": "Internal Sea MVP",
            "project_type": "client_project",
            "status": "active",
            "health_status": "healthy",
        },
    )

    assert response.status_code == 201
    create_arg = mock_project_service.create_project.await_args.args[0]
    assert create_arg.project_type == ProjectType.INTERNAL_PROJECT


def test_delete_project(api_client: TestClient, mock_project_service: AsyncMock) -> None:
    project_id = uuid.uuid4()
    mock_project_service.delete_project.return_value = None

    response = api_client.delete(f"/api/v1/projects/{project_id}")

    assert response.status_code == 204
