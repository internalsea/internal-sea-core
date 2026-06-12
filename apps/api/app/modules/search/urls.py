"""Frontend URL builders for search results."""

from __future__ import annotations

import uuid

from app.domain.enums import ProjectType
from app.modules.search.schemas import SearchResultType


def build_data_product_url(entity_id: uuid.UUID) -> str:
    return f"/data-products/{entity_id}"


def build_work_item_url(entity_id: uuid.UUID) -> str:
    return f"/work-items/{entity_id}"


def build_project_url(entity_id: uuid.UUID, project_type: ProjectType) -> str:
    if project_type == ProjectType.INTERNAL_PROJECT:
        return f"/internal-projects/{entity_id}"
    return f"/projects/{entity_id}"


def build_person_url(entity_id: uuid.UUID) -> str:
    return f"/people/{entity_id}"


def build_team_url(entity_id: uuid.UUID) -> str:
    return f"/teams/{entity_id}"


def build_capability_url(entity_id: uuid.UUID) -> str:
    return f"/capabilities/{entity_id}"


def build_file_url(entity_id: uuid.UUID) -> str:
    return f"/files/{entity_id}"


def build_policy_url(entity_id: uuid.UUID) -> str:
    return f"/compliance/policies/{entity_id}"


def build_compliance_check_url(entity_id: uuid.UUID) -> str:
    return f"/compliance/checks/{entity_id}"


def build_automation_trigger_url(entity_id: uuid.UUID) -> str:
    return f"/automation/triggers/{entity_id}"


def build_notification_template_url(entity_id: uuid.UUID) -> str:
    return f"/notifications/templates/{entity_id}"


def build_notification_message_url(entity_id: uuid.UUID) -> str:
    return f"/notifications/messages/{entity_id}"


def project_search_result_type(project_type: ProjectType) -> SearchResultType:
    if project_type == ProjectType.INTERNAL_PROJECT:
        return SearchResultType.INTERNAL_PROJECT
    return SearchResultType.PROJECT
