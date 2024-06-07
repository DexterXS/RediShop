from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime
from typing import Optional

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
    # Сохранение db_user в базу данных
    return db_user

def authenticate_user(email: str, password: str) -> Optional[User]:
    # Получить пользователя из базы данных по email
    db_user = get_user_by_email(email)
    if db_user and verify_password(password, db_user.hashed_password):
        return db_user
    return None
