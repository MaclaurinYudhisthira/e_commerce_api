import random
import string
from typing import Optional
from models import Cart, Order, DiscountCode
from constants import sample_products

class EcommerceService:
    def __init__(self):
        self.cart = Cart()
        self.orders = []
        self.discount_codes = []
        self.nth_order = 5  # Every 5th order gets a discount code
        self.products=sample_products
        self.order_count=0

    def get_products(self):
        return self.products
    
    def get_discount_codes(self):
        return self.discount_codes

    def add_item_to_cart(self, item):
        self.cart.items.append(item)

    def get_cart(self):
        return self.cart.items

    def checkout(self, discount_code: Optional[str] = None):
        total_amount = sum(item.price * item.quantity for item in self.cart.items)
        discount = 0
        discounted_amount = None
        
        # check for discount code applied by customer
        if discount_code:
            discount = self.validate_discount_code(discount_code)
            discounted_amount = total_amount * ((100 - discount) / 100)
        order = Order(id=str(self.order_count + 1), items=self.cart.items, total_amount=total_amount, discount_code=discount_code,discounted_amount=discounted_amount)

        self.orders.append(order)
        self.order_count+=1
        self.cart = Cart()  # Clear the cart after checkout
        
        # Generate discount code if nth order
        if self.order_count % self.nth_order == 0:
            self.generate_discount_code(discount_percentage=10)

        return order

    def validate_discount_code(self, code: str) -> float:
        for discount in self.discount_codes:
            if discount.code == code and not discount.used:
                discount.used = True
                return discount.discount_percentage
        return 0  # Invalid or already used code

    def generate_discount_code(self, discount_percentage: float):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        discount = DiscountCode(code=code, discount_percentage=discount_percentage)
        self.discount_codes.append(discount)
        return code

    def get_order_summary(self):
        return {
            "total_items": sum(len(order.items) for order in self.orders),
            "total_amount": sum(order.discounted_amount or order.total_amount for order in self.orders),
            "discount_codes": [order.discount_code for order in self.orders if order.discount_code],
            "total_discount_given": sum(order.total_amount - (order.discounted_amount or order.total_amount) for order in self.orders)
        }
