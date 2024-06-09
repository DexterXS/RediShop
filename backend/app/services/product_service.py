from typing import List, Optional
from backend.app.models.product import Product
from backend.app.schemas.product import ProductCreate, ProductUpdate
from pymongo import MongoClient

# Инициализируем клиент MongoDB и выбираем базу данных и коллекцию
client = MongoClient("mongodb://localhost:27017")
db = client["myshop"]
collection = db["products"]

def create_product(product: ProductCreate) -> Product:
    product_dict = product.dict()
    result = collection.insert_one(product_dict)
    product_dict["_id"] = str(result.inserted_id)
    return Product(**product_dict)

def get_product(product_id: str) -> Optional[Product]:
    product_data = collection.find_one({"_id": product_id})
    if product_data:
        return Product(**product_data)
    return None

def update_product(product_id: str, product: ProductUpdate) -> Optional[Product]:
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    result = collection.update_one({"_id": product_id}, {"$set": update_data})
    if result.modified_count == 1:
        updated_product = collection.find_one({"_id": product_id})
        return Product(**updated_product)
    return None

def delete_product(product_id: str) -> bool:
    result = collection.delete_one({"_id": product_id})
    return result.deleted_count == 1

def get_products() -> List[Product]:
    products = []
    for product_data in collection.find():
        products.append(Product(**product_data))
    return products
