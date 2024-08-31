from fastapi import FastAPI, HTTPException
from models import Item
from services import EcommerceService
from typing import Optional

app = FastAPI()
service = EcommerceService()

@app.get("/")
async def home():
    return {"message": "Service is running."}

@app.get("/products")
def get_products():
    return service.get_products()

@app.get("/discount_codes")
def get_discount_codes():
    return service.get_discount_codes()

@app.get("/cart")
def get_cart():
    return service.get_cart()

@app.post("/cart/add")
def add_to_cart(item: Item):
    service.add_item_to_cart(item)
    return {"message": "Item added to cart"}

@app.post("/checkout")
def checkout(discount_code: Optional[str] = None):
    order = service.checkout(discount_code)
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order")
    return order

@app.post("/admin/generate-discount")
def generate_discount(discount_percentage:float=10):
    service.generate_discount_code(discount_percentage=discount_percentage)
    return {"message": "Discount code generated"}

@app.get("/admin/orders-summary")
def get_orders_summary():
    return service.get_order_summary()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)