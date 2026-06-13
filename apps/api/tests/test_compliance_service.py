import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import ComplianceSubjectType, EvidenceStatus
from app.modules.compliance.errors import ComplianceEvidenceConflictError, PolicyNotFoundError
from app.modules.compliance.schemas import ComplianceEvidenceCreate, PolicyCreate
from app.modules.compliance.service import ComplianceService


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_file_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_activity() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def compliance_service(
    mock_repository: AsyncMock,
    mock_file_repository: AsyncMock,
    mock_activity: AsyncMock,
    mock_session: AsyncMock,
) -> ComplianceService:
    return ComplianceService(
        mock_repository,
        mock_file_repository,
        mock_activity,
        mock_session,
    )


@pytest.mark.asyncio
async def test_create_policy(
    compliance_service: ComplianceService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_policy_by_name.return_value = None
    mock_policy = MagicMock()
    mock_policy.id = uuid.uuid4()
    mock_policy.name = "Test Policy"
    mock_policy.description = None
    mock_policy.status = "active"
    mock_policy.owner_id = None
    mock_policy.effective_from = None
    mock_policy.effective_to = None
    mock_policy.version = "v1.0"
    mock_policy.created_at = MagicMock()
    mock_policy.updated_at = MagicMock()
    mock_repository.create_policy.return_value = mock_policy

    result = await compliance_service.create_policy(
        PolicyCreate(name="Test Policy", status="active", version="v1.0")
    )
    assert result.name == "Test Policy"


@pytest.mark.asyncio
async def test_get_overview(
    compliance_service: ComplianceService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_overview.return_value = {
        "policies_total": 2,
        "policies_active": 2,
        "rules_total": 5,
        "active_rules": 5,
        "controls_total": 3,
        "active_controls": 3,
        "checks_total": 4,
        "checks_open": 2,
        "checks_compliant": 2,
        "checks_non_compliant": 0,
        "checks_overdue": 0,
        "evidence_missing": 1,
    }
    overview = await compliance_service.get_overview()
    assert overview.policies_total == 2
    assert overview.checks_total == 4


@pytest.mark.asyncio
async def test_add_evidence_raises_conflict(
    compliance_service: ComplianceService,
    mock_repository: AsyncMock,
    mock_file_repository: AsyncMock,
) -> None:
    check_id = uuid.uuid4()
    file_id = uuid.uuid4()
    mock_check = MagicMock()
    mock_check.subject_type = ComplianceSubjectType.DATA_PRODUCT.value
    mock_check.subject_id = uuid.uuid4()
    mock_check.title = "Ownership check"
    mock_repository.get_check_by_id.return_value = mock_check
    mock_file_repository.get_file_by_id.return_value = MagicMock(name="Spec")
    mock_repository.get_duplicate_evidence.return_value = MagicMock()

    with pytest.raises(ComplianceEvidenceConflictError):
        await compliance_service.add_evidence(
            check_id,
            ComplianceEvidenceCreate(file_id=file_id, status=EvidenceStatus.SUBMITTED),
        )


@pytest.mark.asyncio
async def test_delete_policy_raises_when_missing(
    compliance_service: ComplianceService,
    mock_repository: AsyncMock,
) -> None:
    mock_repository.get_policy_by_id.return_value = None
    with pytest.raises(PolicyNotFoundError):
        await compliance_service.delete_policy(uuid.uuid4())
