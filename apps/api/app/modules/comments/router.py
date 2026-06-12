import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.modules.activity.repository import ActivityRepository
from app.modules.activity.service import ActivityService
from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import CommentCreate, CommentListResponse, CommentRead, CommentUpdate
from app.modules.comments.service import CommentService
from app.modules.data_products.repository import DataProductRepository
from app.modules.projects.repository import ProjectRepository
from app.modules.work_items.repository import WorkItemRepository

router = APIRouter(tags=["Comments"])


def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    activity_service = ActivityService(ActivityRepository(db))
    return CommentService(
        CommentRepository(db),
        activity_service,
        DataProductRepository(db),
        WorkItemRepository(db),
        ProjectRepository(db),
    )


@router.get("/data-products/{data_product_id}/comments", response_model=CommentListResponse)
async def list_data_product_comments(
    data_product_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return await service.list_data_product_comments(
        data_product_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/data-products/{data_product_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_data_product_comment(
    data_product_id: uuid.UUID,
    payload: CommentCreate,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> CommentRead:
    return await service.add_data_product_comment(data_product_id, payload)


@router.get("/work-items/{work_item_id}/comments", response_model=CommentListResponse)
async def list_work_item_comments(
    work_item_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return await service.list_work_item_comments(
        work_item_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/work-items/{work_item_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_work_item_comment(
    work_item_id: uuid.UUID,
    payload: CommentCreate,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> CommentRead:
    return await service.add_work_item_comment(work_item_id, payload)


@router.get("/projects/{project_id}/comments", response_model=CommentListResponse)
async def list_project_comments(
    project_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return await service.list_project_comments(
        project_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/projects/{project_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_comment(
    project_id: uuid.UUID,
    payload: CommentCreate,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> CommentRead:
    return await service.add_project_comment(project_id, payload)


@router.get("/internal-projects/{project_id}/comments", response_model=CommentListResponse)
async def list_internal_project_comments(
    project_id: uuid.UUID,
    _user: ViewerUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return await service.list_internal_project_comments(
        project_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/internal-projects/{project_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_internal_project_comment(
    project_id: uuid.UUID,
    payload: CommentCreate,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> CommentRead:
    return await service.add_internal_project_comment(project_id, payload)


@router.patch("/comments/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: uuid.UUID,
    payload: CommentUpdate,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> CommentRead:
    return await service.update_comment(comment_id, payload)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: uuid.UUID,
    _user: EditorUser,
    service: CommentService = Depends(get_comment_service),
) -> None:
    await service.delete_comment(comment_id)
