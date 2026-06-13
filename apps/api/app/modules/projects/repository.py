import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import ProjectStatus, ProjectType, WorkItemStatus
from app.models.projects import Project
from app.models.work import WorkItem

COMPLETED_WORK_ITEM_STATUSES = (WorkItemStatus.DONE, WorkItemStatus.CLOSED)


@dataclass
class ProjectListFilters:
    search: str | None = None
    project_type: ProjectType | None = None
    status: ProjectStatus | None = None
    client_name: str | None = None
    account_name: str | None = None
    owner_id: uuid.UUID | None = None
    team_id: uuid.UUID | None = None
    capability_id: uuid.UUID | None = None
    health_status: str | None = None
    starts_after: date | None = None
    ends_before: date | None = None
    company_id: uuid.UUID | None = None


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _apply_filters(self, query, filters: ProjectListFilters):
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(
                or_(
                    Project.name.ilike(pattern),
                    Project.description.ilike(pattern),
                    Project.client_name.ilike(pattern),
                    Project.account_name.ilike(pattern),
                )
            )
        if filters.project_type is not None:
            query = query.where(Project.project_type == filters.project_type)
        if filters.status is not None:
            query = query.where(Project.status == filters.status)
        if filters.client_name:
            query = query.where(Project.client_name.ilike(f"%{filters.client_name}%"))
        if filters.account_name:
            query = query.where(Project.account_name.ilike(f"%{filters.account_name}%"))
        if filters.owner_id is not None:
            query = query.where(Project.owner_id == filters.owner_id)
        if filters.team_id is not None:
            query = query.where(Project.team_id == filters.team_id)
        if filters.capability_id is not None:
            query = query.where(Project.capability_id == filters.capability_id)
        if filters.health_status is not None:
            query = query.where(Project.health_status == filters.health_status)
        if filters.starts_after is not None:
            query = query.where(Project.start_date >= filters.starts_after)
        if filters.ends_before is not None:
            query = query.where(Project.target_end_date <= filters.ends_before)
        if filters.company_id is not None:
            query = query.where(Project.company_id == filters.company_id)
        return query

    async def list(
        self,
        *,
        filters: ProjectListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Project], int]:
        base_query = select(Project)
        filtered_query = self._apply_filters(base_query, filters)

        count_query = self._apply_filters(select(func.count(Project.id)), filters)
        total = int(await self._session.scalar(count_query) or 0)

        result = await self._session.scalars(
            filtered_query.order_by(Project.updated_at.desc()).offset(offset).limit(limit)
        )
        return list(result.all()), total

    async def get_by_id(self, project_id: uuid.UUID) -> Project | None:
        return await self._session.get(Project, project_id)

    async def create(self, data: dict[str, object]) -> Project:
        project = Project(**data)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project)
        return project

    async def update(self, project: Project, data: dict[str, object]) -> Project:
        for field, value in data.items():
            setattr(project, field, value)
        await self._session.commit()
        await self._session.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        await self._session.delete(project)
        await self._session.commit()

    async def get_summary_counts(self, project_id: uuid.UUID) -> dict[str, int]:
        today = date.today()
        base = WorkItem.project_id == project_id

        total = int(await self._session.scalar(select(func.count(WorkItem.id)).where(base)) or 0)
        open_count = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    base,
                    WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )
        completed = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    base,
                    WorkItem.status.in_(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )
        overdue = int(
            await self._session.scalar(
                select(func.count(WorkItem.id)).where(
                    base,
                    WorkItem.due_date.is_not(None),
                    WorkItem.due_date < today,
                    WorkItem.status.not_in(COMPLETED_WORK_ITEM_STATUSES),
                )
            )
            or 0
        )

        return {
            "total_work_items": total,
            "open_work_items": open_count,
            "completed_work_items": completed,
            "overdue_work_items": overdue,
        }
