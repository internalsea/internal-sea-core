import pytest
from app.modules.comments.schemas import CommentCreate, CommentUpdate
from pydantic import ValidationError


def test_comment_create_rejects_empty_body() -> None:
    with pytest.raises(ValidationError):
        CommentCreate(body="")


def test_comment_create_rejects_whitespace_body() -> None:
    with pytest.raises(ValidationError):
        CommentCreate(body="   ")


def test_comment_create_accepts_valid_body() -> None:
    payload = CommentCreate(body="Business owner confirmed this product is still active.")
    assert payload.body == "Business owner confirmed this product is still active."


def test_comment_update_rejects_empty_body() -> None:
    with pytest.raises(ValidationError):
        CommentUpdate(body="")
