import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import AutomationTargetType, ProjectType
from app.models.catalog import DataProduct
from app.models.compliance import ComplianceCheck
from app.models.people import Capability, Team
from app.models.projects import Project
from app.models.work import WorkItem
from app.modules.automation.errors import (
    AutomationTargetNotFoundError,
    UnsupportedAutomationTargetTypeError,
)

SUPPORTED_AUTOMATION_TARGET_TYPES: set[AutomationTargetType] = {
    AutomationTargetType.DATA_PRODUCT,
    AutomationTargetType.PROJECT,
    AutomationTargetType.INTERNAL_PROJECT,
    AutomationTargetType.COMPLIANCE_CHECK,
    AutomationTargetType.TEAM,
    AutomationTargetType.CAPABILITY,
    AutomationTargetType.WORK_ITEM,
}


async def validate_automation_target_exists(
    session: AsyncSession,
    target_type: AutomationTargetType,
    target_id: uuid.UUID,
) -> bool:
    if target_type not in SUPPORTED_AUTOMATION_TARGET_TYPES:
        raise UnsupportedAutomationTargetTypeError(target_type.value)

    exists = False
    if target_type == AutomationTargetType.DATA_PRODUCT:
        exists = await session.get(DataProduct, target_id) is not None
    elif target_type == AutomationTargetType.WORK_ITEM:
        exists = await session.get(WorkItem, target_id) is not None
    elif target_type == AutomationTargetType.TEAM:
        exists = await session.get(Team, target_id) is not None
    elif target_type == AutomationTargetType.CAPABILITY:
        exists = await session.get(Capability, target_id) is not None
    elif target_type == AutomationTargetType.COMPLIANCE_CHECK:
        exists = await session.get(ComplianceCheck, target_id) is not None
    elif target_type == AutomationTargetType.PROJECT:
        project = await session.get(Project, target_id)
        exists = project is not None and project.project_type != ProjectType.INTERNAL_PROJECT
    elif target_type == AutomationTargetType.INTERNAL_PROJECT:
        project = await session.get(Project, target_id)
        exists = project is not None and project.project_type == ProjectType.INTERNAL_PROJECT

    if not exists:
        raise AutomationTargetNotFoundError(target_type.value, target_id)
    return True


async def ensure_automation_target_supported(
    target_type: AutomationTargetType,
) -> None:
    if target_type not in SUPPORTED_AUTOMATION_TARGET_TYPES:
        raise UnsupportedAutomationTargetTypeError(target_type.value)
