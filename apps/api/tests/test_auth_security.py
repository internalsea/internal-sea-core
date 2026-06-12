from datetime import timedelta

import jwt
import pytest

from app.config import get_settings
from app.modules.auth.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    validate_password_strength,
    verify_password,
)
from app.core.errors import ValidationError


def test_hash_password_does_not_return_plaintext() -> None:
    hashed = hash_password("secret12345")
    assert hashed != "secret12345"
    assert hashed.startswith("$2")


def test_verify_password_works() -> None:
    hashed = hash_password("secret12345")
    assert verify_password("secret12345", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_and_decode_token() -> None:
    token = create_access_token(
        "user-id",
        extra_claims={"email": "a@example.com", "role": "admin", "is_superuser": True},
    )
    payload = decode_access_token(token)
    assert payload["sub"] == "user-id"
    assert payload["email"] == "a@example.com"
    assert payload["role"] == "admin"
    assert payload["is_superuser"] is True


def test_invalid_token_rejected() -> None:
    with pytest.raises(jwt.PyJWTError):
        decode_access_token("not-a-valid-token")


def test_validate_password_strength_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        validate_password_strength("short")
