import uuid
from datetime import UTC, datetime

import pytest
from app.domain.enums import DataProductStatus, DataProductType, QualityStatus
from app.modules.data_products.schemas import DataProductCreate, DataProductRead, DataProductUpdate
from pydantic import ValidationError


def test_valid_create_payload() -> None:
    payload = DataProductCreate(
        name="Customer Revenue Dataset",
        description="Monthly revenue aggregation",
        type=DataProductType.DATASET,
        status=DataProductStatus.DRAFT,
    )
    assert payload.name == "Customer Revenue Dataset"
    assert payload.type == DataProductType.DATASET


def test_empty_name_rejected() -> None:
    with pytest.raises(ValidationError):
        DataProductCreate(name="")


def test_update_allows_partial_payload() -> None:
    payload = DataProductUpdate(status=DataProductStatus.ACTIVE)
    data = payload.model_dump(exclude_unset=True)
    assert data == {"status": DataProductStatus.ACTIVE}


def test_enum_values_accepted_in_create() -> None:
    payload = DataProductCreate(
        name="Executive KPI Dashboard",
        type=DataProductType.DASHBOARD,
        status=DataProductStatus.ACTIVE,
        quality_status=QualityStatus.GOOD,
    )
    assert payload.type == DataProductType.DASHBOARD
    assert payload.quality_status == QualityStatus.GOOD


def test_data_product_read_from_attributes() -> None:
    now = datetime.now(UTC)
    product_id = uuid.uuid4()
    payload = DataProductRead(
        id=product_id,
        name="API Gateway Metrics",
        description=None,
        type=DataProductType.API,
        status=DataProductStatus.ACTIVE,
        quality_status=QualityStatus.UNKNOWN,
        business_domain_id=None,
        business_owner_id=None,
        technical_owner_id=None,
        capability_id=None,
        team_id=None,
        refresh_frequency=None,
        source_systems=None,
        consumers=None,
        documentation_url=None,
        created_at=now,
        updated_at=now,
    )
    assert payload.id == product_id
