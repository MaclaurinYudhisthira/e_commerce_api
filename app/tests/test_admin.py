import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)


def test_generate_discount_code():
    # Generate a discount code via the admin API
    response = client.post("/admin/generate-discount")
    assert response.status_code == 200
    assert response.json() == {"message": "Discount code generated"}


def test_get_order_summary():
    # Call the admin API to get a summary of orders
    response = client.get("/admin/orders-summary")
    assert response.status_code == 200

    # Validate the structure of the response
    response_data = response.json()
    assert "total_items" in response_data
    assert "total_amount" in response_data
    assert "discount_codes" in response_data
    assert "total_discount_given" in response_data
