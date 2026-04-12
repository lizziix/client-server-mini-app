from fastapi import APIRouter, HTTPException

from app.models import Product, ProductUpdate
from app.database import products_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", summary="Список всех продуктов")
def list_products():
    return list(products_db.values())


@router.get("/{product_id}", summary="Получить продукт по ID")
def get_product(product_id: int):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", status_code=201, summary="Создать продукт")
def create_product(product: Product):
    if product.id in products_db:
        raise HTTPException(status_code=400, detail="Product already exists")
    products_db[product.id] = product
    return product


@router.put("/{product_id}", summary="Обновить продукт")
def update_product(product_id: int, update: ProductUpdate):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = product.model_copy(update=update.model_dump(exclude_none=True))
    products_db[product_id] = updated
    return updated


@router.delete("/{product_id}", status_code=204, summary="Удалить продукт")
def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
