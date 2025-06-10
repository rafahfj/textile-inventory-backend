from pydantic import BaseModel
from datetime import date
from typing import Optional

class OutgoingCreate(BaseModel):
    product_id: int
    qty: int
    date: date
    purpose: str
    user_id: int
    note: Optional[str] = None

class OutgoingRead(BaseModel):
    id: int
    product_id: int
    qty: int
    date: date
    purpose: str
    user_id: int
    note: Optional[str]

    class Config:
        orm_mode = True
