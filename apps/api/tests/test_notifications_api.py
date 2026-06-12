from fastapi.testclient import TestClient

from app.main import app


def test_openapi_contains_notification_endpoints() -> None:
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/notifications/overview" in paths
    assert "/api/v1/notifications/channels" in paths
    assert "/api/v1/notifications/templates" in paths
    assert "/api/v1/notifications/messages" in paths
    assert "/api/v1/notifications/messages/{message_id}/send" in paths
