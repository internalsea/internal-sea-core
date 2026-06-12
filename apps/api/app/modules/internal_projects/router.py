import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import ProjectStatus, ProjectType
from app.modules.activity.dependencies import build_activity_service
from app.modules.projects.repository import ProjectListFilters, ProjectRepository
from app.modules.projects.schemas import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.modules.projects.service import ProjectService
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant

router = APIRouter(prefix="/internal-projects", tags=["Internal Projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(ProjectRepository(db), build_activity_service(db))


@router.get("", response_model=ProjectListResponse)
async def list_internal_projects(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    status: ProjectStatus | None = None,
    owner_id: uuid.UUID | None = None,
    team_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    health_status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: ProjectService = Depends(get_project_service),
) -> ProjectListResponse:
    filters = ProjectListFilters(
        search=search,
        project_type=ProjectType.INTERNAL_PROJECT,
        status=status,
        owner_id=owner_id,
        team_id=team_id,
        capability_id=capability_id,
        health_status=health_status,
        company_id=tenant.company_id,
    )
    return await service.list_projects(
        filters=filters,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_internal_project(
    payload: ProjectCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    forced_payload = payload.model_copy(update={"project_type": ProjectType.INTERNAL_PROJECT})
    return await service.create_project(
        forced_payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{project_id}", response_model=ProjectRead)
async def get_internal_project(
    project_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    return await service.get_internal_project(project_id, company_id=tenant.company_id)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_internal_project(
    project_id: uuid.UUID,
    payload: ProjectUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    return await service.update_internal_project(project_id, payload, company_id=tenant.company_id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_internal_project(
    project_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: ProjectService = Depends(get_project_service),
) -> None:
    await service.delete_internal_project(project_id, company_id=tenant.company_id)
