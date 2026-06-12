import pytest
from pydantic import ValidationError

from app.modules.capabilities.schemas import CapabilityCreate, CapabilityUpdate


def test_capability_create_valid_payload() -> None:
    payload = CapabilityCreate(
        name="Data Engineering",
        description="Builds and operates data pipelines, data products and platform integrations.",
    )
    assert payload.name == "Data Engineering"


def test_capability_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        CapabilityCreate(name="")


def test_capability_update_allows_partial_payload() -> None:
    payload = CapabilityUpdate(description="Updated description")
    data = payload.model_dump(exclude_unset=True)
    assert data == {"description": "Updated description"}


def test_capability_update_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        CapabilityUpdate(name="")
