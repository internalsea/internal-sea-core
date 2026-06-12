"""Tenant scoping helpers for repositories and services."""

from __future__ import annotations

import uuid
from typing import Any

from app.core.errors import NotFoundError


def apply_company_filter(query: Any, model: type, company_id: uuid.UUID) -> Any:
    if hasattr(model, "company_id"):
        return query.where(model.company_id == company_id)
    return query


def merge_tenant_fields(
    data: dict,
    *,
    company_id: uuid.UUID,
    workspace_id: uuid.UUID | None = None,
) -> dict:
    merged = dict(data)
    merged["company_id"] = company_id
    if workspace_id is not None:
        merged["workspace_id"] = workspace_id
    return merged


def ensure_company_access(entity: Any, company_id: uuid.UUID, *, label: str = "Resource") -> None:
    entity_company_id = getattr(entity, "company_id", None)
    if entity_company_id is not None and entity_company_id != company_id:
        raise NotFoundError(f"{label} not found")
