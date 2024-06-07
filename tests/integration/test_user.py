import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user():
    response = client.get("/user/me", headers={"Authorization": "Bearer <token>"})
    assert response.status_code == 200
    assert "email" in response.json()

def test_update_user():
    response = client.put("/user/me", headers={"Authorization": "Bearer <token>"}, json={
        "name": "Updated User",
        "birth_date": "1999-01-01",
        "address": "New Address"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated User"
