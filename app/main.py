from fastapi import FastAPI, HTTPException
from models import Item
from services import EcommerceService
from typing import Optional

app = FastAPI()
service = EcommerceService()


@app.get("/")
async def home():
    """
    ## Get status of the service.

    ## Returns:
        JSON: {"message": "Service is running."}
    """
    return {"message": "Service is running."}


@app.get("/products")
def get_products():
    """
    ## Get a list of all the products available.

    ## Returns:
        JSON: A list of products

    ## Example Response:

        [
            {
                "product_id": "1",
                "name": "Wireless Earbuds",
                "description": "Bluetooth 5.0 earbuds with noise cancellation and 24-hour battery life.",
                "category": "Electronics",
                "price": 59.99,
                "stock_quantity": 120
            },
            {
                "product_id": "2",
                "name": "4K LED Smart TV",
                "description": "55-inch Ultra HD TV with streaming apps and voice control.",
                "category": "Electronics",
                "price": 499.99,
                "stock_quantity": 45
            },
            ...
        ]
    """
    return service.get_products()


@app.get("/discount_codes")
def get_discount_codes():
    """
    ## Get a list of all the discount codes available.

    ## Returns:
        JSON: A list of discount codes.

    ## Example Response:

        [
            {
                "code": "8XYLS82O",
                "discount_percentage": 10,
                "used": false
            },
            {
                "code": "8BVERAM2",
                "discount_percentage": 10,
                "used": false
            },
            ...
        ]
    """
    return service.get_discount_codes()


@app.get("/cart")
def get_cart():
    """
    ## Get the list of items added to the cart.

    ## Returns:
        JSON: List of items in cart.

    ## Example Response:

        [
            {
                "product_id": "8",
                "price": 39.99,
                "quantity": 1
            },
            ...
        ]
    """
    return service.get_cart()


@app.post("/cart")
def add_to_cart(item: Item):
    """
     Add a single item to the cart.

    ## Args:
        item (Item):
        {
            "product_id": "8",
            "price": 39.99,
            "quantity": 1
        }

    ## Returns:
        JSON: {"message": "Item added to cart"}
    """
    service.add_item_to_cart(item)
    return {"message": "Item added to cart"}


@app.post("/checkout")
def checkout(discount_code: Optional[str] = None):
    """
    Checkout with all the items in the cart combined as a single order.

    ## Args:
        discount_code (Optional[str]): An optional discount code to be applied during checkout.

    ## Returns:
        JSON: A JSON  response containing the order details.

    ## Raises:
        HTTPException: If the checkout fails due to an invalid order or other issues.
        HTTPException: If the cart is empty.

    ## Example Response:

        {
            "id": "1",
            "items": [
                {
                "product_id": "8",
                "price": 39.99,
                "quantity": 1
                }
            ],
            "total_amount": 39.99,
            "discount_code": "NS27d78",
            "discounted_amount": 33.15
        }
    """
    order = service.checkout(discount_code)
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order")
    return order


@app.post("/admin/generate-discount")
def generate_discount(discount_percentage: float = 10):
    """
    ## Generate a new discount code with a specified discount percentage.

    ## Args:
        discount_percentage (float): The percentage discount for the generated code.
                                     Default is 10.

    ## Returns:
        JSON: {"message": "Discount code generated"}
    """
    service.generate_discount_code(discount_percentage=discount_percentage)
    return {"message": "Discount code generated"}


@app.get("/admin/orders-summary")
def get_orders_summary():
    """
    ## Get an aggregate summary of all orders.

    ## Returns:
        JSON: json object containing orders summary

    ## Example Response:

        {
            "total_items": 1,
            "total_amount": 39.99,
            "discount_codes": [],
            "total_discount_given": 0
        }
    """
    return service.get_order_summary()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
