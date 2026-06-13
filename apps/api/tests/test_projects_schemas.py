from datetime import date
from decimal import Decimal

import pytest
from app.domain.enums import ProjectStatus, ProjectType
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate
from pydantic import ValidationError


def test_project_create_valid_payload() -> None:
    payload = ProjectCreate(
        name="Finance Data Platform Migration",
        description="Client migration project",
        project_type=ProjectType.CLIENT_PROJECT,
        status=ProjectStatus.ACTIVE,
        client_name="Example Client",
        health_status="healthy",
    )
    assert payload.name == "Finance Data Platform Migration"
    assert payload.project_type == ProjectType.CLIENT_PROJECT


def test_project_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(name="")


def test_project_update_allows_partial_payload() -> None:
    payload = ProjectUpdate(status=ProjectStatus.COMPLETED)
    data = payload.model_dump(exclude_unset=True)
    assert data == {"status": ProjectStatus.COMPLETED}


def test_project_create_rejects_target_end_before_start() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(
            name="Invalid Dates",
            start_date=date(2026, 6, 15),
            target_end_date=date(2026, 6, 1),
        )


def test_project_update_rejects_actual_end_before_start() -> None:
    with pytest.raises(ValidationError):
        ProjectUpdate(
            start_date=date(2026, 6, 15),
            actual_end_date=date(2026, 6, 1),
        )


def test_project_create_rejects_negative_budget() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(name="Budget Test", budget_amount=Decimal("-1.00"))
