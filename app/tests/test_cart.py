import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_item_to_cart():
    item_data = {"product_id": "8", "price": 39.99, "quantity": 1}

    response = client.post("/cart", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to cart"}
