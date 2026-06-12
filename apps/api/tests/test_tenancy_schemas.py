"""Tests for tenancy Pydantic schemas."""

import uuid

import pytest
from pydantic import ValidationError

from app.domain.enums import CompanyStatus, Industry
from app.modules.tenancy.schemas import (
    CompanyCreate,
    CompanyRead,
    FirstUserOnboardingRequest,
)


def test_company_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        CompanyCreate(name="")


def test_company_create_slug_optional() -> None:
    company = CompanyCreate(name="Acme Corp")
    assert company.slug is None
    assert company.status == CompanyStatus.TRIAL


def test_first_user_onboarding_requires_fields() -> None:
    payload = FirstUserOnboardingRequest(
        full_name="Jane Doe",
        email="jane@example.com",
        password="securepass1",
        company_name="Acme",
    )
    assert payload.company_name == "Acme"


def test_company_read_from_attributes() -> None:
    now = "2026-01-01T00:00:00Z"
    data = {
        "id": uuid.uuid4(),
        "name": "Test",
        "slug": "test",
        "description": None,
        "industry": Industry.TECHNOLOGY.value,
        "company_size": None,
        "country": None,
        "website": None,
        "status": CompanyStatus.ACTIVE.value,
        "created_at": now,
        "updated_at": now,
    }
    # Use model_validate with a simple namespace object
    class Obj:
        pass

    obj = Obj()
    for k, v in data.items():
        setattr(obj, k, v)
    from datetime import datetime

    obj.created_at = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
    obj.updated_at = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
    read = CompanyRead.model_validate(obj)
    assert read.slug == "test"
