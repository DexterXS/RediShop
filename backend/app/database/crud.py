from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.app.database.models import User
from backend.app.database.models import Product, CartItem

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


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

from backend.app.database.models import Product, CartItem


def add_product(db: Session, user_id: int, name: str, quantity: int, price: float, image_path: str):
    product = Product(name=name, price=price, image_path=image_path)
    db.add(product)
    db.commit()
    db.refresh(product)

    # Создаем элемент корзины для добавленного продукта
    cart_item = CartItem(user_id=user_id, product_id=product.id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)


def get_products(db: Session):
    return db.query(Product).all()


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
    db.commit()


def get_cart_count(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).count()