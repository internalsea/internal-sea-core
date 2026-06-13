"""Tests for tenancy dependencies."""

import uuid
from unittest.mock import AsyncMock

import pytest
from app.domain.enums import CompanyMemberRole, CompanyMemberStatus, UserRole
from app.models.identity import User
from app.models.tenancy import CompanyMember
from app.modules.tenancy.dependencies import ROLE_RANK, get_current_company_id
from app.modules.tenancy.errors import TenantSelectionRequiredError


@pytest.mark.asyncio
async def test_single_membership_auto_selects_company() -> None:
    user = User(
        id=uuid.uuid4(),
        email="u@example.com",
        role=UserRole.VIEWER,
        is_active=True,
    )
    company_id = uuid.uuid4()
    member = CompanyMember(
        company_id=company_id,
        user_id=user.id,
        role=CompanyMemberRole.VIEWER.value,
        status=CompanyMemberStatus.ACTIVE.value,
    )
    repository = AsyncMock()
    repository.get_active_memberships.return_value = [member]

    result = await get_current_company_id(user=user, repository=repository, x_company_id=None)
    assert result == company_id


@pytest.mark.asyncio
async def test_multiple_memberships_requires_selection() -> None:
    user = User(
        id=uuid.uuid4(),
        email="u@example.com",
        role=UserRole.VIEWER,
        is_active=True,
    )
    repository = AsyncMock()
    repository.get_active_memberships.return_value = [
        CompanyMember(company_id=uuid.uuid4(), user_id=user.id, role="viewer", status="active"),
        CompanyMember(company_id=uuid.uuid4(), user_id=user.id, role="viewer", status="active"),
    ]
    repository.get_first_company.return_value = None

    with pytest.raises(TenantSelectionRequiredError):
        await get_current_company_id(user=user, repository=repository, x_company_id=None)


def test_role_rank_order() -> None:
    assert ROLE_RANK[CompanyMemberRole.OWNER] > ROLE_RANK[CompanyMemberRole.ADMIN]
