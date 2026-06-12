"""Integration tests for global search (requires live PostgreSQL)."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.seed.seed import seed_database


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_finds_seeded_entities() -> None:
    await seed_database()

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        sales_response = await client.get("/api/v1/search", params={"q": "sales"})
        assert sales_response.status_code == 200
        sales_items = sales_response.json()["items"]
        assert any(item["title"] == "Executive Sales Dashboard" for item in sales_items)

        project_response = await client.get("/api/v1/search", params={"q": "Internal Sea"})
        assert project_response.status_code == 200
        project_items = project_response.json()["items"]
        assert any(item["title"] == "Internal Sea MVP" for item in project_items)

        person_response = await client.get("/api/v1/search", params={"q": "Nikita"})
        assert person_response.status_code == 200
        person_items = person_response.json()["items"]
        assert any(item["type"] == "person" for item in person_items)
