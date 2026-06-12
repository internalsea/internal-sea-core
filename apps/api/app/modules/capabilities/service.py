import uuid

from app.core.pagination import calculate_pages, normalize_pagination
from app.modules.capabilities.errors import CapabilityConflictError, CapabilityNotFoundError
from app.modules.tenancy.scope import ensure_company_access, merge_tenant_fields
from app.modules.capabilities.repository import CapabilityListFilters, CapabilityRepository
from app.modules.capabilities.schemas import (
    CapabilityCreate,
    CapabilityListItem,
    CapabilityListResponse,
    CapabilityRead,
    CapabilitySummary,
    CapabilityUpdate,
)


class CapabilityService:
    def __init__(self, repository: CapabilityRepository) -> None:
        self._repository = repository

    async def list_capabilities(
        self,
        *,
        filters: CapabilityListFilters,
        page: int,
        page_size: int,
    ) -> CapabilityListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list(
            filters=filters,
            offset=offset,
            limit=normalized_page_size,
        )
        return CapabilityListResponse(
            items=[CapabilityListItem.model_validate(item) for item in items],
            page=normalized_page,
            page_size=normalized_page_size,
            total=total,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_capability(self, capability_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> CapabilityRead:
        capability = await self._repository.get_by_id(capability_id)
        if capability is None:
            raise CapabilityNotFoundError(capability_id)
        if company_id is not None:
            ensure_company_access(capability, company_id, label="Capability")
        return CapabilityRead.model_validate(capability)

    async def get_capability_summary(
        self, capability_id: uuid.UUID, *, company_id: uuid.UUID | None = None
    ) -> CapabilitySummary:
        capability = await self._repository.get_by_id(capability_id)
        if capability is None:
            raise CapabilityNotFoundError(capability_id)
        if company_id is not None:
            ensure_company_access(capability, company_id, label="Capability")
        counts = await self._repository.get_summary_counts(capability_id)
        return CapabilitySummary(
            capability=CapabilityRead.model_validate(capability),
            people_count=counts["people_count"],
            active_people_count=counts["active_people_count"],
            data_products_count=counts["data_products_count"],
            open_work_items_count=counts["open_work_items_count"],
            projects_count=counts["projects_count"],
            internal_projects_count=counts["internal_projects_count"],
        )

    async def create_capability(
        self,
        payload: CapabilityCreate,
        *,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> CapabilityRead:
        existing = await self._repository.get_by_name(payload.name)
        if existing is not None:
            raise CapabilityConflictError(
                f"Capability with name '{payload.name}' already exists"
            )
        data = merge_tenant_fields(payload.model_dump(), company_id=company_id, workspace_id=workspace_id)
        capability = await self._repository.create(data)
        return CapabilityRead.model_validate(capability)

    async def update_capability(
        self,
        capability_id: uuid.UUID,
        payload: CapabilityUpdate,
        *,
        company_id: uuid.UUID | None = None,
    ) -> CapabilityRead:
        capability = await self._repository.get_by_id(capability_id)
        if capability is None:
            raise CapabilityNotFoundError(capability_id)
        if company_id is not None:
            ensure_company_access(capability, company_id, label="Capability")
        update_data = payload.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] is not None:
            existing = await self._repository.get_by_name(update_data["name"])
            if existing is not None and existing.id != capability_id:
                raise CapabilityConflictError(
                    f"Capability with name '{update_data['name']}' already exists"
                )
        updated = await self._repository.update(capability, update_data)
        return CapabilityRead.model_validate(updated)

    async def delete_capability(self, capability_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> None:
        capability = await self._repository.get_by_id(capability_id)
        if capability is None:
            raise CapabilityNotFoundError(capability_id)
        if company_id is not None:
            ensure_company_access(capability, company_id, label="Capability")
        if await self._repository.has_references(capability_id):
            raise CapabilityConflictError(
                "Cannot delete capability while people, data products, work items or projects "
                "reference it"
            )
        await self._repository.delete(capability)
