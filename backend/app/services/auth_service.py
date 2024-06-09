from passlib.context import CryptContext
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from datetime import datetime
from typing import Optional
from backend.app.services.user_service import get_user_by_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        birth_date=user.birth_date
    )
    return db_user

def authenticate_user(email: str, password: str) -> Optional[User]:
    db_user = get_user_by_email(email)
    if db_user and verify_password(password, db_user.hashed_password):
        return db_user
    return None
