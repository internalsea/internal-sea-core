import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import ActivityAction, ActivityEntityType, ProjectType
from app.models.projects import Project
from app.modules.activity.helpers import get_updated_fields
from app.modules.activity.schemas import ActivityEventCreateInternal
from app.modules.activity.service import ActivityService
from app.modules.projects.errors import ProjectNotFoundError
from app.modules.projects.repository import ProjectListFilters, ProjectRepository
from app.modules.projects.schemas import (
    ProjectCreate,
    ProjectListItem,
    ProjectListResponse,
    ProjectRead,
    ProjectSummary,
    ProjectUpdate,
)
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields


class ProjectService:
    def __init__(self, repository: ProjectRepository, activity_service: ActivityService) -> None:
        self._repository = repository
        self._activity = activity_service

    def _project_entity_type(self, project: Project) -> ActivityEntityType:
        if project.project_type == ProjectType.INTERNAL_PROJECT:
            return ActivityEntityType.INTERNAL_PROJECT
        return ActivityEntityType.PROJECT

    async def list_projects(
        self,
        *,
        filters: ProjectListFilters,
        page: int,
        page_size: int,
    ) -> ProjectListResponse:
        normalized_page, normalized_page_size, offset = normalize_pagination(page, page_size)
        items, total = await self._repository.list_paginated(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return ProjectListResponse(
            items=[ProjectListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_project(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> ProjectRead:
        project = await self._repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        if company_id is not None:
            ensure_company_access(project, company_id, label="Project")
        return ProjectRead.model_validate(project)

    async def get_project_summary(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> ProjectSummary:
        project = await self._repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        if company_id is not None:
            ensure_company_access(project, company_id, label="Project")
        counts = await self._repository.get_summary_counts(project_id)
        return ProjectSummary(
            project=ProjectRead.model_validate(project),
            open_work_items=counts["open_work_items"],
            completed_work_items=counts["completed_work_items"],
            total_work_items=counts["total_work_items"],
            overdue_work_items=counts["overdue_work_items"],
        )

    async def create_project(
        self,
        payload: ProjectCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> ProjectRead:
        data = merge_tenant_fields(
            payload.model_dump(), company_id=company_id, workspace_id=workspace_id
        )
        project = await self._repository.create(data)
        entity_type = self._project_entity_type(project)
        title = (
            "Internal project created"
            if entity_type == ActivityEntityType.INTERNAL_PROJECT
            else "Project created"
        )
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=entity_type,
                entity_id=project.id,
                action=ActivityAction.CREATED,
                title=title,
            )
        )
        return ProjectRead.model_validate(project)

    async def update_project(
        self,
        project_id: uuid.UUID,
        payload: ProjectUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> ProjectRead:
        project = await self._repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        if company_id is not None:
            ensure_company_access(project, company_id, label="Project")
        update_data = payload.model_dump(exclude_unset=True)
        previous_status = project.status
        entity_type = self._project_entity_type(project)
        updated = await self._repository.update(project, update_data)
        if update_data:
            await self._activity.record_event(
                ActivityEventCreateInternal(
                    entity_type=entity_type,
                    entity_id=project_id,
                    action=ActivityAction.UPDATED,
                    title="Internal project updated"
                    if entity_type == ActivityEntityType.INTERNAL_PROJECT
                    else "Project updated",
                    details={"updated_fields": get_updated_fields(update_data)},
                )
            )
            if "status" in update_data and update_data["status"] != previous_status:
                await self._activity.record_event(
                    ActivityEventCreateInternal(
                        entity_type=entity_type,
                        entity_id=project_id,
                        action=ActivityAction.STATUS_CHANGED,
                        title="Internal project status changed"
                        if entity_type == ActivityEntityType.INTERNAL_PROJECT
                        else "Project status changed",
                        details={
                            "from_status": previous_status.value,
                            "to_status": update_data["status"].value
                            if hasattr(update_data["status"], "value")
                            else str(update_data["status"]),
                        },
                    )
                )
        return ProjectRead.model_validate(updated)

    async def delete_project(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> None:
        project = await self._repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        if company_id is not None:
            ensure_company_access(project, company_id, label="Project")
        entity_type = self._project_entity_type(project)
        await self._activity.record_event(
            ActivityEventCreateInternal(
                entity_type=entity_type,
                entity_id=project_id,
                action=ActivityAction.DELETED,
                title="Internal project deleted"
                if entity_type == ActivityEntityType.INTERNAL_PROJECT
                else "Project deleted",
            )
        )
        await self._repository.delete(project)

    async def get_internal_project(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> ProjectRead:
        project = await self._get_internal_project_model(project_id, company_id=company_id)
        return ProjectRead.model_validate(project)

    async def update_internal_project(
        self,
        project_id: uuid.UUID,
        payload: ProjectUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> ProjectRead:
        await self._get_internal_project_model(project_id, company_id=company_id)
        update_data = payload.model_dump(exclude_unset=True)
        update_data.pop("project_type", None)
        return await self.update_project(
            project_id, ProjectUpdate(**update_data), company_id=company_id
        )

    async def delete_internal_project(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> None:
        await self._get_internal_project_model(project_id, company_id=company_id)
        await self.delete_project(project_id, company_id=company_id)

    async def _get_internal_project_model(
        self, project_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> Project:
        project = await self._repository.get_by_id(project_id)
        if project is None or project.project_type != ProjectType.INTERNAL_PROJECT:
            raise ProjectNotFoundError(project_id)
        if company_id is not None:
            ensure_company_access(project, company_id, label="Internal project")
        return project
