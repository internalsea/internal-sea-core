"""Tenancy business logic."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.pagination import calculate_pages, normalize_pagination
from app.domain.enums import (
    CompanyMemberRole,
    CompanyMemberStatus,
    CompanyStatus,
    UserRole,
    WorkspaceStatus,
)
from app.models.identity import User
from app.models.people import Capability, Person, Team
from app.models.tenancy import CompanyMember
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreateInternal
from app.modules.auth.security import create_access_token, hash_password, validate_password_strength
from app.modules.auth.service import AuthService
from app.modules.tenancy.errors import (
    CompanyConflictError,
    CompanyMemberNotFoundError,
    CompanyNotFoundError,
    OnboardingNotAllowedError,
    TenantAccessDeniedError,
    WorkspaceNotFoundError,
)
from app.modules.tenancy.repository import TenancyRepository
from app.modules.tenancy.schemas import (
    CompanyCreate,
    CompanyListResponse,
    CompanyMemberCreate,
    CompanyMemberListResponse,
    CompanyMemberRead,
    CompanyMemberUpdate,
    CompanyRead,
    CompanyUpdate,
    CurrentTenantContext,
    FirstUserOnboardingRequest,
    FirstUserOnboardingResponse,
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceRead,
    WorkspaceUpdate,
)
from app.modules.tenancy.validators import ensure_unique_slug, slugify_name


class TenancyService:
    def __init__(self, repository: TenancyRepository, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session
        self._auth_repository = AuthRepository(session)

    async def _resolve_company_slug(self, name: str, slug: str | None = None) -> str:
        base = slugify_name(slug or name)
        existing = await self._repository.get_all_company_slugs()
        return ensure_unique_slug(base, existing)

    async def _resolve_workspace_slug(
        self,
        company_id: uuid.UUID,
        name: str,
        slug: str | None = None,
    ) -> str:
        base = slugify_name(slug or name)
        existing = await self._repository.get_workspace_slugs_for_company(company_id)
        return ensure_unique_slug(base, existing)

    async def create_company(self, payload: CompanyCreate, *, owner_user: User) -> CompanyRead:
        slug = await self._resolve_company_slug(payload.name, payload.slug)
        company = await self._repository.create_company(
            {
                "name": payload.name,
                "slug": slug,
                "description": payload.description,
                "industry": payload.industry.value if payload.industry else None,
                "company_size": payload.company_size.value if payload.company_size else None,
                "country": payload.country,
                "website": payload.website,
                "status": payload.status.value,
            }
        )
        workspace = await self._repository.create_workspace(
            {
                "company_id": company.id,
                "name": "Default Workspace",
                "slug": "default",
                "description": "Default workspace",
                "default_timezone": "UTC",
                "default_currency": "EUR",
                "status": WorkspaceStatus.ACTIVE.value,
            }
        )
        await self._repository.create_member(
            {
                "company_id": company.id,
                "user_id": owner_user.id,
                "role": CompanyMemberRole.OWNER.value,
                "status": CompanyMemberStatus.ACTIVE.value,
                "joined_at": self._repository.now_utc(),
            }
        )
        await self._session.commit()
        await self._session.refresh(company)
        await self._session.refresh(workspace)
        return CompanyRead.model_validate(company)

    async def update_company(self, company_id: uuid.UUID, payload: CompanyUpdate) -> CompanyRead:
        company = await self._repository.get_company_by_id(company_id)
        if company is None:
            raise CompanyNotFoundError(company_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data and data["name"] is not None:
            data["name"] = data["name"].strip()
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"].value
        if "industry" in data and data["industry"] is not None:
            data["industry"] = data["industry"].value
        if "company_size" in data and data["company_size"] is not None:
            data["company_size"] = data["company_size"].value
        if "slug" in data and data["slug"] is not None:
            data["slug"] = slugify_name(data["slug"])
        company = await self._repository.update_company(company, data)
        await self._session.commit()
        await self._session.refresh(company)
        return CompanyRead.model_validate(company)

    async def list_companies_for_current_user(
        self,
        *,
        page: int,
        page_size: int,
        user: User,
    ) -> CompanyListResponse:
        companies = await self._repository.get_user_companies(user.id)
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        total = len(companies)
        offset = (normalized_page - 1) * normalized_page_size
        page_items = companies[offset : offset + normalized_page_size]
        return CompanyListResponse(
            items=[CompanyRead.model_validate(c) for c in page_items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_company(self, company_id: uuid.UUID, *, user: User) -> CompanyRead:
        member = await self._repository.get_member(company_id, user.id)
        if member is None and not user.is_superuser:
            raise TenantAccessDeniedError()
        company = await self._repository.get_company_by_id(company_id)
        if company is None:
            raise CompanyNotFoundError(company_id)
        return CompanyRead.model_validate(company)

    async def create_workspace(self, payload: WorkspaceCreate) -> WorkspaceRead:
        company = await self._repository.get_company_by_id(payload.company_id)
        if company is None:
            raise CompanyNotFoundError(payload.company_id)
        slug = await self._resolve_workspace_slug(payload.company_id, payload.name, payload.slug)
        workspace = await self._repository.create_workspace(
            {
                "company_id": payload.company_id,
                "name": payload.name,
                "slug": slug,
                "description": payload.description,
                "default_timezone": payload.default_timezone,
                "default_currency": payload.default_currency,
                "status": payload.status.value,
            }
        )
        await self._session.commit()
        await self._session.refresh(workspace)
        return WorkspaceRead.model_validate(workspace)

    async def update_workspace(
        self,
        workspace_id: uuid.UUID,
        payload: WorkspaceUpdate,
    ) -> WorkspaceRead:
        workspace = await self._repository.get_workspace_by_id(workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundError(workspace_id)
        data = payload.model_dump(exclude_unset=True)
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"].value
        if "slug" in data and data["slug"] is not None:
            data["slug"] = slugify_name(data["slug"])
        workspace = await self._repository.update_workspace(workspace, data)
        await self._session.commit()
        await self._session.refresh(workspace)
        return WorkspaceRead.model_validate(workspace)

    async def list_workspaces(
        self,
        company_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> WorkspaceListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_workspaces(
            company_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return WorkspaceListResponse(
            items=[WorkspaceRead.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def get_current_tenant_context(
        self,
        *,
        user: User,
        company_id: uuid.UUID,
        workspace_id: uuid.UUID,
    ) -> CurrentTenantContext:
        company = await self._repository.get_company_by_id(company_id)
        if company is None:
            raise CompanyNotFoundError(company_id)
        workspace = await self._repository.get_workspace_by_id(workspace_id)
        if workspace is None or workspace.company_id != company_id:
            raise WorkspaceNotFoundError(workspace_id)
        member = await self._repository.get_member(company_id, user.id)
        if member is None and not user.is_superuser:
            raise TenantAccessDeniedError()
        if member is None:
            member = CompanyMember(
                company_id=company_id,
                user_id=user.id,
                role=CompanyMemberRole.ADMIN.value,
                status=CompanyMemberStatus.ACTIVE.value,
            )
        return CurrentTenantContext(
            company=CompanyRead.model_validate(company),
            workspace=WorkspaceRead.model_validate(workspace),
            member=CompanyMemberRead.model_validate(member),
        )

    async def list_members(
        self,
        company_id: uuid.UUID,
        *,
        page: int,
        page_size: int,
    ) -> CompanyMemberListResponse:
        normalized_page, normalized_page_size = normalize_pagination(page, page_size)
        offset = (normalized_page - 1) * normalized_page_size
        items, total = await self._repository.list_members(
            company_id,
            offset=offset,
            limit=normalized_page_size,
        )
        return CompanyMemberListResponse(
            items=[CompanyMemberRead.model_validate(item) for item in items],
            total=total,
            page=normalized_page,
            page_size=normalized_page_size,
            pages=calculate_pages(total, normalized_page_size),
        )

    async def add_member(self, payload: CompanyMemberCreate) -> CompanyMemberRead:
        existing = await self._repository.get_member(payload.company_id, payload.user_id)
        if existing is not None:
            raise CompanyConflictError("User is already a member of this company")
        member = await self._repository.create_member(
            {
                "company_id": payload.company_id,
                "user_id": payload.user_id,
                "person_id": payload.person_id,
                "role": payload.role.value,
                "status": payload.status.value,
                "joined_at": self._repository.now_utc(),
            }
        )
        await self._session.commit()
        await self._session.refresh(member)
        return CompanyMemberRead.model_validate(member)

    async def update_member(
        self,
        member_id: uuid.UUID,
        payload: CompanyMemberUpdate,
    ) -> CompanyMemberRead:
        member = await self._repository.get_member_by_id(member_id)
        if member is None:
            raise CompanyMemberNotFoundError(member_id)
        data = payload.model_dump(exclude_unset=True)
        if "role" in data and data["role"] is not None:
            data["role"] = data["role"].value
        if "status" in data and data["status"] is not None:
            data["status"] = data["status"].value
        member = await self._repository.update_member(member, data)
        await self._session.commit()
        await self._session.refresh(member)
        return CompanyMemberRead.model_validate(member)

    async def remove_member(self, member_id: uuid.UUID) -> None:
        member = await self._repository.get_member_by_id(member_id)
        if member is None:
            raise CompanyMemberNotFoundError(member_id)
        await self._repository.update_member(
            member,
            {"status": CompanyMemberStatus.REMOVED.value},
        )
        await self._session.commit()

    async def first_user_onboarding(
        self,
        payload: FirstUserOnboardingRequest,
    ) -> FirstUserOnboardingResponse:
        user_count = await self._repository.count_users()
        company_count = await self._repository.count_companies()
        if user_count > 0 and company_count > 0:
            raise OnboardingNotAllowedError()

        validate_password_strength(payload.password)
        email = payload.email.strip().lower()
        if await self._auth_repository.get_user_by_email(email) is not None:
            raise CompanyConflictError("User with this email already exists")

        user = await self._auth_repository.create_user(
            UserCreateInternal(
                email=email,
                full_name=payload.full_name,
                hashed_password=hash_password(payload.password),
                role=UserRole.ADMIN,
                is_active=True,
                is_superuser=False,
            )
        )

        slug = await self._resolve_company_slug(payload.company_name)
        company = await self._repository.create_company(
            {
                "name": payload.company_name,
                "slug": slug,
                "industry": payload.industry.value if payload.industry else None,
                "company_size": payload.company_size.value if payload.company_size else None,
                "country": payload.country,
                "status": CompanyStatus.TRIAL.value,
            }
        )
        workspace = await self._repository.create_workspace(
            {
                "company_id": company.id,
                "name": "Default Workspace",
                "slug": "default",
                "default_timezone": "UTC",
                "default_currency": "EUR",
                "status": WorkspaceStatus.ACTIVE.value,
            }
        )

        team_name = payload.team_name or "Core Team"
        team = Team(
            name=team_name,
            description="Default team",
            company_id=company.id,
            workspace_id=workspace.id,
        )
        self._session.add(team)
        await self._session.flush()

        capability_name = payload.main_capability_name or "General"
        capability = Capability(
            name=capability_name,
            description="Default capability",
            company_id=company.id,
            workspace_id=workspace.id,
        )
        self._session.add(capability)
        await self._session.flush()

        person = Person(
            full_name=payload.full_name,
            email=email,
            user_id=user.id,
            team_id=team.id,
            capability_id=capability.id,
            company_id=company.id,
            workspace_id=workspace.id,
            is_active=True,
        )
        self._session.add(person)
        await self._session.flush()

        member = await self._repository.create_member(
            {
                "company_id": company.id,
                "user_id": user.id,
                "person_id": person.id,
                "role": CompanyMemberRole.OWNER.value,
                "status": CompanyMemberStatus.ACTIVE.value,
                "joined_at": self._repository.now_utc(),
            }
        )

        await self._session.commit()
        await self._session.refresh(user)
        await self._session.refresh(company)
        await self._session.refresh(workspace)
        await self._session.refresh(member)

        settings = get_settings()
        token = create_access_token(
            str(user.id),
            extra_claims={
                "email": user.email,
                "role": user.role.value,
                "is_superuser": user.is_superuser,
            },
        )
        return FirstUserOnboardingResponse(
            user=AuthService.to_current_user(user),
            company=CompanyRead.model_validate(company),
            workspace=WorkspaceRead.model_validate(workspace),
            member=CompanyMemberRead.model_validate(member),
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
        )
