import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import get_model
from app.domain.enums import ProjectType, WorkItemStatus
from app.models.catalog import DataProduct
from app.models.people import Person, Team
from app.models.projects import Project
from app.models.work import WorkItem

COMPLETED_WORK_ITEM_STATUSES = (WorkItemStatus.DONE, WorkItemStatus.CLOSED)


@dataclass
class TeamListFilters:
    search: str | None = None
    company_id: uuid.UUID | None = None


class TeamRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query: Any, filters: TeamListFilters) -> Any:
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    Team.name.ilike(pattern),
                    Team.description.ilike(pattern),
                )
            )
        if filters.company_id is not None:
            query = query.where(Team.company_id == filters.company_id)
        return query

    async def list_paginated(
        self,
        *,
        filters: TeamListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Team], int]:
        base_query = select(Team)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(Team.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(Team.name.asc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_by_id(self, team_id: uuid.UUID) -> Team | None:
        return await get_model(self._session, Team, team_id)

    async def get_by_name(self, name: str) -> Team | None:
        return await self._session.scalar(select(Team).where(Team.name == name))

    async def create(self, data: dict[str, object]) -> Team:
        team = Team(**data)
        self._session.add(team)
        await self._session.commit()
        await self._session.refresh(team)
        return team

    async def update(self, team: Team, data: dict[str, object]) -> Team:
        for field, value in data.items():
            setattr(team, field, value)
        await self._session.commit()
        await self._session.refresh(team)
        return team

    async def delete(self, team: Team) -> None:
        await self._session.delete(team)
        await self._session.commit()

    async def get_summary_counts(self, team_id: uuid.UUID) -> dict[str, int]:
        people_count = int(
            await self._session.scalar(
                select(func.count(Person.id)).where(Person.team_id == team_id)
            )
            or 0
        )
        active_people_count = int(
            await self._session.scalar(
                select(func.count(Person.id)).where(
                    Person.team_id == team_id,
                    Person.is_active.is_(True),
                )
            )
            or 0
        )
        data_products_count = int(
            await self._session.scalar(
                select(func.count(DataProduct.id)).where(DataProduct.team_id == team_id)
            )
            or 0
        )
        open_work_items_count = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    WorkItem.team_id == team_id,
                    WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )
        projects_count = int(
            await self._session.scalar(
                select(func.count(Project.id)).where(Project.team_id == team_id)
            )
            or 0
        )
        internal_projects_count = int(
            await self._session.scalar(
                select(func.count(Project.id)).where(
                    Project.team_id == team_id,
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

    async def has_references(self, team_id: uuid.UUID) -> bool:
        counts = await self.get_summary_counts(team_id)
        return any(count > 0 for count in counts.values())
