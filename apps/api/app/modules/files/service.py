import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, FileEntityType, FileStatus
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.files.errors import (
    FileAssetNotFoundError,
    FileAttachmentConflictError,
    FileAttachmentNotFoundError,
    FileStorageConflictError,
    FileStorageNotFoundError,
    UnsupportedFileEntityTypeError,
)
from app.modules.files.repository import FileListFilters, FileRepository
from app.modules.files.schemas import (
    EntityFilesResponse,
    FileAssetCreate,
    FileAssetFilters,
    FileAssetListItem,
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
from app.modules.files.validators import (
    is_supported_file_entity_type,
    validate_file_attachment_entity_exists,
)


class FileService:
    def __init__(
        self,
        repository: FileRepository,
        activity_service: ActivityService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._session = session

    def _to_activity_entity_type(
        self,
        entity_type: FileEntityType,
    ) -> ActivityEntityType | None:
        try:
            return ActivityEntityType(entity_type.value)
        except ValueError:
            return None

    def _attachment_to_read(self, attachment) -> FileAttachmentRead:
        file_item = None
        if attachment.file is not None:
            file_item = FileAssetListItem.model_validate(attachment.file)
        return FileAttachmentRead(
            id=attachment.id,
            file_id=attachment.file_id,
            entity_type=FileEntityType(attachment.entity_type),
            entity_id=attachment.entity_id,
            purpose=attachment.purpose,
            is_evidence=attachment.is_evidence,
            evidence_type=attachment.evidence_type,
            attached_by_id=attachment.attached_by_id,
            created_at=attachment.created_at,
            updated_at=attachment.updated_at,
            file=file_item,
        )

    async def _record_attachment_activity(
        self,
        *,
        entity_type: FileEntityType,
        entity_id: uuid.UUID,
        action: ActivityAction,
        file_name: str,
        purpose: str | None,
        attachment_id: uuid.UUID,
        actor_id: uuid.UUID | None = None,
    ) -> None:
        activity_entity_type = self._to_activity_entity_type(entity_type)
        if activity_entity_type is None:
            return
        if action == ActivityAction.LINKED:
            title = "File attached"
            purpose_text = f" ({purpose})" if purpose else ""
            description = f"{file_name}{purpose_text}"
        else:
            title = "File detached"
            description = file_name
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=activity_entity_type,
                entity_id=entity_id,
                action=action,
                actor_id=actor_id,
                title=title,
                description=description,
                details={"attachment_id": str(attachment_id)},
            )
        )

    def _enum_value(self, value) -> str | None:
        if value is None:
            return None
        return value.value if hasattr(value, "value") else str(value)

    async def list_storages(
        self,
        *,
        page: int,
        page_size: int,
    ) -> FileStorageListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_storages(
            offset=offset,
            limit=normalized_page_size,
        )
        return FileStorageListResponse(
            items=[FileStorageRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_storage(self, storage_id: uuid.UUID) -> FileStorageRead:
        storage = await self._repository.get_storage_by_id(storage_id)
        if storage is None:
            raise FileStorageNotFoundError(storage_id)
        return FileStorageRead.model_validate(storage)

    async def create_storage(self, payload: FileStorageCreate) -> FileStorageRead:
        existing = await self._repository.get_storage_by_name(payload.name)
        if existing is not None:
            raise FileStorageConflictError(f"File storage already exists: {payload.name}")
        data = payload.model_dump()
        data["storage_type"] = self._enum_value(data["storage_type"])
        storage = await self._repository.create_storage(data)
        return FileStorageRead.model_validate(storage)

    async def update_storage(
        self,
        storage_id: uuid.UUID,
        payload: FileStorageUpdate,
    ) -> FileStorageRead:
        storage = await self._repository.get_storage_by_id(storage_id)
        if storage is None:
            raise FileStorageNotFoundError(storage_id)
        update_data = payload.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = await self._repository.get_storage_by_name(update_data["name"])
            if existing is not None and existing.id != storage_id:
                raise FileStorageConflictError(
                    f"File storage already exists: {update_data['name']}"
                )
        if "storage_type" in update_data:
            update_data["storage_type"] = self._enum_value(update_data["storage_type"])
        updated = await self._repository.update_storage(storage, update_data)
        return FileStorageRead.model_validate(updated)

    async def delete_storage(self, storage_id: uuid.UUID) -> None:
        storage = await self._repository.get_storage_by_id(storage_id)
        if storage is None:
            raise FileStorageNotFoundError(storage_id)
        asset_count = await self._repository.count_assets_for_storage(storage_id)
        if asset_count > 0:
            raise FileStorageConflictError("File storage is in use and cannot be deleted")
        await self._repository.delete_storage(storage)

    async def list_files(
        self,
        *,
        filters: FileAssetFilters,
        page: int,
        page_size: int,
    ) -> FileAssetListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        repo_filters = FileListFilters(
            search=filters.search,
            file_type=filters.file_type,
            status=filters.status,
            sensitivity=filters.sensitivity,
            storage_id=filters.storage_id,
            owner_id=filters.owner_id,
            is_evidence=filters.is_evidence,
        )
        items, total = await self._repository.list_files(
            filters=repo_filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return FileAssetListResponse(
            items=[FileAssetListItem.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_file(self, file_id: uuid.UUID) -> FileAssetRead:
        file_asset = await self._repository.get_file_by_id(file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(file_id)
        return FileAssetRead.model_validate(file_asset)

    async def create_file(self, payload: FileAssetCreate) -> FileAssetRead:
        data = payload.model_dump()
        for key in ("file_type", "status", "sensitivity"):
            data[key] = self._enum_value(data[key])
        file_asset = await self._repository.create_file(data)
        return FileAssetRead.model_validate(file_asset)

    async def update_file(self, file_id: uuid.UUID, payload: FileAssetUpdate) -> FileAssetRead:
        file_asset = await self._repository.get_file_by_id(file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(file_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key in ("file_type", "status", "sensitivity"):
            if key in update_data:
                update_data[key] = self._enum_value(update_data[key])
        updated = await self._repository.update_file(file_asset, update_data)
        return FileAssetRead.model_validate(updated)

    async def archive_or_delete_file(self, file_id: uuid.UUID) -> None:
        file_asset = await self._repository.get_file_by_id(file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(file_id)
        file_asset.status = FileStatus.DELETED.value
        await self._repository.update_file(file_asset, {"status": FileStatus.DELETED.value})

    async def list_entity_files(
        self,
        entity_type: FileEntityType,
        entity_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> EntityFilesResponse:
        if not is_supported_file_entity_type(entity_type):
            raise UnsupportedFileEntityTypeError(entity_type.value)
        await validate_file_attachment_entity_exists(self._session, entity_type, entity_id)
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_attachments_for_entity(
            entity_type=entity_type,
            entity_id=entity_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return EntityFilesResponse(
            entity_type=entity_type,
            entity_id=entity_id,
            files=[self._attachment_to_read(item) for item in items],
            total=total,
        )

    async def attach_file(self, payload: FileAttachmentCreate) -> FileAttachmentRead:
        if not is_supported_file_entity_type(payload.entity_type):
            raise UnsupportedFileEntityTypeError(payload.entity_type.value)

        file_asset = await self._repository.get_file_by_id(payload.file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(payload.file_id)

        await validate_file_attachment_entity_exists(
            self._session,
            payload.entity_type,
            payload.entity_id,
        )

        duplicate = await self._repository.get_duplicate_attachment(
            file_id=payload.file_id,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            purpose=payload.purpose,
        )
        if duplicate is not None:
            raise FileAttachmentConflictError()

        data = payload.model_dump()
        data["entity_type"] = self._enum_value(data["entity_type"])
        attachment = await self._repository.create_attachment(data)

        await self._record_attachment_activity(
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            action=ActivityAction.LINKED,
            file_name=file_asset.name,
            purpose=payload.purpose,
            attachment_id=attachment.id,
            actor_id=payload.attached_by_id,
        )

        return self._attachment_to_read(attachment)

    async def detach_file(self, attachment_id: uuid.UUID) -> None:
        attachment = await self._repository.get_attachment_by_id(attachment_id)
        if attachment is None:
            raise FileAttachmentNotFoundError(attachment_id)

        file_name = attachment.file.name if attachment.file else str(attachment.file_id)
        entity_type = FileEntityType(attachment.entity_type)
        entity_id = attachment.entity_id

        await self._repository.delete_attachment(attachment)

        await self._record_attachment_activity(
            entity_type=entity_type,
            entity_id=entity_id,
            action=ActivityAction.UNLINKED,
            file_name=file_name,
            purpose=attachment.purpose,
            attachment_id=attachment_id,
            actor_id=attachment.attached_by_id,
        )

    async def list_file_attachments(
        self,
        file_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> FileAttachmentListResponse:
        file_asset = await self._repository.get_file_by_id(file_id)
        if file_asset is None:
            raise FileAssetNotFoundError(file_id)
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_attachments_for_file(
            file_id=file_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return FileAttachmentListResponse(
            items=[self._attachment_to_read(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )
