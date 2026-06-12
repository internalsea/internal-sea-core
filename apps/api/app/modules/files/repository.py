import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums import FileAssetType, FileSensitivity, FileStatus, FileEntityType
from app.models.files import FileAsset, FileAttachment, FileStorage


@dataclass
class FileListFilters:
    search: str | None = None
    file_type: FileAssetType | None = None
    status: FileStatus | None = None
    sensitivity: FileSensitivity | None = None
    storage_id: uuid.UUID | None = None
    owner_id: uuid.UUID | None = None
    is_evidence: bool | None = None


class FileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_file_filters(self, query, filters: FileListFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    FileAsset.name.ilike(pattern),
                    FileAsset.description.ilike(pattern),
                    FileAsset.original_filename.ilike(pattern),
                    FileAsset.external_url.ilike(pattern),
                )
            )
        if filters.file_type is not None:
            query = query.where(FileAsset.file_type == filters.file_type.value)
        if filters.status is not None:
            query = query.where(FileAsset.status == filters.status.value)
        if filters.sensitivity is not None:
            query = query.where(FileAsset.sensitivity == filters.sensitivity.value)
        if filters.storage_id is not None:
            query = query.where(FileAsset.storage_id == filters.storage_id)
        if filters.owner_id is not None:
            query = query.where(FileAsset.owner_id == filters.owner_id)
        if filters.is_evidence is not None:
            evidence_subq = (
                select(FileAttachment.file_id)
                .where(FileAttachment.is_evidence.is_(filters.is_evidence))
                .distinct()
            )
            query = query.where(FileAsset.id.in_(evidence_subq))
        return query

    async def list_storages(
        self,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[FileStorage], int]:
        count_query = select(func.count(FileStorage.id))
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            select(FileStorage)
            .order_by(FileStorage.name.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_storage_by_id(self, storage_id: uuid.UUID) -> FileStorage | None:
        return await self._session.get(FileStorage, storage_id)

    async def get_storage_by_name(self, name: str) -> FileStorage | None:
        result = await self._session.execute(
            select(FileStorage).where(FileStorage.name == name)
        )
        return result.scalar_one_or_none()

    async def create_storage(self, data: dict[str, object]) -> FileStorage:
        storage = FileStorage(**data)
        self._session.add(storage)
        await self._session.commit()
        await self._session.refresh(storage)
        return storage

    async def update_storage(self, storage: FileStorage, data: dict[str, object]) -> FileStorage:
        for key, value in data.items():
            setattr(storage, key, value)
        await self._session.commit()
        await self._session.refresh(storage)
        return storage

    async def delete_storage(self, storage: FileStorage) -> None:
        await self._session.delete(storage)
        await self._session.commit()

    async def count_assets_for_storage(self, storage_id: uuid.UUID) -> int:
        result = await self._session.scalar(
            select(func.count(FileAsset.id)).where(FileAsset.storage_id == storage_id)
        )
        return int(result or 0)

    async def list_files(
        self,
        *,
        filters: FileListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[FileAsset], int]:
        base_query = select(FileAsset)
        filtered_query = self._apply_file_filters(base_query, filters)
        count_query = self._apply_file_filters(select(func.count(FileAsset.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            filtered_query.order_by(FileAsset.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_file_by_id(self, file_id: uuid.UUID) -> FileAsset | None:
        return await self._session.get(FileAsset, file_id)

    async def create_file(self, data: dict[str, object]) -> FileAsset:
        file_asset = FileAsset(**data)
        self._session.add(file_asset)
        await self._session.commit()
        await self._session.refresh(file_asset)
        return file_asset

    async def update_file(self, file_asset: FileAsset, data: dict[str, object]) -> FileAsset:
        for key, value in data.items():
            setattr(file_asset, key, value)
        await self._session.commit()
        await self._session.refresh(file_asset)
        return file_asset

    async def delete_file(self, file_asset: FileAsset) -> None:
        await self._session.delete(file_asset)
        await self._session.commit()

    async def count_attachments_for_file(self, file_id: uuid.UUID) -> int:
        result = await self._session.scalar(
            select(func.count(FileAttachment.id)).where(FileAttachment.file_id == file_id)
        )
        return int(result or 0)

    async def list_attachments_for_entity(
        self,
        *,
        entity_type: FileEntityType,
        entity_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[FileAttachment], int]:
        base = select(FileAttachment).where(
            FileAttachment.entity_type == entity_type.value,
            FileAttachment.entity_id == entity_id,
        )
        count_query = select(func.count(FileAttachment.id)).where(
            FileAttachment.entity_type == entity_type.value,
            FileAttachment.entity_id == entity_id,
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            base.options(selectinload(FileAttachment.file))
            .order_by(FileAttachment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def list_attachments_for_file(
        self,
        *,
        file_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[FileAttachment], int]:
        base = select(FileAttachment).where(FileAttachment.file_id == file_id)
        count_query = select(func.count(FileAttachment.id)).where(
            FileAttachment.file_id == file_id
        )
        total = int(await self._session.scalar(count_query) or 0)
        result = await self._session.scalars(
            base.options(selectinload(FileAttachment.file))
            .order_by(FileAttachment.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.all()), total

    async def get_attachment_by_id(self, attachment_id: uuid.UUID) -> FileAttachment | None:
        result = await self._session.execute(
            select(FileAttachment)
            .options(selectinload(FileAttachment.file))
            .where(FileAttachment.id == attachment_id)
        )
        return result.scalar_one_or_none()

    async def get_duplicate_attachment(
        self,
        *,
        file_id: uuid.UUID,
        entity_type: FileEntityType,
        entity_id: uuid.UUID,
        purpose: str | None,
    ) -> FileAttachment | None:
        query = select(FileAttachment).where(
            FileAttachment.file_id == file_id,
            FileAttachment.entity_type == entity_type.value,
            FileAttachment.entity_id == entity_id,
        )
        if purpose is None:
            query = query.where(FileAttachment.purpose.is_(None))
        else:
            query = query.where(FileAttachment.purpose == purpose)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def create_attachment(self, data: dict[str, object]) -> FileAttachment:
        attachment = FileAttachment(**data)
        self._session.add(attachment)
        await self._session.commit()
        result = await self._session.execute(
            select(FileAttachment)
            .options(selectinload(FileAttachment.file))
            .where(FileAttachment.id == attachment.id)
        )
        return result.scalar_one()

    async def delete_attachment(self, attachment: FileAttachment) -> None:
        await self._session.delete(attachment)
        await self._session.commit()
