import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import AdminUser, EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import FileAssetType, FileEntityType, FileSensitivity, FileStatus
from app.modules.activity.dependencies import build_activity_service
from app.modules.files.repository import FileRepository
from app.modules.files.schemas import (
    EntityFilesResponse,
    FileAssetCreate,
    FileAssetFilters,
    FileAssetListResponse,
    FileAssetRead,
    FileAssetUpdate,
    FileAttachmentCreate,
    FileAttachmentListResponse,
    FileAttachmentRead,
    FileStorageCreate,
    FileStorageListResponse,
    FileStorageRead,
    FileStorageUpdate,
)
from app.modules.files.service import FileService

router = APIRouter(prefix="/files", tags=["Files"])


def get_file_service(db: AsyncSession = Depends(get_db)) -> FileService:
    return FileService(FileRepository(db), build_activity_service(db), db)


@router.get("/storages", response_model=FileStorageListResponse)
async def list_file_storages(
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: FileService = Depends(get_file_service),
) -> FileStorageListResponse:
    return await service.list_storages(page=page, page_size=page_size)


@router.post("/storages", response_model=FileStorageRead, status_code=status.HTTP_201_CREATED)
async def create_file_storage(
    payload: FileStorageCreate,
    _user: AdminUser,
    service: FileService = Depends(get_file_service),
) -> FileStorageRead:
    return await service.create_storage(payload)


@router.get("/storages/{storage_id}", response_model=FileStorageRead)
async def get_file_storage(
    storage_id: uuid.UUID,
    _user: ViewerUser,
    service: FileService = Depends(get_file_service),
) -> FileStorageRead:
    return await service.get_storage(storage_id)


@router.patch("/storages/{storage_id}", response_model=FileStorageRead)
async def update_file_storage(
    storage_id: uuid.UUID,
    payload: FileStorageUpdate,
    _user: AdminUser,
    service: FileService = Depends(get_file_service),
) -> FileStorageRead:
    return await service.update_storage(storage_id, payload)


@router.delete("/storages/{storage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_storage(
    storage_id: uuid.UUID,
    _user: AdminUser,
    service: FileService = Depends(get_file_service),
) -> None:
    await service.delete_storage(storage_id)


@router.get("/entity/{entity_type}/{entity_id}", response_model=EntityFilesResponse)
async def list_entity_files(
    entity_type: FileEntityType,
    entity_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: FileService = Depends(get_file_service),
) -> EntityFilesResponse:
    return await service.list_entity_files(
        entity_type,
        entity_id,
        page=page,
        page_size=page_size,
    )


@router.post("/attachments", response_model=FileAttachmentRead, status_code=status.HTTP_201_CREATED)
async def attach_file(
    payload: FileAttachmentCreate,
    _user: EditorUser,
    service: FileService = Depends(get_file_service),
) -> FileAttachmentRead:
    return await service.attach_file(payload)


@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def detach_file(
    attachment_id: uuid.UUID,
    _user: EditorUser,
    service: FileService = Depends(get_file_service),
) -> None:
    await service.detach_file(attachment_id)


@router.get("", response_model=FileAssetListResponse)
async def list_files(
    _user: ViewerUser,
    search: str | None = None,
    file_type: FileAssetType | None = None,
    status: FileStatus | None = None,
    sensitivity: FileSensitivity | None = None,
    storage_id: uuid.UUID | None = None,
    owner_id: uuid.UUID | None = None,
    is_evidence: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: FileService = Depends(get_file_service),
) -> FileAssetListResponse:
    filters = FileAssetFilters(
        search=search,
        file_type=file_type,
        status=status,
        sensitivity=sensitivity,
        storage_id=storage_id,
        owner_id=owner_id,
        is_evidence=is_evidence,
    )
    return await service.list_files(filters=filters, page=page, page_size=page_size)


@router.post("", response_model=FileAssetRead, status_code=status.HTTP_201_CREATED)
async def create_file(
    payload: FileAssetCreate,
    _user: EditorUser,
    service: FileService = Depends(get_file_service),
) -> FileAssetRead:
    return await service.create_file(payload)


@router.get("/{file_id}", response_model=FileAssetRead)
async def get_file(
    file_id: uuid.UUID,
    _user: ViewerUser,
    service: FileService = Depends(get_file_service),
) -> FileAssetRead:
    return await service.get_file(file_id)


@router.patch("/{file_id}", response_model=FileAssetRead)
async def update_file(
    file_id: uuid.UUID,
    payload: FileAssetUpdate,
    _user: EditorUser,
    service: FileService = Depends(get_file_service),
) -> FileAssetRead:
    return await service.update_file(file_id, payload)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: uuid.UUID,
    _user: EditorUser,
    service: FileService = Depends(get_file_service),
) -> None:
    await service.archive_or_delete_file(file_id)


@router.get("/{file_id}/attachments", response_model=FileAttachmentListResponse)
async def list_file_attachments(
    file_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: FileService = Depends(get_file_service),
) -> FileAttachmentListResponse:
    return await service.list_file_attachments(file_id, page=page, page_size=page_size)
