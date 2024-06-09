from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.app.database.models import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, birth_date: str, address: str):
    hashed_password = pwd_context.hash(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        birth_date=birth_date,
        address=address
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
