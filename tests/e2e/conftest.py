import subprocess
import time
import socket

import requests
import pytest

BASE_URL = "http://127.0.0.1:8001"

INITIAL_PRODUCTS = [
    {"id": 1, "name": "Milk",  "price": 89.9},
    {"id": 2, "name": "Bread", "price": 49.0},
]


def _wait_for_server(url: str, timeout: float = 5.0) -> None:
    """Ждёт, пока сервер не начнёт отвечать."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            requests.get(url, timeout=0.5)
            return
        except requests.ConnectionError:
            time.sleep(0.2)
    raise RuntimeError(f"Server at {url} did not start in {timeout}s")


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


@pytest.fixture(scope="session", autouse=True)
def server():
    """Запускает uvicorn на порту 8001 на время сессии тестов."""
    if not _port_is_free(8001):
        # Сервер уже запущен снаружи — не трогаем
        yield
        return

    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "app.main:app", "--port", "8001"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _wait_for_server(f"{BASE_URL}/products")
    yield
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def base_url():
    """Переопределяем base_url pytest-playwright."""
    return BASE_URL


@pytest.fixture(autouse=True)
def restore_products():
    """
    Восстанавливает начальное состояние БД после каждого теста.
    E2E-тесты бьют в реальный сервер, поэтому изоляцию делаем через API.
    """
    yield

    # Удаляем всё, что добавили тесты
    current = requests.get(f"{BASE_URL}/products").json()
    initial_ids = {p["id"] for p in INITIAL_PRODUCTS}
    for p in current:
        if p["id"] not in initial_ids:
            requests.delete(f"{BASE_URL}/products/{p['id']}")

    # Восстанавливаем удалённые / изменённые начальные продукты
    current_ids = {p["id"] for p in requests.get(f"{BASE_URL}/products").json()}
    for p in INITIAL_PRODUCTS:
        if p["id"] not in current_ids:
            requests.post(f"{BASE_URL}/products", json=p)
        else:
            requests.put(f"{BASE_URL}/products/{p['id']}",
                         json={"name": p["name"], "price": p["price"]})
