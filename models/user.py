from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    fullname: str
    email: str
    password: str  # hashed di backend sebelum disimpan
    role: Literal['admin', 'staff', 'viewer'] = 'viewer'

class UserLogin(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    fullname: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
