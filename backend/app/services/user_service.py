from backend.app.models.user import User
from backend.app.schemas.user import UserUpdate
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user(user_id: int):
    # Ваш код для получения пользователя по user_id
    pass

def update_user(user_id: int, user_update: UserUpdate):
    # Ваш код для обновления пользователя
    pass
