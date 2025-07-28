from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Backend"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_users_endpoint():
    response = client.get("/api/v1/users/")
    # This should return 401 because authentication is required
    assert response.status_code == 401

def test_items_endpoint():
    response = client.get("/api/v1/items/")
    # This should return 401 because authentication is required
    assert response.status_code == 401 