from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Модель данных (то, что у нас хранится и ходит в JSON)
class Product(BaseModel):
    id: int
    name: str
    price: float

# "База данных" в памяти (обычно тут была бы реальная БД)
products_db = {
    1: Product(id=1, name="Milk", price=89.9),
    2: Product(id=2, name="Bread", price=49.0),
}

# GET /products - получить список всех продуктов
@app.get("/products")
def list_products():
    return list(products_db.values())
    # возвращаем JSON-массив объектов Product

# GET /products/{product_id} - получить продукт по id
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products_db.get(product_id)
    if not product:
        # 404 - если такого ресурса нет
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# POST /products - создать новый продукт
@app.post("/products", status_code=201)
def create_product(product: Product):
    if product.id in products_db:
        # 400 - некорректный запрос (id уже занят)
        raise HTTPException(status_code=400, detail="Product already exists")
    products_db[product.id] = product
    return product

# Пример искусственной 500 - ошибка сервера
@app.get("/error")
def cause_error():
    # тут мы специально кидаем исключение
    raise RuntimeError("Something went wrong on server")