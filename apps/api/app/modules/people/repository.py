import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import get_model
from app.domain.enums import SeniorityLevel, WorkItemStatus
from app.models.catalog import DataProduct
from app.models.people import Person
from app.models.projects import Project
from app.models.work import WorkItem

COMPLETED_WORK_ITEM_STATUSES = (WorkItemStatus.DONE, WorkItemStatus.CLOSED)


@dataclass
class PersonListFilters:
    search: str | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    seniority_level: SeniorityLevel | None = None
    is_active: bool | None = None
    location: str | None = None
    min_availability: int | None = None
    max_availability: int | None = None
    company_id: uuid.UUID | None = None


class PersonRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query: Any, filters: PersonListFilters) -> Any:
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    Person.full_name.ilike(pattern),
                    Person.email.ilike(pattern),
                    Person.role_title.ilike(pattern),
                    Person.location.ilike(pattern),
                )
            )
        if filters.team_id is not None:
            query = query.where(Person.team_id == filters.team_id)
        if filters.capability_id is not None:
            query = query.where(Person.capability_id == filters.capability_id)
        if filters.seniority_level is not None:
            query = query.where(Person.seniority_level == filters.seniority_level)
        if filters.is_active is not None:
            query = query.where(Person.is_active == filters.is_active)
        if filters.location:
            query = query.where(Person.location.ilike(f"%{filters.location}%"))
        if filters.min_availability is not None:
            query = query.where(Person.availability_percent >= filters.min_availability)
        if filters.max_availability is not None:
            query = query.where(Person.availability_percent <= filters.max_availability)
        if filters.company_id is not None:
            query = query.where(Person.company_id == filters.company_id)
        return query

    async def list_paginated(
        self,
        *,
        filters: PersonListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Person], int]:
        base_query = select(Person)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(Person.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(Person.full_name.asc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_by_id(self, person_id: uuid.UUID) -> Person | None:
        return await get_model(self._session, Person, person_id)

    async def get_by_email(self, email: str) -> Person | None:
        return await self._session.scalar(select(Person).where(Person.email == email))

    async def create(self, data: dict[str, object]) -> Person:
        person = Person(**data)
        self._session.add(person)
        await self._session.commit()
        await self._session.refresh(person)
        return person

    async def update(self, person: Person, data: dict[str, object]) -> Person:
        for field, value in data.items():
            setattr(person, field, value)
        await self._session.commit()
        await self._session.refresh(person)
        return person

    async def deactivate(self, person: Person) -> Person:
        person.is_active = False
        await self._session.commit()
        await self._session.refresh(person)
        return person

    async def get_summary_counts(self, person_id: uuid.UUID) -> dict[str, int]:
        assigned_work_items = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    WorkItem.assignee_id == person_id,
                    WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )
        owned_data_products_business = int(
            await self._session.scalar(
                select(func.count(DataProduct.id)).where(
                    DataProduct.business_owner_id == person_id,
                )
            )
            or 0
        )
        owned_data_products_technical = int(
            await self._session.scalar(
                select(func.count(DataProduct.id)).where(
                    DataProduct.technical_owner_id == person_id,
                )
            )
            or 0
        )
        owned_projects = int(
            await self._session.scalar(
                select(func.count(Project.id)).where(Project.owner_id == person_id)
            )
            or 0
        )

        return {
            "assigned_work_items": assigned_work_items,
            "owned_data_products_business": owned_data_products_business,
            "owned_data_products_technical": owned_data_products_technical,
            "owned_projects": owned_projects,
        }
