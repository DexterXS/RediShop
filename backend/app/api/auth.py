from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.schemas.user import UserCreate, UserLogin, UserResponse
from backend.app.services.auth_service import create_user, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    db_user = create_user(user)
    return db_user

@router.post("/login", response_model=UserResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
