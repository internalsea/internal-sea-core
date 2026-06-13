from fastapi.testclient import TestClient

EXPECTED_TAGS = {
    "Health",
    "Auth",
    "Dashboard",
    "Search",
    "Data Products",
    "Work",
    "Projects",
    "Internal Projects",
    "People",
    "Teams",
    "Capabilities",
    "Comments",
    "Activity",
    "Relationships",
    "Files",
    "Compliance",
    "Automation",
    "Performance",
}


def test_openapi_includes_core_module_paths(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    spec = response.json()
    paths = spec["paths"]

    expected_paths = [
        "/api/v1/health",
        "/api/v1/auth/login",
        "/api/v1/dashboard/summary",
        "/api/v1/search",
        "/api/v1/data-products",
        "/api/v1/work-items",
        "/api/v1/projects",
        "/api/v1/internal-projects",
        "/api/v1/people",
        "/api/v1/teams",
        "/api/v1/capabilities",
        "/api/v1/compliance/overview",
        "/api/v1/automation/overview",
        "/api/v1/performance/overview",
    ]
    for path in expected_paths:
        assert path in paths, f"Missing OpenAPI path: {path}"

    tags: set[str] = set()
    for path_item in spec["paths"].values():
        for operation in path_item.values():
            if isinstance(operation, dict) and "tags" in operation:
                tags.update(operation["tags"])
    assert EXPECTED_TAGS.issubset(tags)
