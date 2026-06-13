import uuid
from collections.abc import Generator
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from app.config import get_settings
from app.domain.enums import (
    CompanyMemberRole,
    CompanyMemberStatus,
    CompanyStatus,
    WorkspaceStatus,
)
from app.main import create_app
from app.models.tenancy import Company, CompanyMember, Workspace
from app.modules.auth.dependencies import DEV_BYPASS_USER_ID
from fastapi.testclient import TestClient

_TEST_COMPANY_ID = uuid.UUID("00000000-0000-0000-0000-000000000010")
_TEST_WORKSPACE_ID = uuid.UUID("00000000-0000-0000-0000-000000000011")
_TEST_MEMBER_ID = uuid.UUID("00000000-0000-0000-0000-000000000012")
_TEST_NOW = datetime.now(UTC)

_TEST_COMPANY = Company(
    id=_TEST_COMPANY_ID,
    name="Test Company",
    slug="test-company",
    status=CompanyStatus.ACTIVE.value,
    created_at=_TEST_NOW,
    updated_at=_TEST_NOW,
)
_TEST_WORKSPACE = Workspace(
    id=_TEST_WORKSPACE_ID,
    company_id=_TEST_COMPANY_ID,
    name="Default",
    slug="default",
    status=WorkspaceStatus.ACTIVE.value,
    created_at=_TEST_NOW,
    updated_at=_TEST_NOW,
)
_TEST_MEMBER = CompanyMember(
    id=_TEST_MEMBER_ID,
    company_id=_TEST_COMPANY_ID,
    user_id=DEV_BYPASS_USER_ID,
    role=CompanyMemberRole.ADMIN.value,
    status=CompanyMemberStatus.ACTIVE.value,
    created_at=_TEST_NOW,
    updated_at=_TEST_NOW,
)


@pytest.fixture(autouse=True)
def mock_tenancy_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    """Resolve tenant context without a live Postgres instance."""

    async def get_first_company(self: object) -> Company:
        return _TEST_COMPANY

    async def get_default_workspace_for_company(
        self: object,
        company_id: uuid.UUID,
    ) -> Workspace:
        return _TEST_WORKSPACE

    async def get_member(
        self: object,
        company_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> CompanyMember | None:
        if company_id == _TEST_COMPANY_ID and user_id == DEV_BYPASS_USER_ID:
            return _TEST_MEMBER
        return None

    async def get_active_memberships(
        self: object,
        user_id: uuid.UUID,
    ) -> list[CompanyMember]:
        if user_id == DEV_BYPASS_USER_ID:
            return [_TEST_MEMBER]
        return []

    async def get_workspace_by_id(
        self: object,
        workspace_id: uuid.UUID,
    ) -> Workspace | None:
        if workspace_id == _TEST_WORKSPACE_ID:
            return _TEST_WORKSPACE
        return None

    monkeypatch.setattr(
        "app.modules.tenancy.repository.TenancyRepository.get_first_company",
        get_first_company,
    )
    monkeypatch.setattr(
        "app.modules.tenancy.repository.TenancyRepository.get_default_workspace_for_company",
        get_default_workspace_for_company,
    )
    monkeypatch.setattr(
        "app.modules.tenancy.repository.TenancyRepository.get_member",
        get_member,
    )
    monkeypatch.setattr(
        "app.modules.tenancy.repository.TenancyRepository.get_active_memberships",
        get_active_memberships,
    )
    monkeypatch.setattr(
        "app.modules.tenancy.repository.TenancyRepository.get_workspace_by_id",
        get_workspace_by_id,
    )


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def disable_auth_for_unit_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Existing API tests assume open access unless auth is explicitly enabled."""
    monkeypatch.setenv("AUTH_ENABLED", "false")
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def mock_database_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default tests assume database is reachable without a live Postgres instance."""

    async def _connected() -> bool:
        return True

    monkeypatch.setattr(
        "app.api.v1.endpoints.health.check_database_connection",
        _connected,
    )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_db_unavailable(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock(return_value=False)
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", mock)
    return mock


@pytest.fixture
def mock_db_available(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock(return_value=True)
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", mock)
    return mock
