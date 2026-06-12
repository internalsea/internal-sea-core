import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.enums import FileEntityType, FileStatus
from app.modules.files.errors import (
    FileAssetNotFoundError,
    FileAttachmentConflictError,
    FileAttachmentNotFoundError,
)
from app.modules.files.schemas import FileAssetCreate, FileAttachmentCreate
from app.modules.files.service import FileService


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_activity() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def file_service(
    mock_repository: AsyncMock,
    mock_activity: AsyncMock,
    mock_session: AsyncMock,
) -> FileService:
    return FileService(mock_repository, mock_activity, mock_session)


@pytest.mark.asyncio
async def test_create_file(
    file_service: FileService,
    mock_repository: AsyncMock,
) -> None:
    file_id = uuid.uuid4()
    mock_asset = MagicMock()
    mock_asset.id = file_id
    mock_asset.name = "Test File"
    mock_asset.description = None
    mock_asset.file_type = "document"
    mock_asset.status = "active"
    mock_asset.sensitivity = "internal"
    mock_asset.storage_id = None
    mock_asset.original_filename = None
    mock_asset.mime_type = None
    mock_asset.file_size_bytes = None
    mock_asset.external_url = "https://example.com/doc"
    mock_asset.storage_path = None
    mock_asset.checksum = None
    mock_asset.version = None
    mock_asset.owner_id = None
    mock_asset.uploaded_by_id = None
    mock_asset.created_at = MagicMock()
    mock_asset.updated_at = MagicMock()
    mock_repository.create_file.return_value = mock_asset

    result = await file_service.create_file(
        FileAssetCreate(
            name="Test File",
            external_url="https://example.com/doc",
        )
    )

    assert result.name == "Test File"
    mock_repository.create_file.assert_awaited_once()


@pytest.mark.asyncio
async def test_archive_or_delete_file_sets_deleted_status(
    file_service: FileService,
    mock_repository: AsyncMock,
) -> None:
    file_id = uuid.uuid4()
    mock_asset = MagicMock()
    mock_asset.status = FileStatus.ACTIVE.value
    mock_repository.get_file_by_id.return_value = mock_asset
    mock_repository.update_file.return_value = mock_asset

    await file_service.archive_or_delete_file(file_id)

    mock_repository.update_file.assert_awaited_once()
    call_args = mock_repository.update_file.call_args
    assert call_args[0][1]["status"] == FileStatus.DELETED.value


@pytest.mark.asyncio
async def test_archive_or_delete_file_raises_when_missing(
    file_service: FileService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_file_by_id.return_value = None
    with pytest.raises(FileAssetNotFoundError):
        await file_service.archive_or_delete_file(uuid.uuid4())


@pytest.mark.asyncio
async def test_attach_file_raises_conflict_on_duplicate(
    file_service: FileService,
    mock_repository: AsyncMock,
    mock_session: AsyncMock,
) -> None:
    file_id = uuid.uuid4()
    entity_id = uuid.uuid4()
    mock_asset = MagicMock()
    mock_asset.name = "Spec"
    mock_repository.get_file_by_id.return_value = mock_asset
    mock_repository.get_duplicate_attachment.return_value = MagicMock()
    mock_session.get = AsyncMock(return_value=MagicMock())

    with pytest.raises(FileAttachmentConflictError):
        await file_service.attach_file(
            FileAttachmentCreate(
                file_id=file_id,
                entity_type=FileEntityType.DATA_PRODUCT,
                entity_id=entity_id,
            )
        )


@pytest.mark.asyncio
async def test_detach_file_raises_when_missing(
    file_service: FileService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_attachment_by_id.return_value = None
    with pytest.raises(FileAttachmentNotFoundError):
        await file_service.detach_file(uuid.uuid4())
