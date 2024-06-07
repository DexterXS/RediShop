import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product",
        "price": 10.0,
        "shipping_cost": 2.0,
        "images": []
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
