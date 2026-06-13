import uuid

import pytest
from app.domain.enums import FileAssetType, FileEntityType, FileSensitivity
from app.modules.files.schemas import FileAssetCreate, FileAttachmentCreate
from pydantic import ValidationError


def test_file_asset_create_accepts_valid_external_url() -> None:
    payload = FileAssetCreate(
        name="Finance KPI Definitions",
        file_type=FileAssetType.EVIDENCE,
        sensitivity=FileSensitivity.CONFIDENTIAL,
        external_url="https://example.com/docs/finance-kpi-definitions",
        version="v1.0",
    )
    assert payload.external_url == "https://example.com/docs/finance-kpi-definitions"


def test_file_asset_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        FileAssetCreate(name="")


def test_file_asset_create_rejects_negative_file_size() -> None:
    with pytest.raises(ValidationError):
        FileAssetCreate(name="Test", file_size_bytes=-1)


def test_file_attachment_create_accepts_valid_payload() -> None:
    payload = FileAttachmentCreate(
        file_id=uuid.uuid4(),
        entity_type=FileEntityType.DATA_PRODUCT,
        entity_id=uuid.uuid4(),
        purpose="Certified KPI evidence",
        is_evidence=True,
        evidence_type="kpi_certification",
    )
    assert payload.is_evidence is True
    assert payload.evidence_type == "kpi_certification"
