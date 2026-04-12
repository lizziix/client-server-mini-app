import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import products_db
from app.models import Product

# Начальное состояние БД — восстанавливается перед каждым тестом
INITIAL_PRODUCTS = {
    1: Product(id=1, name="Milk", price=89.9),
    2: Product(id=2, name="Bread", price=49.0),
}


@pytest.fixture(autouse=True)
def reset_db():
    """Сбрасывает products_db в исходное состояние перед каждым тестом."""
    products_db.clear()
    products_db.update(INITIAL_PRODUCTS)
    yield
    # teardown — необязателен, но явно подчёркивает намерение
    products_db.clear()


@pytest.fixture
def client():
    """TestClient — аналог requests, но без реального HTTP."""
    with TestClient(app) as c:
        yield c
