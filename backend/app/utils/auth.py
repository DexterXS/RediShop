from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = "some_logic_to_extract_user_id_from_token"
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user
