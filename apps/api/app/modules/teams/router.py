import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.modules.teams.repository import TeamListFilters, TeamRepository
from app.modules.teams.schemas import (
    TeamCreate,
    TeamListResponse,
    TeamRead,
    TeamSummary,
    TeamUpdate,
)
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant
from app.modules.teams.service import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


def get_team_service(db: AsyncSession = Depends(get_db)) -> TeamService:
    return TeamService(TeamRepository(db))


@router.get("", response_model=TeamListResponse)
async def list_teams(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: TeamService = Depends(get_team_service),
) -> TeamListResponse:
    filters = TeamListFilters(search=search, company_id=tenant.company_id)
    return await service.list_teams(filters=filters, page=page, page_size=page_size)


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    payload: TeamCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TeamService = Depends(get_team_service),
) -> TeamRead:
    return await service.create_team(
        payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{team_id}", response_model=TeamRead)
async def get_team(
    team_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TeamService = Depends(get_team_service),
) -> TeamRead:
    return await service.get_team(team_id, company_id=tenant.company_id)


@router.get("/{team_id}/summary", response_model=TeamSummary)
async def get_team_summary(
    team_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TeamService = Depends(get_team_service),
) -> TeamSummary:
    return await service.get_team_summary(team_id, company_id=tenant.company_id)


@router.patch("/{team_id}", response_model=TeamRead)
async def update_team(
    team_id: uuid.UUID,
    payload: TeamUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TeamService = Depends(get_team_service),
) -> TeamRead:
    return await service.update_team(team_id, payload, company_id=tenant.company_id)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: TeamService = Depends(get_team_service),
) -> None:
    await service.delete_team(team_id, company_id=tenant.company_id)
