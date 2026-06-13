import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.domain.enums import AutomationTargetType
from app.modules.automation.errors import (
    AutomationTargetNotFoundError,
)
from app.modules.automation.validators import (
    SUPPORTED_AUTOMATION_TARGET_TYPES,
    validate_automation_target_exists,
)


@pytest.mark.asyncio
async def test_data_product_not_found_raises() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    target_id = uuid.uuid4()
    with pytest.raises(AutomationTargetNotFoundError):
        await validate_automation_target_exists(
            session,
            AutomationTargetType.DATA_PRODUCT,
            target_id,
        )


@pytest.mark.asyncio
async def test_supported_target_types_include_data_product() -> None:
    assert AutomationTargetType.DATA_PRODUCT in SUPPORTED_AUTOMATION_TARGET_TYPES


@pytest.mark.asyncio
async def test_data_product_exists_returns_true() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=MagicMock())
    result = await validate_automation_target_exists(
        session,
        AutomationTargetType.DATA_PRODUCT,
        uuid.uuid4(),
    )
    assert result is True
