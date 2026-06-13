import pytest
from app.modules.teams.schemas import TeamCreate, TeamUpdate
from pydantic import ValidationError


def test_team_create_valid_payload() -> None:
    payload = TeamCreate(
        name="Core Platform Team",
        description="Internal Sea product and platform team.",
    )
    assert payload.name == "Core Platform Team"


def test_team_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        TeamCreate(name="")


def test_team_update_allows_partial_payload() -> None:
    payload = TeamUpdate(description="Updated description")
    data = payload.model_dump(exclude_unset=True)
    assert data == {"description": "Updated description"}


def test_team_update_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        TeamUpdate(name="")
