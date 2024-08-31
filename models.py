from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from fastapi import HTTPException

class Item(BaseModel):
    product_id: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)

class Product(BaseModel):
    product_id: str 
    name: str 
    description: str
    category: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(gt=-1)

class Cart(BaseModel):
    items: List[Item] = []

class DiscountCode(BaseModel):
    code: str
    discount_percentage: float = Field(default=0,gt=-1, lt=101)
    used: bool = Field(default=False)

class Order(BaseModel):
    id: str
    items: List[Item] = Field(...)
    total_amount: float
    discount_code: Optional[str] = None
    discounted_amount: Optional[float] = None

    @field_validator('items',mode="before")
    def price_must_be_positive(cls, value):
        if not value:
            raise HTTPException(status_code=422, detail='Cart cannot be empty')
        return value

    
