from fastapi import APIRouter, Depends, HTTPException
from typing import List  # Добавлен импорт
from backend.app.schemas.cart import CartItemCreate, CartItemResponse
from backend.app.services.cart_service import add_to_cart, get_cart_items, remove_from_cart
from backend.app.utils.auth import get_current_user
from backend.app.schemas.user import UserResponse  # Добавлен импорт

router = APIRouter()

@router.post("/", response_model=CartItemResponse)
def add_item_to_cart(cart_item: CartItemCreate, current_user: UserResponse = Depends(get_current_user)):
    return add_to_cart(current_user.email, cart_item)

@router.get("/", response_model=List[CartItemResponse])
def read_cart_items(current_user: UserResponse = Depends(get_current_user)):
    return get_cart_items(current_user.email)

@router.delete("/{item_id}")
def delete_cart_item(item_id: str, current_user: UserResponse = Depends(get_current_user)):
    if not remove_from_cart(current_user.email, item_id):
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message": "Item removed from cart"}
