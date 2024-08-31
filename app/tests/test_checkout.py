import pytest
from fastapi.testclient import TestClient
from main import app
from services import EcommerceService
from models import Cart

client = TestClient(app)

def test_checkout_without_discount():
    # Add items to cart first
    item_data = {
        "product_id": "8",
        "price": 39.99,
        "quantity": 1
    }
    client.post("/cart", json=item_data)

    # Checkout without a discount code
    response = client.post("/checkout")
    assert response.status_code == 200

    # Check the response contains the correct order details
    response_data = response.json()
    assert response_data["discounted_amount"] is None


def test_checkout_with_empty_cart():
    # Checkout without a discount code
    response = client.post("/checkout")
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"] == "Cart cannot be empty"


def test_checkout_with_invalid_discount():
    # Add item to cart
    item_data = {
        "product_id": "8",
        "price": 39.99,
        "quantity": 1
    }
    client.post("/cart", json=item_data)

    # Checkout with an invalid discount code
    response = client.post("/checkout?discount_code=INVALIDCODE")
    assert response.status_code == 200  # Checkout still goes through
    assert response.json()["total_amount"] == 39.99  # No discount applied


def test_checkout_with_valid_discount():
    # Add item to cart again
    item_data = {
        "product_id": "8",
        "price": 39.99,
        "quantity": 1
    }
    client.post("/cart", json=item_data)
    
    client.post(f"/admin/generate-discount?discount_percentage={15}")
    response = client.get("/discount_codes")
    discount_code = response.json()[-1]["code"]
    
    # Checkout with valid discount code
    response = client.post(f"/checkout?discount_code={discount_code}")

    assert response.status_code == 200

    # Check the response contains the discounted order details
    response_data = response.json()
    assert response_data["total_amount"] == 39.99
    assert response_data["discounted_amount"] == 33.9915  # 15% discount applied