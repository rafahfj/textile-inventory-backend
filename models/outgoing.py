from pydantic import BaseModel
from datetime import date
from typing import Optional

class OutgoingCreate(BaseModel):
    product_id: int
    qty: int
    date: date
    note: str
    user_id: int
    note: Optional[str] = None

class OutgoingRead(BaseModel):
    id: int
    product_id: int
    qty: int
    date: date
    purpose: str    
    note: str
    user_id: int
    note: Optional[str]

    class Config:
        from_attributes = True
