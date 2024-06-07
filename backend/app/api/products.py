from fastapi import APIRouter, Depends, HTTPException
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import create_product, get_product, update_product, delete_product, get_products

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def add_product(product: ProductCreate):
    db_product = create_product(product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: str):
    db_product = get_product(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(product_id: str, product: ProductUpdate):
    db_product = update_product(product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def remove_product(product_id: str):
    result = delete_product(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/", response_model=List[ProductResponse])
def list_products():
    return get_products()
