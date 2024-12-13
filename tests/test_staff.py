from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_staff_member():
    response = client.post(
        "/api/v1/staff/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "role": "waiter"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["role"] == "waiter"

def test_get_staff_members():
    response = client.get("/api/v1/staff/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 