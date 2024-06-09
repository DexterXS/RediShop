import sys
import os
import uuid
import logging
from fastapi import FastAPI, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from backend.app.database.database import SessionLocal, init_db
from backend.app.database.crud import get_user_by_email, create_user, verify_password, pwd_context
from backend.app.schemas.schemas import UserCreate
from backend.app.database.crud import get_cart_items
from backend.app.database.crud import get_products, add_product, add_to_cart, get_cart_count

# Добавление корневого пути в sys.path
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(root_path)

# Обновление пути для загруженных изображений
UPLOAD_DIRECTORY = "frontend/static/uploaded_images"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

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


@app.get("/cart", response_class=HTMLResponse)
async def get_cart(request: Request, db: Session = Depends(get_db)):
    user_id = 1  # Замените это на фактический ID пользователя, например, из сессии или токена
    cart_items = get_cart_items(db, user_id)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    cart_count = len(set(item.product_id for item in cart_items))

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_count": cart_count
    })


@app.post("/add_product")
async def add_product_endpoint(name: str = Form(...), quantity: int = Form(...), price: float = Form(...),
                               image: UploadFile = File(...), description: str = Form(...),
                               db: Session = Depends(get_db)):
    # Убедитесь, что директория для сохранения изображений существует
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    # Получение расширения файла изображения
    file_extension = os.path.splitext(image.filename)[1]
    # Создание уникального имени файла
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    # Путь для сохранения изображения
    image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    user_id = 1  # Замените это на фактический ID пользователя, например, из сессии или токена
    relative_image_path = os.path.join("uploaded_images", unique_filename)
    add_product(db, user_id, name, description, int(price), relative_image_path, quantity)
    return RedirectResponse(url="/profile", status_code=302)


@app.get("/products", response_class=JSONResponse)
async def get_products_endpoint(db: Session = Depends(get_db)):
    products = get_products(db)
    products_json = [{"id": p.id, "name": p.name, "price": p.price, "image_path": p.image_path, "description": p.description} for p in products]
    return JSONResponse(content=products_json)


@app.post("/add_to_cart")
async def add_to_cart_endpoint(productId: int = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    user_id = 1  # Замените это на фактический ID пользователя, например, из сессии или токена
    add_to_cart(db, user_id, productId, quantity)
    return JSONResponse(content={"status": "success"})

@app.get("/cart_count", response_class=JSONResponse)
async def get_cart_count_endpoint(db: Session = Depends(get_db)):
    user_id = 1  # Замените это на фактический ID пользователя, например, из сессии или токена
    count = get_cart_count(db, user_id)
    return JSONResponse(content=count)