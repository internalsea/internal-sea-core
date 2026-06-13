from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import User
from app.modules.auth.schemas import UserCreateInternal, UserFilters, UserUpdateInternal


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def list_users(
        self,
        filters: UserFilters,
        page: int,
        page_size: int,
    ) -> tuple[list[User], int]:
        query = select(User)
        count_query = select(func.count()).select_from(User)

        if filters.search:
            pattern = f"%{filters.search.strip()}%"
            condition = or_(User.email.ilike(pattern), User.full_name.ilike(pattern))
            query = query.where(condition)
            count_query = count_query.where(condition)
        if filters.role is not None:
            query = query.where(User.role == filters.role)
            count_query = count_query.where(User.role == filters.role)
        if filters.is_active is not None:
            query = query.where(User.is_active == filters.is_active)
            count_query = count_query.where(User.is_active == filters.is_active)

        total = int((await self._session.execute(count_query)).scalar_one())
        offset = (page - 1) * page_size
        result = await self._session.execute(
            query.order_by(User.updated_at.desc()).offset(offset).limit(page_size)
        )
        return list(result.scalars().all()), total

    async def count_users(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(User))
        return int(result.scalar_one())

    async def create_user(self, payload: UserCreateInternal) -> User:
        user = User(
            email=payload.email.lower(),
            full_name=payload.full_name,
            hashed_password=payload.hashed_password,
            role=payload.role,
            is_active=payload.is_active,
            is_superuser=payload.is_superuser,
        )
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update_user(self, user: User, payload: UserUpdateInternal) -> User:
        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.role is not None:
            user.role = payload.role
        if payload.is_active is not None:
            user.is_active = payload.is_active
        if payload.is_superuser is not None:
            user.is_superuser = payload.is_superuser
        if payload.hashed_password is not None:
            user.hashed_password = payload.hashed_password
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update_last_login(self, user: User) -> User:
        from datetime import UTC, datetime

        user.last_login_at = datetime.now(UTC)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def deactivate_user(self, user: User) -> User:
        user.is_active = False
        await self._session.flush()
        await self._session.refresh(user)
        return user
