"""Integration tests for dashboard endpoints (requires live PostgreSQL)."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.seed.seed import seed_database


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dashboard_endpoints_return_seeded_data() -> None:
    await seed_database()

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        summary_response = await client.get("/api/v1/dashboard/summary")
        assert summary_response.status_code == 200
        summary = summary_response.json()
        assert summary["data_products_total"] >= 6
        assert summary["work_items_total"] >= 10
        assert summary["people_total"] >= 10

        products_response = await client.get("/api/v1/dashboard/recent-data-products")
        assert products_response.status_code == 200
        assert len(products_response.json()) >= 1

        work_response = await client.get("/api/v1/dashboard/high-priority-work-items")
        assert work_response.status_code == 200
        assert len(work_response.json()) >= 1

        health_response = await client.get("/api/v1/dashboard/project-health")
        assert health_response.status_code == 200
        assert len(health_response.json()) >= 1

        workload_response = await client.get("/api/v1/dashboard/capability-workload")
        assert workload_response.status_code == 200
        assert len(workload_response.json()) >= 1

        gaps_response = await client.get("/api/v1/dashboard/ownership-gaps")
        assert gaps_response.status_code == 200
        assert isinstance(gaps_response.json(), list)
