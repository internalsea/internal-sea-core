"""Tests for tenancy service (mocked, no DB)."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import CompanyStatus, UserRole
from app.models.identity import User
from app.modules.tenancy.errors import OnboardingNotAllowedError
from app.modules.tenancy.repository import TenancyRepository
from app.modules.tenancy.schemas import FirstUserOnboardingRequest
from app.modules.tenancy.service import TenancyService


@pytest.mark.asyncio
async def test_first_user_onboarding_blocked_when_company_exists() -> None:
    repository = AsyncMock(spec=TenancyRepository)
    repository.count_users.return_value = 5
    repository.count_companies.return_value = 1
    session = AsyncMock()
    service = TenancyService(repository, session)

    with pytest.raises(OnboardingNotAllowedError):
        await service.first_user_onboarding(
            FirstUserOnboardingRequest(
                full_name="Jane",
                email="jane@example.com",
                password="password123",
                company_name="Acme",
            )
        )


@pytest.mark.asyncio
async def test_create_company_generates_slug() -> None:
    repository = AsyncMock(spec=TenancyRepository)
    repository.get_all_company_slugs.return_value = set()
    company = MagicMock()
    company.id = uuid.uuid4()
    company.name = "Acme"
    company.slug = "acme"
    company.description = None
    company.industry = None
    company.company_size = None
    company.country = None
    company.website = None
    company.status = CompanyStatus.TRIAL.value
    company.created_at = repository.now_utc()
    company.updated_at = repository.now_utc()
    repository.create_company.return_value = company
    workspace = MagicMock()
    workspace.id = uuid.uuid4()
    repository.create_workspace.return_value = workspace
    repository.create_member.return_value = MagicMock()
    repository.get_member.return_value = MagicMock(role="owner")
    user = User(email="u@example.com", full_name="User", role=UserRole.VIEWER)
    auth_repo = AsyncMock()
    auth_repo.update_user.return_value = user
    session = AsyncMock()

    service = TenancyService(repository, session)
    service._auth_repository = auth_repo
    from app.modules.tenancy.schemas import CompanyCreate

    result = await service.create_company(CompanyCreate(name="Acme Corp"), owner_user=user)
    assert result.name == "Acme"
    repository.create_company.assert_awaited_once()
    call_data = repository.create_company.await_args.args[0]
    assert call_data["slug"] == "acme-corp"
    auth_repo.update_user.assert_awaited_once()
