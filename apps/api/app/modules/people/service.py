import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.modules.people.errors import PersonConflictError, PersonNotFoundError
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields
from app.modules.people.repository import PersonListFilters, PersonRepository
from app.modules.people.schemas import (
    PersonCreate,
    PersonListItem,
    PersonListResponse,
    PersonRead,
    PersonSummary,
    PersonUpdate,
)


class PersonService:
    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def list_people(
        self,
        *,
        filters: PersonListFilters,
        page: int,
        page_size: int,
    ) -> PersonListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return PersonListResponse(
            items=[PersonListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_person(self, person_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> PersonRead:
        person = await self._repository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundError(person_id)
        if company_id is not None:
            ensure_company_access(person, company_id, label="Person")
        return PersonRead.model_validate(person)

    async def get_person_summary(self, person_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> PersonSummary:
        person = await self._repository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundError(person_id)
        if company_id is not None:
            ensure_company_access(person, company_id, label="Person")
        counts = await self._repository.get_summary_counts(person_id)
        return PersonSummary(
            person=PersonRead.model_validate(person),
            assigned_work_items=counts["assigned_work_items"],
            owned_data_products_business=counts["owned_data_products_business"],
            owned_data_products_technical=counts["owned_data_products_technical"],
            owned_projects=counts["owned_projects"],
        )

    async def create_person(
        self,
        payload: PersonCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> PersonRead:
        if payload.email is not None:
            existing = await self._repository.get_by_email(payload.email)
            if existing is not None:
                raise PersonConflictError(f"Person with email {payload.email} already exists")
        data = merge_tenant_fields(payload.model_dump(), company_id=company_id, workspace_id=workspace_id)
        person = await self._repository.create(data)
        return PersonRead.model_validate(person)

    async def update_person(
        self,
        person_id: uuid.UUID,
        payload: PersonUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> PersonRead:
        person = await self._repository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundError(person_id)
        if company_id is not None:
            ensure_company_access(person, company_id, label="Person")
        update_data = payload.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"] is not None:
            existing = await self._repository.get_by_email(update_data["email"])
            if existing is not None and existing.id != person_id:
                raise PersonConflictError(
                    f"Person with email {update_data['email']} already exists"
                )
        updated = await self._repository.update(person, update_data)
        return PersonRead.model_validate(updated)

    async def deactivate_person(self, person_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> None:
        person = await self._repository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundError(person_id)
        if company_id is not None:
            ensure_company_access(person, company_id, label="Person")
        await self._repository.deactivate(person)
