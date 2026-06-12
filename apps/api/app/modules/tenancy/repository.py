"""Tenancy data access."""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import CompanyMemberStatus, CompanyStatus, WorkspaceStatus
from app.models.identity import User
from app.models.tenancy import Company, CompanyMember, Workspace


@dataclass
class CompanyListFilters:
    search: str | None = None
    status: CompanyStatus | None = None


class TenancyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def count_users(self) -> int:
        return int(await self._session.scalar(select(func.count()).select_from(User)) or 0)

    async def count_companies(self) -> int:
        return int(await self._session.scalar(select(func.count()).select_from(Company)) or 0)

    async def list_companies(
        self,
        *,
        filters: CompanyListFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[Company], int]:
        query = select(Company)
        if filters.search:
            pattern = f"%{filters.search}%"
            query = query.where(Company.name.ilike(pattern) | Company.slug.ilike(pattern))
        if filters.status is not None:
            query = query.where(Company.status == filters.status.value)

        total = int(await self._session.scalar(select(func.count()).select_from(query.subquery())) or 0)
        items = list(
            await self._session.scalars(
                query.order_by(Company.name.asc()).offset(offset).limit(limit)
            )
        )
        return items, total

    async def get_company_by_id(self, company_id: uuid.UUID) -> Company | None:
        return await self._session.get(Company, company_id)

    async def get_company_by_slug(self, slug: str) -> Company | None:
        result = await self._session.execute(select(Company).where(Company.slug == slug))
        return result.scalar_one_or_none()

    async def get_all_company_slugs(self) -> set[str]:
        result = await self._session.scalars(select(Company.slug))
        return set(result.all())

    async def create_company(self, data: dict) -> Company:
        company = Company(**data)
        self._session.add(company)
        await self._session.flush()
        return company

    async def update_company(self, company: Company, data: dict) -> Company:
        for key, value in data.items():
            setattr(company, key, value)
        await self._session.flush()
        return company

    async def delete_company(self, company: Company) -> None:
        await self._session.delete(company)

    async def list_workspaces(
        self,
        company_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Workspace], int]:
        base = select(Workspace).where(Workspace.company_id == company_id)
        total = int(
            await self._session.scalar(
                select(func.count()).select_from(base.subquery())
            )
            or 0
        )
        items = list(
            await self._session.scalars(
                base.order_by(Workspace.name.asc()).offset(offset).limit(limit)
            )
        )
        return items, total

    async def get_workspace_by_id(self, workspace_id: uuid.UUID) -> Workspace | None:
        return await self._session.get(Workspace, workspace_id)

    async def get_default_workspace_for_company(self, company_id: uuid.UUID) -> Workspace | None:
        result = await self._session.execute(
            select(Workspace)
            .where(
                Workspace.company_id == company_id,
                Workspace.status == WorkspaceStatus.ACTIVE.value,
            )
            .order_by(Workspace.created_at.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_workspace_slugs_for_company(self, company_id: uuid.UUID) -> set[str]:
        result = await self._session.scalars(
            select(Workspace.slug).where(Workspace.company_id == company_id)
        )
        return set(result.all())

    async def create_workspace(self, data: dict) -> Workspace:
        workspace = Workspace(**data)
        self._session.add(workspace)
        await self._session.flush()
        return workspace

    async def update_workspace(self, workspace: Workspace, data: dict) -> Workspace:
        for key, value in data.items():
            setattr(workspace, key, value)
        await self._session.flush()
        return workspace

    async def list_members(
        self,
        company_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[CompanyMember], int]:
        base = select(CompanyMember).where(CompanyMember.company_id == company_id)
        total = int(
            await self._session.scalar(select(func.count()).select_from(base.subquery())) or 0
        )
        items = list(
            await self._session.scalars(
                base.order_by(CompanyMember.created_at.asc()).offset(offset).limit(limit)
            )
        )
        return items, total

    async def get_member(self, company_id: uuid.UUID, user_id: uuid.UUID) -> CompanyMember | None:
        result = await self._session.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == company_id,
                CompanyMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_member_by_id(self, member_id: uuid.UUID) -> CompanyMember | None:
        return await self._session.get(CompanyMember, member_id)

    async def create_member(self, data: dict) -> CompanyMember:
        member = CompanyMember(**data)
        self._session.add(member)
        await self._session.flush()
        return member

    async def update_member(self, member: CompanyMember, data: dict) -> CompanyMember:
        for key, value in data.items():
            setattr(member, key, value)
        await self._session.flush()
        return member

    async def get_user_companies(self, user_id: uuid.UUID) -> list[Company]:
        result = await self._session.scalars(
            select(Company)
            .join(CompanyMember, CompanyMember.company_id == Company.id)
            .where(
                CompanyMember.user_id == user_id,
                CompanyMember.status == CompanyMemberStatus.ACTIVE.value,
            )
            .order_by(Company.name.asc())
        )
        return list(result.all())

    async def get_active_memberships(self, user_id: uuid.UUID) -> list[CompanyMember]:
        result = await self._session.scalars(
            select(CompanyMember).where(
                CompanyMember.user_id == user_id,
                CompanyMember.status == CompanyMemberStatus.ACTIVE.value,
            )
        )
        return list(result.all())

    async def get_first_company(self) -> Company | None:
        result = await self._session.execute(
            select(Company).order_by(Company.created_at.asc()).limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def calculate_pages(total: int, page_size: int) -> int:
        return math.ceil(total / page_size) if total else 0

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)
