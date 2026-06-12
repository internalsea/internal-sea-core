"""Tests for tenancy API registration and auth."""

from app.main import app


def test_tenancy_endpoints_in_openapi() -> None:
    paths = app.openapi()["paths"]
    assert "/api/v1/tenancy/current" in paths
    assert "/api/v1/tenancy/onboarding/first-user" in paths
    assert "/api/v1/tenancy/companies" in paths
    assert "/api/v1/tenancy/actionable-insights" not in paths
