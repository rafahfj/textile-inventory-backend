from pydantic import BaseModel
from datetime import date
from typing import Optional

class IncomingCreate(BaseModel):
    product_id: int
    qty: int
    date: date
    user_id: int
    note: Optional[str] = None

class IncomingRead(BaseModel):
    id: int
    product_id: int
    qty: int
    date: date
    user_id: int
    note: Optional[str]

    class Config:
        from_attributes = True
