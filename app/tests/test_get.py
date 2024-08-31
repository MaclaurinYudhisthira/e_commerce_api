import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Service is running."}


def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200


def test_get_discount_codes():
    response = client.get("/discount_codes")
    assert response.status_code == 200


def test_get_cart():
    response = client.get("/cart")
    assert response.status_code == 200
