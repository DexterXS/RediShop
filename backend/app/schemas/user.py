from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    birth_date: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    birth_date: Optional[datetime]
    address: Optional[str]

class UserResponse(BaseModel):
    email: EmailStr
    name: str
    birth_date: datetime
    address: Optional[str] = None
    class Config:
        orm_mode = True
