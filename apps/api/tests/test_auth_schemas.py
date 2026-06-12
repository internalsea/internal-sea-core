import pytest
from pydantic import ValidationError

from app.modules.auth.schemas import LoginRequest, UserCreate, UserRead


def test_login_request_validates_email() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password="secret12345")


def test_user_create_requires_password_length() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="short")


def test_user_read_excludes_hashed_password() -> None:
    fields = set(UserRead.model_fields.keys())
    assert "hashed_password" not in fields
