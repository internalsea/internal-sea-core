from fastapi.testclient import TestClient

from app.main import create_app


def test_request_id_header_is_generated() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        request_id = response.headers.get("X-Request-ID")
        assert request_id
        assert len(request_id) >= 8


def test_request_id_header_is_echoed() -> None:
    app = create_app()
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/health/live",
            headers={"X-Request-ID": "test-request-123"},
        )
        assert response.headers.get("X-Request-ID") == "test-request-123"
