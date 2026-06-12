import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.work import Comment
from app.modules.comments.schemas import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _paginated_list(
        self,
        *,
        where_clause,
        offset: int,
        limit: int,
    ) -> tuple[list[Comment], int]:
        base_query = select(Comment).where(where_clause)
        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self._session.scalar(count_query) or 0
        items_query = (
            base_query.order_by(Comment.created_at.desc()).offset(offset).limit(limit)
        )
        result = await self._session.execute(items_query)
        return list(result.scalars().all()), total

    async def list_for_data_product(
        self,
        data_product_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Comment], int]:
        return await self._paginated_list(
            where_clause=Comment.data_product_id == data_product_id,
            offset=offset,
            limit=limit,
        )

    async def list_for_work_item(
        self,
        work_item_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Comment], int]:
        return await self._paginated_list(
            where_clause=Comment.work_item_id == work_item_id,
            offset=offset,
            limit=limit,
        )

    async def list_for_project(
        self,
        project_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Comment], int]:
        return await self._paginated_list(
            where_clause=Comment.project_id == project_id,
            offset=offset,
            limit=limit,
        )

    async def get_by_id(self, comment_id: uuid.UUID) -> Comment | None:
        return await self._session.get(Comment, comment_id)

    async def create_for_data_product(
        self,
        data_product_id: uuid.UUID,
        payload: CommentCreate,
    ) -> Comment:
        comment = Comment(
            body=payload.body,
            author_id=payload.author_id,
            data_product_id=data_product_id,
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def create_for_work_item(
        self,
        work_item_id: uuid.UUID,
        payload: CommentCreate,
    ) -> Comment:
        comment = Comment(
            body=payload.body,
            author_id=payload.author_id,
            work_item_id=work_item_id,
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def create_for_project(
        self,
        project_id: uuid.UUID,
        payload: CommentCreate,
    ) -> Comment:
        comment = Comment(
            body=payload.body,
            author_id=payload.author_id,
            project_id=project_id,
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def update(self, comment: Comment, payload: CommentUpdate) -> Comment:
        comment.body = payload.body
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)
        await self._session.commit()
