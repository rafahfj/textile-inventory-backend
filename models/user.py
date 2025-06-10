from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str  # hashed di backend sebelum disimpan
    role: Literal['admin', 'staff', 'viewer'] = 'viewer'

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
