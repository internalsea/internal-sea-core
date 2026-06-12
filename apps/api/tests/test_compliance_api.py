import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.enums import ComplianceCheckType, ComplianceStatus, ComplianceSubjectType
from app.main import create_app
from app.modules.compliance.errors import ComplianceEvidenceConflictError
from app.modules.compliance.router import get_compliance_service
from app.modules.compliance.schemas import (
    ComplianceCheckListItem,
    ComplianceCheckListResponse,
    ComplianceCheckRead,
    ComplianceOverview,
    PolicyListItem,
    PolicyListResponse,
    PolicyRead,
)


@pytest.fixture
def mock_compliance_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def api_client(mock_compliance_service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_compliance_service] = lambda: mock_compliance_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_openapi_includes_compliance_paths(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/compliance/overview" in paths
    assert "/api/v1/compliance/policies" in paths
    assert "/api/v1/compliance/checks" in paths
    assert "/api/v1/compliance/entity/{subject_type}/{subject_id}" in paths


def test_get_compliance_overview(api_client: TestClient, mock_compliance_service: AsyncMock) -> None:
    mock_compliance_service.get_overview.return_value = ComplianceOverview(
        policies_total=2,
        checks_total=4,
        checks_open=1,
    )
    response = api_client.get("/api/v1/compliance/overview")
    assert response.status_code == 200
    assert response.json()["policies_total"] == 2


def test_list_policies(api_client: TestClient, mock_compliance_service: AsyncMock) -> None:
    item = PolicyListItem(
        id=uuid.uuid4(),
        name="Data Product Governance Policy",
        status="active",
        owner_id=None,
        effective_from=None,
        effective_to=None,
        version="v1.0",
        updated_at=datetime.now(timezone.utc),
    )
    mock_compliance_service.list_policies.return_value = PolicyListResponse(
        items=[item],
        total=1,
        page=1,
        page_size=20,
        pages=1,
    )
    response = api_client.get("/api/v1/compliance/policies")
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_create_policy(api_client: TestClient, mock_compliance_service: AsyncMock) -> None:
    policy_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    mock_compliance_service.create_policy.return_value = PolicyRead(
        id=policy_id,
        name="Data Product Governance Policy",
        description="Minimum requirements",
        status="active",
        owner_id=None,
        effective_from=None,
        effective_to=None,
        version="v1.0",
        created_at=now,
        updated_at=now,
    )
    response = api_client.post(
        "/api/v1/compliance/policies",
        json={
            "name": "Data Product Governance Policy",
            "status": "active",
            "version": "v1.0",
        },
    )
    assert response.status_code == 201


def test_add_evidence_conflict(api_client: TestClient, mock_compliance_service: AsyncMock) -> None:
    check_id = uuid.uuid4()
    mock_compliance_service.add_evidence.side_effect = ComplianceEvidenceConflictError()
    response = api_client.post(
        f"/api/v1/compliance/checks/{check_id}/evidence",
        json={"file_id": str(uuid.uuid4())},
    )
    assert response.status_code == 409


def test_list_checks(api_client: TestClient, mock_compliance_service: AsyncMock) -> None:
    item = ComplianceCheckListItem(
        id=uuid.uuid4(),
        subject_type=ComplianceSubjectType.DATA_PRODUCT,
        subject_id=uuid.uuid4(),
        title="Ownership confirmed",
        status=ComplianceStatus.COMPLIANT,
        check_type=ComplianceCheckType.MANUAL,
        owner_id=None,
        due_date=None,
        completed_at=None,
        next_check_at=None,
        rule_id=None,
        control_id=None,
        updated_at=datetime.now(timezone.utc),
    )
    mock_compliance_service.list_checks.return_value = ComplianceCheckListResponse(
        items=[item],
        total=1,
        page=1,
        page_size=20,
        pages=1,
    )
    response = api_client.get("/api/v1/compliance/checks")
    assert response.status_code == 200
    assert response.json()["items"][0]["status"] == "compliant"
