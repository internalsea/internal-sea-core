import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import ProjectType, WorkItemStatus
from app.models.catalog import DataProduct
from app.models.people import Capability, Person
from app.models.projects import Project
from app.models.work import WorkItem

COMPLETED_WORK_ITEM_STATUSES = (WorkItemStatus.DONE, WorkItemStatus.CLOSED)


@dataclass
class CapabilityListFilters:
    search: str | None = None
    company_id: uuid.UUID | None = None


class CapabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query, filters: CapabilityListFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    Capability.name.ilike(pattern),
                    Capability.description.ilike(pattern),
                )
            )
        if filters.company_id is not None:
            query = query.where(Capability.company_id == filters.company_id)
        return query

    async def list(
        self,
        *,
        filters: CapabilityListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Capability], int]:
        base_query = select(Capability)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(Capability.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(Capability.name.asc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_by_id(self, capability_id: uuid.UUID) -> Capability | None:
        return await self._session.get(Capability, capability_id)

    async def get_by_name(self, name: str) -> Capability | None:
        return await self._session.scalar(select(Capability).where(Capability.name == name))

    async def create(self, data: dict[str, object]) -> Capability:
        capability = Capability(**data)
        self._session.add(capability)
        await self._session.commit()
        await self._session.refresh(capability)
        return capability

    async def update(self, capability: Capability, data: dict[str, object]) -> Capability:
        for field, value in data.items():
            setattr(capability, field, value)
        await self._session.commit()
        await self._session.refresh(capability)
        return capability

    async def delete(self, capability: Capability) -> None:
        await self._session.delete(capability)
        await self._session.commit()

    async def get_summary_counts(self, capability_id: uuid.UUID) -> dict[str, int]:
        people_count = int(
            await self._session.scalar(
                select(func.count(Person.id)).where(Person.capability_id == capability_id)
            )
            or 0
        )
        active_people_count = int(
            await self._session.scalar(
                select(func.count(Person.id)).where(
                    Person.capability_id == capability_id,
                    Person.is_active.is_(True),
                )
            )
            or 0
        )
        data_products_count = int(
            await self._session.scalar(
                select(func.count(DataProduct.id)).where(
                    DataProduct.capability_id == capability_id,
                )
            )
            or 0
        )
        open_work_items_count = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    WorkItem.capability_id == capability_id,
                    WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )
        projects_count = int(
            await self._session.scalar(
                select(func.count(Project.id)).where(Project.capability_id == capability_id)
            )
            or 0
        )
        internal_projects_count = int(
            await self._session.scalar(
                select(func.count(Project.id)).where(
                    Project.capability_id == capability_id,
                    Project.project_type == ProjectType.INTERNAL_PROJECT,
                )
            )
            or 0
        )

        return {
            "people_count": people_count,
            "active_people_count": active_people_count,
            "data_products_count": data_products_count,
            "open_work_items_count": open_work_items_count,
            "projects_count": projects_count,
            "internal_projects_count": internal_projects_count,
        }

    async def has_references(self, capability_id: uuid.UUID) -> bool:
        counts = await self.get_summary_counts(capability_id)
        return any(count > 0 for count in counts.values())
