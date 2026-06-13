import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.modules.teams.errors import TeamConflictError, TeamNotFoundError
from app.modules.teams.repository import TeamListFilters, TeamRepository
from app.modules.teams.schemas import (
    TeamCreate,
    TeamListItem,
    TeamListResponse,
    TeamRead,
    TeamSummary,
    TeamUpdate,
)
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields


class TeamService:
    def __init__(self, repository: TeamRepository) -> None:
        self._repository = repository

    async def list_teams(
        self,
        *,
        filters: TeamListFilters,
        page: int,
        page_size: int,
    ) -> TeamListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_paginated(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return TeamListResponse(
            items=[TeamListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_team(
        self, team_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> TeamRead:
        team = await self._repository.get_by_id(team_id)
        if team is None:
            raise TeamNotFoundError(team_id)
        if company_id is not None:
            ensure_company_access(team, company_id, label="Team")
        return TeamRead.model_validate(team)

    async def get_team_summary(
        self, team_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> TeamSummary:
        team = await self._repository.get_by_id(team_id)
        if team is None:
            raise TeamNotFoundError(team_id)
        if company_id is not None:
            ensure_company_access(team, company_id, label="Team")
        counts = await self._repository.get_summary_counts(team_id)
        return TeamSummary(
            team=TeamRead.model_validate(team),
            people_count=counts["people_count"],
            active_people_count=counts["active_people_count"],
            data_products_count=counts["data_products_count"],
            open_work_items_count=counts["open_work_items_count"],
            projects_count=counts["projects_count"],
            internal_projects_count=counts["internal_projects_count"],
        )

    async def create_team(
        self,
        payload: TeamCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> TeamRead:
        existing = await self._repository.get_by_name(payload.name)
        if existing is not None:
            raise TeamConflictError(f"Team with name '{payload.name}' already exists")
        data = merge_tenant_fields(
            payload.model_dump(), company_id=company_id, workspace_id=workspace_id
        )
        team = await self._repository.create(data)
        return TeamRead.model_validate(team)

    async def update_team(
        self,
        team_id: uuid.UUID,
        payload: TeamUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> TeamRead:
        team = await self._repository.get_by_id(team_id)
        if team is None:
            raise TeamNotFoundError(team_id)
        if company_id is not None:
            ensure_company_access(team, company_id, label="Team")
        update_data = payload.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] is not None:
            existing = await self._repository.get_by_name(update_data["name"])
            if existing is not None and existing.id != team_id:
                raise TeamConflictError(f"Team with name '{update_data['name']}' already exists")
        updated = await self._repository.update(team, update_data)
        return TeamRead.model_validate(updated)

    async def delete_team(self, team_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> None:
        team = await self._repository.get_by_id(team_id)
        if team is None:
            raise TeamNotFoundError(team_id)
        if company_id is not None:
            ensure_company_access(team, company_id, label="Team")
        if await self._repository.has_references(team_id):
            raise TeamConflictError(
                "Cannot delete team while people, data products, work items, "
                "or projects reference it"
            )
        await self._repository.delete(team)
