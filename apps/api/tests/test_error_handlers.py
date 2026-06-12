from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.core.errors import NotFoundError
from app.main import create_app
from app.modules.capabilities.router import get_capability_service
from unittest.mock import AsyncMock


def test_validation_error_returns_standard_shape(client: TestClient) -> None:
    response = client.post("/api/v1/auth/login", json={"email": "not-an-email"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert body["message"] == "Request validation failed"
    assert body["detail"] == body["message"]
    assert "request_id" in body
    assert response.headers.get("X-Request-ID")


def test_not_found_error_returns_standard_shape() -> None:
    app = create_app()
    mock_service = AsyncMock()
    mock_service.get_capability.side_effect = NotFoundError("Capability missing")
    app.dependency_overrides[get_capability_service] = lambda: mock_service

    with TestClient(app) as client:
        response = client.get("/api/v1/capabilities/00000000-0000-0000-0000-000000000099")
        assert response.status_code == 404
        body = response.json()
        assert body["error"] == "not_found"
        assert body["message"] == "Capability missing"
        assert body["request_id"]


def test_http_exception_returns_standard_shape() -> None:
    app = create_app()

    @app.get("/test-http-error")
    def _raise() -> None:
        raise HTTPException(status_code=403, detail="Forbidden action")

    with TestClient(app) as test_client:
        response = test_client.get("/test-http-error")
        assert response.status_code == 403
        body = response.json()
        assert body["error"] == "forbidden"
        assert body["message"] == "Forbidden action"
