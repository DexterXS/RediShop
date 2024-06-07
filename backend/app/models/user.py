from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    hashed_password: str
    name: str
    birth_date: datetime
    address: Optional[str] = None
    is_deleted: bool = False
    products: List[str] = []
