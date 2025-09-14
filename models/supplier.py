from pydantic import BaseModel
from datetime import datetime

class SupplierCreate(BaseModel):
    name: str
    contact: str
    address: str

class SupplierRead(BaseModel):
    id: int
    name: str
    contact: str
    address: str
    created_at: datetime

    class Config:
        from_attributes = True
