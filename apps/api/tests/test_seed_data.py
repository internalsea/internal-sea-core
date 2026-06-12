"""Unit tests for seed data definitions (no live database required)."""

from __future__ import annotations

import re

import pytest

from app.domain.enums import (
    DataProductStatus,
    DataProductType,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.seed import seed_data
from app.seed.seed_data import (
    BUSINESS_DOMAINS,
    CAPABILITIES,
    DATA_PRODUCTS,
    PEOPLE,
    SEED_DATASETS,
    TEAMS,
    WORK_ITEMS,
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def test_seed_data_imports() -> None:
    assert seed_data.CAPABILITIES is CAPABILITIES
    assert seed_data.SEED_DATASETS is SEED_DATASETS


def test_seed_datasets_have_required_keys() -> None:
    required = {
        "capabilities",
        "teams",
        "people",
        "business_domains",
        "client_projects",
        "internal_projects",
        "data_products",
        "work_items",
    }
    assert required.issubset(SEED_DATASETS.keys())
    for key in required:
        assert isinstance(SEED_DATASETS[key], list)
        assert len(SEED_DATASETS[key]) > 0


def test_capabilities_not_empty() -> None:
    assert len(CAPABILITIES) >= 8
    for item in CAPABILITIES:
        assert item["name"].strip()
        assert item["description"].strip()


def test_teams_not_empty() -> None:
    assert len(TEAMS) >= 5
    for item in TEAMS:
        assert item["name"].strip()


def test_people_have_valid_emails() -> None:
    for person in PEOPLE:
        assert EMAIL_PATTERN.match(person["email"])
        assert person["full_name"].strip()
        assert person["team"].strip()
        assert person["capability"].strip()


@pytest.mark.parametrize(
    "field",
    ["type", "status", "quality_status", "name"],
)
def test_data_products_have_required_fields(field: str) -> None:
    for product in DATA_PRODUCTS:
        assert field in product
        assert str(product[field]).strip()


def test_data_products_have_valid_enum_values() -> None:
    for product in DATA_PRODUCTS:
        assert DataProductType(product["type"])
        assert DataProductStatus(product["status"])


@pytest.mark.parametrize(
    "field",
    ["title", "type", "status", "priority"],
)
def test_work_items_have_required_fields(field: str) -> None:
    for item in WORK_ITEMS:
        assert field in item
        assert str(item[field]).strip()


def test_work_items_have_valid_enum_values() -> None:
    for item in WORK_ITEMS:
        assert WorkItemType(item["type"])
        assert WorkItemStatus(item["status"])
        assert WorkItemPriority(item["priority"])


def test_capability_names_unique() -> None:
    names = [item["name"] for item in CAPABILITIES]
    assert len(names) == len(set(names))


def test_team_names_unique() -> None:
    names = [item["name"] for item in TEAMS]
    assert len(names) == len(set(names))


def test_people_emails_unique() -> None:
    emails = [item["email"] for item in PEOPLE]
    assert len(emails) == len(set(emails))


def test_business_domain_names_unique() -> None:
    names = [item["name"] for item in BUSINESS_DOMAINS]
    assert len(names) == len(set(names))


def test_project_names_unique() -> None:
    names = [item["name"] for item in SEED_DATASETS["client_projects"]]
    names += [item["name"] for item in SEED_DATASETS["internal_projects"]]
    assert len(names) == len(set(names))


def test_data_product_names_unique() -> None:
    names = [item["name"] for item in DATA_PRODUCTS]
    assert len(names) == len(set(names))


def test_work_item_natural_keys_unique() -> None:
    keys = [(item["title"], item["type"]) for item in WORK_ITEMS]
    assert len(keys) == len(set(keys))
