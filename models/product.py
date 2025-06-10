from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    type: str
    color: str
    unit: str
    price: float
    min_stock: int
    current_stock: int
    supplier_id: int

class ProductRead(BaseModel):
    id: int
    name: str
    type: str
    color: str
    unit: str
    price: float
    min_stock: int
    current_stock: int
    supplier_id: int
    created_at: datetime

    class Config:
        orm_mode = True
