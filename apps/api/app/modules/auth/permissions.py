"""Simple role-based permission helpers."""

from app.domain.enums import UserRole
from app.models.identity import User


def can_read(user: User) -> bool:
    return user.is_active


def can_write(user: User) -> bool:
    if user.is_superuser:
        return True
    return user.is_active and user.role in {UserRole.EDITOR, UserRole.ADMIN}


def can_admin(user: User) -> bool:
    if user.is_superuser:
        return True
    return user.is_active and user.role == UserRole.ADMIN


def can_manage_users(user: User) -> bool:
    return can_admin(user)
