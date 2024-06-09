from pydantic import BaseModel
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float

    class Config:
        from_attributes = True
