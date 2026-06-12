import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.enums import SeniorityLevel
from app.main import create_app
from app.modules.people.router import get_person_service
from app.modules.people.schemas import PersonListItem, PersonListResponse, PersonRead


@pytest.fixture
def mock_person_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_person_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_person_service] = lambda: mock_person_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_person() -> PersonRead:
    now = datetime.now(timezone.utc)
    return PersonRead(
        id=uuid.uuid4(),
        full_name="Nikita Rogatov",
        email="nikita@example.com",
        role_title="Partner, Data Engineering and Cloud",
        seniority_level=SeniorityLevel.PARTNER,
        user_id=None,
        team_id=None,
        capability_id=None,
        availability_percent=80,
        location="Netherlands",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_people_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/people" in paths
    assert "/api/v1/people/{person_id}" in paths
    assert "/api/v1/people/{person_id}/summary" in paths


def test_list_people(api_client: TestClient, mock_person_service: AsyncMock) -> None:
    person = _sample_person()
    mock_person_service.list_people.return_value = PersonListResponse(
        items=[PersonListItem.model_validate(person)],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )

    response = api_client.get("/api/v1/people")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["full_name"] == "Nikita Rogatov"


def test_create_person(api_client: TestClient, mock_person_service: AsyncMock) -> None:
    person = _sample_person()
    mock_person_service.create_person.return_value = person

    response = api_client.post(
        "/api/v1/people",
        json={
            "full_name": "Nikita Rogatov",
            "email": "nikita@example.com",
            "role_title": "Partner, Data Engineering and Cloud",
            "seniority_level": "partner",
            "availability_percent": 80,
            "location": "Netherlands",
        },
    )

    assert response.status_code == 201
    assert response.json()["full_name"] == "Nikita Rogatov"


def test_get_person(api_client: TestClient, mock_person_service: AsyncMock) -> None:
    person = _sample_person()
    mock_person_service.get_person.return_value = person

    response = api_client.get(f"/api/v1/people/{person.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(person.id)


def test_deactivate_person(api_client: TestClient, mock_person_service: AsyncMock) -> None:
    person_id = uuid.uuid4()
    mock_person_service.deactivate_person.return_value = None

    response = api_client.delete(f"/api/v1/people/{person_id}")

    assert response.status_code == 204
