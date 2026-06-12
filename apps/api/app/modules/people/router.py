import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_deps import EditorUser, ViewerUser
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import SeniorityLevel
from app.modules.people.repository import PersonListFilters, PersonRepository
from app.modules.people.schemas import (
    PersonCreate,
    PersonListResponse,
    PersonRead,
    PersonSummary,
    PersonUpdate,
)
from app.modules.tenancy.dependencies import CurrentTenant, get_current_tenant
from app.modules.people.service import PersonService

router = APIRouter(prefix="/people", tags=["People"])


def get_person_service(db: AsyncSession = Depends(get_db)) -> PersonService:
    return PersonService(PersonRepository(db))


@router.get("", response_model=PersonListResponse)
async def list_people(
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    search: str | None = None,
    team_id: uuid.UUID | None = None,
    capability_id: uuid.UUID | None = None,
    seniority_level: SeniorityLevel | None = None,
    is_active: bool | None = None,
    location: str | None = None,
    min_availability: int | None = Query(None, ge=0, le=100),
    max_availability: int | None = Query(None, ge=0, le=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    service: PersonService = Depends(get_person_service),
) -> PersonListResponse:
    filters = PersonListFilters(
        search=search,
        team_id=team_id,
        capability_id=capability_id,
        seniority_level=seniority_level,
        is_active=is_active,
        location=location,
        min_availability=min_availability,
        max_availability=max_availability,
        company_id=tenant.company_id,
    )
    return await service.list_people(filters=filters, page=page, page_size=page_size)


@router.post("", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
async def create_person(
    payload: PersonCreate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: PersonService = Depends(get_person_service),
) -> PersonRead:
    return await service.create_person(
        payload,
        company_id=tenant.company_id,
        workspace_id=tenant.workspace_id,
    )


@router.get("/{person_id}", response_model=PersonRead)
async def get_person(
    person_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: PersonService = Depends(get_person_service),
) -> PersonRead:
    return await service.get_person(person_id, company_id=tenant.company_id)


@router.get("/{person_id}/summary", response_model=PersonSummary)
async def get_person_summary(
    person_id: uuid.UUID,
    _user: ViewerUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: PersonService = Depends(get_person_service),
) -> PersonSummary:
    return await service.get_person_summary(person_id, company_id=tenant.company_id)


@router.patch("/{person_id}", response_model=PersonRead)
async def update_person(
    person_id: uuid.UUID,
    payload: PersonUpdate,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: PersonService = Depends(get_person_service),
) -> PersonRead:
    return await service.update_person(person_id, payload, company_id=tenant.company_id)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_person(
    person_id: uuid.UUID,
    _user: EditorUser,
    tenant: CurrentTenant = Depends(get_current_tenant),
    service: PersonService = Depends(get_person_service),
) -> None:
    await service.deactivate_person(person_id, company_id=tenant.company_id)
