import pytest
from pydantic import ValidationError

from app.modules.auth.schemas import LoginRequest, RegisterRequest, UserCreate, UserRead


def test_login_request_validates_email() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password="secret12345")


def test_register_request_validates_email_and_full_name() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(email="not-an-email", full_name="User", password="secret12345")
    with pytest.raises(ValidationError):
        RegisterRequest(email="user@example.com", full_name="   ", password="secret12345")


def test_user_create_requires_password_length() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="short")


def test_user_read_excludes_hashed_password() -> None:
    fields = set(UserRead.model_fields.keys())
    assert "hashed_password" not in fields
