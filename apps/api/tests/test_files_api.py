import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.enums import FileAssetType, FileEntityType, FileSensitivity, FileStatus
from app.main import create_app
from app.modules.files.errors import FileAttachmentConflictError
from app.modules.files.router import get_file_service
from app.modules.files.schemas import (
    FileAssetListItem,
    FileAssetListResponse,
    FileAssetRead,
    FileAttachmentRead,
)


@pytest.fixture
def mock_file_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_file_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_file_service] = lambda: mock_file_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _sample_file() -> FileAssetRead:
    now = datetime.now(timezone.utc)
    return FileAssetRead(
        id=uuid.uuid4(),
        name="Finance KPI Definitions",
        description="Certified definitions",
        file_type=FileAssetType.EVIDENCE,
        status=FileStatus.ACTIVE,
        sensitivity=FileSensitivity.CONFIDENTIAL,
        storage_id=None,
        original_filename=None,
        mime_type=None,
        file_size_bytes=None,
        external_url="https://example.com/docs/finance-kpi-definitions",
        storage_path=None,
        checksum=None,
        version="v1.0",
        owner_id=None,
        uploaded_by_id=None,
        created_at=now,
        updated_at=now,
    )


def test_openapi_includes_files_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/files" in paths
    assert "/api/v1/files/{file_id}" in paths
    assert "/api/v1/files/attachments" in paths
    assert "/api/v1/files/entity/{entity_type}/{entity_id}" in paths
    assert "/api/v1/files/storages" in paths


def test_list_files(api_client: TestClient, mock_file_service: AsyncMock) -> None:
    item = FileAssetListItem(
        id=uuid.uuid4(),
        name="Finance KPI Definitions",
        description=None,
        file_type=FileAssetType.EVIDENCE,
        status=FileStatus.ACTIVE,
        sensitivity=FileSensitivity.CONFIDENTIAL,
        storage_id=None,
        external_url="https://example.com/docs/finance-kpi-definitions",
        owner_id=None,
        version="v1.0",
        updated_at=datetime.now(timezone.utc),
    )
    mock_file_service.list_files.return_value = FileAssetListResponse(
        items=[item],
        total=1,
        page=1,
        page_size=20,
        pages=1,
    )

    response = api_client.get("/api/v1/files")

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_create_file(api_client: TestClient, mock_file_service: AsyncMock) -> None:
    sample = _sample_file()
    mock_file_service.create_file.return_value = sample

    response = api_client.post(
        "/api/v1/files",
        json={
            "name": "Finance KPI Definitions",
            "file_type": "evidence",
            "sensitivity": "confidential",
            "external_url": "https://example.com/docs/finance-kpi-definitions",
            "version": "v1.0",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Finance KPI Definitions"


def test_delete_file(api_client: TestClient, mock_file_service: AsyncMock) -> None:
    file_id = uuid.uuid4()
    mock_file_service.archive_or_delete_file.return_value = None

    response = api_client.delete(f"/api/v1/files/{file_id}")

    assert response.status_code == 204
    mock_file_service.archive_or_delete_file.assert_awaited_once_with(file_id)


def test_attach_file_conflict(api_client: TestClient, mock_file_service: AsyncMock) -> None:
    mock_file_service.attach_file.side_effect = FileAttachmentConflictError()

    response = api_client.post(
        "/api/v1/files/attachments",
        json={
            "file_id": str(uuid.uuid4()),
            "entity_type": "data_product",
            "entity_id": str(uuid.uuid4()),
            "purpose": "Evidence",
        },
    )

    assert response.status_code == 409


def test_attach_file_success(api_client: TestClient, mock_file_service: AsyncMock) -> None:
    now = datetime.now(timezone.utc)
    attachment = FileAttachmentRead(
        id=uuid.uuid4(),
        file_id=uuid.uuid4(),
        entity_type=FileEntityType.DATA_PRODUCT,
        entity_id=uuid.uuid4(),
        purpose="Evidence",
        is_evidence=True,
        evidence_type="kpi_certification",
        attached_by_id=None,
        created_at=now,
        updated_at=now,
        file=None,
    )
    mock_file_service.attach_file.return_value = attachment

    response = api_client.post(
        "/api/v1/files/attachments",
        json={
            "file_id": str(attachment.file_id),
            "entity_type": "data_product",
            "entity_id": str(attachment.entity_id),
            "purpose": "Evidence",
            "is_evidence": True,
            "evidence_type": "kpi_certification",
        },
    )

    assert response.status_code == 201
    assert response.json()["is_evidence"] is True
