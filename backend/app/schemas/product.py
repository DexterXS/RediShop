from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    shipping_cost: float
    images: Optional[List[str]] = []

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    shipping_cost: Optional[float]
    images: Optional[List[str]] = []

class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    shipping_cost: float
    images: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
