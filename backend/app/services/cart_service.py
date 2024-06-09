from typing import List
from backend.app.models.cart import CartItem
from backend.app.schemas.cart import CartItemCreate, CartItemResponse

def add_to_cart(cart_item: CartItemCreate) -> CartItemResponse:

    pass

def get_cart_items(user_id: int) -> List[CartItemResponse]:

    pass

def remove_from_cart(cart_item_id: int) -> None:

    pass
