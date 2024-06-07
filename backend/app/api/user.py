from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserUpdate, UserResponse
from app.services.user_service import get_user, update_user
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(user: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    updated_user = update_user(current_user.email, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
