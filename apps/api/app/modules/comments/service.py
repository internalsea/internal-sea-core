import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, ProjectType
from app.models.projects import Project
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.comments.errors import CommentNotFoundError
from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import (
    CommentCreate,
    CommentListResponse,
    CommentRead,
    CommentUpdate,
)
from app.modules.data_products.errors import DataProductNotFoundError
from app.modules.data_products.repository import DataProductRepository
from app.modules.projects.errors import ProjectNotFoundError
from app.modules.projects.repository import ProjectRepository
from app.modules.work_items.errors import WorkItemNotFoundError
from app.modules.work_items.repository import WorkItemRepository


class CommentService:
    def __init__(
        self,
        repository: CommentRepository,
        activity_service: ActivityService,
        data_product_repository: DataProductRepository,
        work_item_repository: WorkItemRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self._repository = repository
        self._activity = activity_service
        self._data_products = data_product_repository
        self._work_items = work_item_repository
        self._projects = project_repository

    async def _record_comment_activity(
        self,
        *,
        entity_type: ActivityEntityType,
        entity_id: uuid.UUID,
        title: str,
        author_id: uuid.UUID | None,
        comment_id: uuid.UUID,
    ) -> None:
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=entity_type,
                entity_id=entity_id,
                action=ActivityAction.COMMENTED,
                actor_id=author_id,
                title=title,
                details={"comment_id": str(comment_id)},
            )
        )

    async def list_data_product_comments(
        self,
        data_product_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> CommentListResponse:
        data_product = await self._data_products.get_by_id(data_product_id)
        if data_product is None:
            raise DataProductNotFoundError(data_product_id)
        return await self._list_comments(
            list_fn=lambda offset, limit: self._repository.list_for_data_product(
                data_product_id,
                offset=offset,
                limit=limit,
            ),
            page=page,
            page_size=page_size,
        )

    async def add_data_product_comment(
        self,
        data_product_id: uuid.UUID,
        payload: CommentCreate,
    ) -> CommentRead:
        data_product = await self._data_products.get_by_id(data_product_id)
        if data_product is None:
            raise DataProductNotFoundError(data_product_id)
        comment = await self._repository.create_for_data_product(data_product_id, payload)
        await self._record_comment_activity(
            entity_type=ActivityEntityType.DATA_PRODUCT,
            entity_id=data_product_id,
            title="Comment added to data product",
            author_id=payload.author_id,
            comment_id=comment.id,
        )
        return CommentRead.model_validate(comment)

    async def list_work_item_comments(
        self,
        work_item_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> CommentListResponse:
        work_item = await self._work_items.get_by_id(work_item_id)
        if work_item is None:
            raise WorkItemNotFoundError(work_item_id)
        return await self._list_comments(
            list_fn=lambda offset, limit: self._repository.list_for_work_item(
                work_item_id,
                offset=offset,
                limit=limit,
            ),
            page=page,
            page_size=page_size,
        )

    async def add_work_item_comment(
        self,
        work_item_id: uuid.UUID,
        payload: CommentCreate,
    ) -> CommentRead:
        work_item = await self._work_items.get_by_id(work_item_id)
        if work_item is None:
            raise WorkItemNotFoundError(work_item_id)
        comment = await self._repository.create_for_work_item(work_item_id, payload)
        await self._record_comment_activity(
            entity_type=ActivityEntityType.WORK_ITEM,
            entity_id=work_item_id,
            title="Comment added to work item",
            author_id=payload.author_id,
            comment_id=comment.id,
        )
        return CommentRead.model_validate(comment)

    async def list_project_comments(
        self,
        project_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> CommentListResponse:
        project = await self._projects.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        return await self._list_comments(
            list_fn=lambda offset, limit: self._repository.list_for_project(
                project_id,
                offset=offset,
                limit=limit,
            ),
            page=page,
            page_size=page_size,
        )

    async def add_project_comment(
        self,
        project_id: uuid.UUID,
        payload: CommentCreate,
    ) -> CommentRead:
        project = await self._projects.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        comment = await self._repository.create_for_project(project_id, payload)
        entity_type = (
            ActivityEntityType.INTERNAL_PROJECT
            if project.project_type == ProjectType.INTERNAL_PROJECT
            else ActivityEntityType.PROJECT
        )
        title = (
            "Comment added to internal project"
            if entity_type == ActivityEntityType.INTERNAL_PROJECT
            else "Comment added to project"
        )
        await self._record_comment_activity(
            entity_type=entity_type,
            entity_id=project_id,
            title=title,
            author_id=payload.author_id,
            comment_id=comment.id,
        )
        return CommentRead.model_validate(comment)

    async def list_internal_project_comments(
        self,
        project_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> CommentListResponse:
        await self._get_internal_project(project_id)
        return await self.list_project_comments(project_id, page=page, page_size=page_size)

    async def add_internal_project_comment(
        self,
        project_id: uuid.UUID,
        payload: CommentCreate,
    ) -> CommentRead:
        await self._get_internal_project(project_id)
        return await self.add_project_comment(project_id, payload)

    async def update_comment(
        self,
        comment_id: uuid.UUID,
        payload: CommentUpdate,
    ) -> CommentRead:
        comment = await self._repository.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError(comment_id)
        updated = await self._repository.update(comment, payload)
        return CommentRead.model_validate(updated)

    async def delete_comment(self, comment_id: uuid.UUID) -> None:
        comment = await self._repository.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError(comment_id)
        await self._repository.delete(comment)

    async def _get_internal_project(self, project_id: uuid.UUID) -> Project:
        project = await self._projects.get_by_id(project_id)
        if project is None or project.project_type != ProjectType.INTERNAL_PROJECT:
            raise ProjectNotFoundError(project_id)
        return project

    async def _list_comments(
        self,
        *,
        list_fn: Callable[[int, int], Awaitable[tuple[list[Any], int]]],
        page: int,
        page_size: int,
    ) -> CommentListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        items, total = await list_fn(offset, normalized_page_size)
        return CommentListResponse(
            items=[CommentRead.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )
