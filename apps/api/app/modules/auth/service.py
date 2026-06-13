from __future__ import annotations

import math
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.domain.enums import UserRole
from app.models.identity import User
from app.modules.auth.errors import (
    DuplicateUserEmailError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    CurrentUser,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserCreate,
    UserCreateInternal,
    UserFilters,
    UserListItem,
    UserListResponse,
    UserRead,
    UserUpdate,
    UserUpdateInternal,
)
from app.modules.auth.security import (
    create_access_token,
    hash_password,
    validate_password_strength,
    verify_password,
)


class AuthService:
    def __init__(self, repository: AuthRepository, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    @staticmethod
    def to_current_user(user: User) -> CurrentUser:
        return CurrentUser.model_validate(user)

    @staticmethod
    def to_user_read(user: User) -> UserRead:
        return UserRead.model_validate(user)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self._repository.get_user_by_email(email.strip().lower())
        if user is None or not user.hashed_password:
            raise InvalidCredentialsError()
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError()
        return user

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.authenticate_user(payload.email, payload.password)
        return await self._issue_token_response(user, update_last_login=True)

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        validate_password_strength(payload.password)
        email = payload.email.strip().lower()
        existing = await self._repository.get_user_by_email(email)
        if existing is not None:
            raise DuplicateUserEmailError()

        user = await self._repository.create_user(
            UserCreateInternal(
                email=email,
                full_name=payload.full_name,
                hashed_password=hash_password(payload.password),
                role=UserRole.VIEWER,
                is_active=True,
                is_superuser=False,
            )
        )
        await self._session.commit()
        await self._session.refresh(user)
        return await self._issue_token_response(user, update_last_login=False)

    async def _issue_token_response(self, user: User, *, update_last_login: bool) -> TokenResponse:
        if update_last_login:
            await self._repository.update_last_login(user)
            await self._session.commit()
            await self._session.refresh(user)

        settings = get_settings()
        token = create_access_token(
            str(user.id),
            extra_claims={
                "email": user.email,
                "role": user.role.value,
                "is_superuser": user.is_superuser,
            },
        )
        return TokenResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=self.to_current_user(user),
        )

    async def get_current_user_by_id(self, user_id: uuid.UUID) -> CurrentUser:
        user = await self._repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_active:
            raise InactiveUserError()
        return self.to_current_user(user)

    async def get_user(self, user_id: uuid.UUID) -> UserRead:
        user = await self._repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return self.to_user_read(user)

    async def list_users(
        self,
        filters: UserFilters,
        page: int,
        page_size: int,
    ) -> UserListResponse:
        items, total = await self._repository.list_users(filters, page, page_size)
        pages = math.ceil(total / page_size) if total else 0
        return UserListResponse(
            items=[UserListItem.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )

    async def create_user(self, payload: UserCreate) -> UserRead:
        validate_password_strength(payload.password)
        email = payload.email.strip().lower()
        existing = await self._repository.get_user_by_email(email)
        if existing is not None:
            raise DuplicateUserEmailError()

        role = payload.role
        is_superuser = payload.is_superuser
        if is_superuser and role != UserRole.ADMIN:
            role = UserRole.ADMIN

        user = await self._repository.create_user(
            UserCreateInternal(
                email=email,
                full_name=payload.full_name,
                hashed_password=hash_password(payload.password),
                role=role,
                is_active=payload.is_active,
                is_superuser=is_superuser,
            )
        )
        await self._session.commit()
        return self.to_user_read(user)

    async def update_user(self, user_id: uuid.UUID, payload: UserUpdate) -> UserRead:
        user = await self._repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        update_data = UserUpdateInternal(
            full_name=payload.full_name,
            role=payload.role,
            is_active=payload.is_active,
            is_superuser=payload.is_superuser,
        )
        if payload.password is not None:
            validate_password_strength(payload.password)
            update_data.hashed_password = hash_password(payload.password)

        if update_data.is_superuser and update_data.role not in (None, UserRole.ADMIN):
            update_data.role = UserRole.ADMIN
        elif update_data.role == UserRole.ADMIN and update_data.is_superuser is None:
            pass

        user = await self._repository.update_user(user, update_data)
        await self._session.commit()
        return self.to_user_read(user)

    async def deactivate_user(self, user_id: uuid.UUID) -> None:
        user = await self._repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        await self._repository.deactivate_user(user)
        await self._session.commit()
