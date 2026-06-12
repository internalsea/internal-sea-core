"""Integration tests for seed runner (requires live PostgreSQL)."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from app.db.session import get_sessionmaker
from app.models.catalog import DataProduct
from app.models.people import Capability, Person, Team
from app.models.projects import Project
from app.domain.enums import WorkItemType
from app.models.work import WorkItem
from app.seed.seed import count_seeded_entities, seed_database
from app.seed.seed_data import (
    CAPABILITIES,
    DATA_PRODUCTS,
    PEOPLE,
    TEAMS,
    WORK_ITEMS,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_database_is_idempotent() -> None:
    await seed_database()
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        counts_after_first = await count_seeded_entities(session)

    await seed_database()
    async with sessionmaker() as session:
        counts_after_second = await count_seeded_entities(session)

    assert counts_after_first == counts_after_second
    assert counts_after_first["capabilities"] >= len(CAPABILITIES)
    assert counts_after_first["teams"] >= len(TEAMS)
    assert counts_after_first["people"] >= len(PEOPLE)
    assert counts_after_first["data_products"] >= len(DATA_PRODUCTS)
    assert counts_after_first["work_items"] >= len(WORK_ITEMS)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_database_no_duplicate_capabilities() -> None:
    await seed_database()
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        for item in CAPABILITIES:
            result = await session.execute(
                select(Capability).where(Capability.name == item["name"])
            )
            matches = result.scalars().all()
            assert len(matches) == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_database_no_duplicate_work_items() -> None:
    await seed_database()
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        for item in WORK_ITEMS:
            result = await session.execute(
                select(WorkItem).where(
                    WorkItem.title == item["title"],
                    WorkItem.type == WorkItemType(item["type"]),
                )
            )
            matches = result.scalars().all()
            assert len(matches) == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_database_relationships_linked() -> None:
    await seed_database()
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        person_result = await session.execute(
            select(Person).where(Person.email == "maya.singh@example.com")
        )
        person = person_result.scalar_one()
        assert person.team_id is not None
        assert person.capability_id is not None

        team_result = await session.execute(select(Team).where(Team.id == person.team_id))
        team = team_result.scalar_one()
        assert team.name == "Data Products Team"

        project_result = await session.execute(
            select(Project).where(Project.name == "Internal Sea MVP")
        )
        project = project_result.scalar_one()
        assert project.owner_id is not None

        product_result = await session.execute(
            select(DataProduct).where(DataProduct.name == "Executive Sales Dashboard")
        )
        product = product_result.scalar_one()
        assert product.business_domain_id is not None
        assert product.business_owner_id is not None
