import pytest
from pydantic import ValidationError

from app.domain.enums import SeniorityLevel
from app.modules.people.schemas import PersonCreate, PersonUpdate


def test_person_create_valid_payload() -> None:
    payload = PersonCreate(
        full_name="Nikita Rogatov",
        email="nikita@example.com",
        role_title="Partner, Data Engineering and Cloud",
        seniority_level=SeniorityLevel.PARTNER,
        availability_percent=80,
        location="Netherlands",
    )
    assert payload.full_name == "Nikita Rogatov"
    assert payload.seniority_level == SeniorityLevel.PARTNER


def test_person_create_rejects_empty_full_name() -> None:
    with pytest.raises(ValidationError):
        PersonCreate(full_name="")


def test_person_create_rejects_availability_below_zero() -> None:
    with pytest.raises(ValidationError):
        PersonCreate(full_name="Test Person", availability_percent=-1)


def test_person_create_rejects_availability_above_hundred() -> None:
    with pytest.raises(ValidationError):
        PersonCreate(full_name="Test Person", availability_percent=101)


def test_person_update_allows_partial_payload() -> None:
    payload = PersonUpdate(location="Amsterdam")
    data = payload.model_dump(exclude_unset=True)
    assert data == {"location": "Amsterdam"}


def test_person_update_rejects_empty_full_name() -> None:
    with pytest.raises(ValidationError):
        PersonUpdate(full_name="")
