import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.dependencies import get_db
from app.domain.enums import UserRole
from app.models.identity import User
from app.modules.auth.dependencies import require_active_user, require_admin
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    CurrentUser,
    LoginRequest,
    MessageResponse,
    TokenResponse,
    UserCreate,
    UserFilters,
    UserListResponse,
    UserRead,
    UserUpdate,
)
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db), db)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await service.login(payload)


@router.get("/me", response_model=CurrentUser)
async def get_me(
    current_user: User = Depends(require_active_user),
) -> CurrentUser:
    return CurrentUser.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    _current_user: User = Depends(require_active_user),
) -> MessageResponse:
    return MessageResponse(message="Logged out")


@router.get("/users", response_model=UserListResponse)
async def list_users(
    search: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    _admin: User = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> UserListResponse:
    filters = UserFilters(search=search, role=role, is_active=is_active)
    return await service.list_users(filters=filters, page=page, page_size=page_size)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    _admin: User = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> UserRead:
    return await service.create_user(payload)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    _admin: User = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> UserRead:
    return await service.get_user(user_id)


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    _admin: User = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> UserRead:
    return await service.update_user(user_id, payload)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: uuid.UUID,
    _admin: User = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.deactivate_user(user_id)
