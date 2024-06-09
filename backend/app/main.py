import sys
import os
import logging
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from backend.app.database.database import SessionLocal, init_db
from backend.app.database.crud import get_user_by_email, create_user, verify_password, pwd_context
from backend.app.schemas.schemas import UserCreate  # Импортируем схемы

# Добавление корневого пути в sys.path
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(root_path)

# Импортируем модули из backend.app.api
from backend.app.api import auth, products, user, cart

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Разрешить CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])

# Корректировка путей к папкам
base_path = os.path.abspath(os.path.join(root_path, ".."))
static_path = os.path.join(base_path, "frontend", "static")
templates_path = os.path.join(base_path, "frontend", "templates")

if not os.path.exists(static_path):
    raise RuntimeError(f"Directory '{static_path}' does not exist")

app.mount("/static", StaticFiles(directory=static_path), name="static")

if not os.path.exists(templates_path):
    raise RuntimeError(f"Directory '{templates_path}' does not exist")

templates = Jinja2Templates(directory=templates_path)

# Создание сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация базы данных
@app.on_event("startup")
def on_startup():
    init_db()

# Обработка корневого маршрута
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(
        user: UserCreate,
        request: Request,
        db: Session = Depends(get_db)
):
    logger.info("Received registration request")
    logger.info(
        f"First Name: {user.first_name}, Last Name: {user.last_name}, Email: {user.email}, Birth Date: {user.birth_date}, Address: {user.address}")
    logger.info(f"Password: {user.password}, Confirm Password: {user.confirm_password}")

    if user.password != user.confirm_password:
        logger.error("Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        logger.error("Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user.first_name, user.last_name, user.email, user.password, user.birth_date,
                           user.address)
    logger.info(f"User {user.email} registered successfully")

    return RedirectResponse(url="/profile", status_code=302)

@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request, db: Session = Depends(get_db)):
    user_name = "User"  # Замените на актуальное имя пользователя из базы данных
    return templates.TemplateResponse("user_profile.html", {"request": request, "user_name": user_name})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for user: {username}")
    user = get_user_by_email(db, username)
    if not user or not verify_password(password, user.password):
        logger.error("Invalid username or password")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    logger.info(f"User {username} logged in successfully")
    # Если логин прошел успешно, перенаправляем на страницу профиля
    return RedirectResponse(url="/profile", status_code=302)
