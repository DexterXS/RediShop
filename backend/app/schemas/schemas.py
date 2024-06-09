from pydantic import BaseModel, EmailStr, validator
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    birth_date: str
    address: str

    @validator('first_name', 'last_name')
    def name_must_be_alphabetic(cls, v):
        if not v.isalpha():
            raise ValueError('Name must contain only letters')
        if not (2 <= len(v) <= 20):
            raise ValueError('Name length must be between 2 and 20 characters')
        return v

    @validator('password')
    def password_length(cls, v):
        if not (8 <= len(v) <= 20):
            raise ValueError('Password length must be between 8 and 20 characters')
        return v

    @validator('birth_date')
    def valid_birth_date(cls, v):
        birth_date = date.fromisoformat(v)
        today = date.today()
        hundredTwentyYearsAgo = date(today.year - 120, today.month, today.day)
        sixteenYearsAgo = date(today.year - 16, today.month, today.day)
        if not (hundredTwentyYearsAgo <= birth_date <= sixteenYearsAgo):
            raise ValueError('Please enter a valid birth date. Age must be between 16 and 120 years.')
        return v
