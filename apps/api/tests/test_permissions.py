from app.domain.enums import UserRole
from app.models.identity import User
from app.modules.auth.permissions import can_admin, can_read, can_write


def _user(role: UserRole, *, is_superuser: bool = False, is_active: bool = True) -> User:
    return User(
        email=f"{role.value}@example.com",
        full_name=role.value.title(),
        role=role,
        is_superuser=is_superuser,
        is_active=is_active,
    )


def test_role_permission_helpers() -> None:
    assert can_read(_user(UserRole.VIEWER)) is True
    assert can_write(_user(UserRole.VIEWER)) is False
    assert can_write(_user(UserRole.EDITOR)) is True
    assert can_admin(_user(UserRole.EDITOR)) is False
    assert can_admin(_user(UserRole.ADMIN)) is True
    assert can_write(_user(UserRole.VIEWER, is_superuser=True)) is True
    assert can_read(_user(UserRole.VIEWER, is_active=False)) is False
