# Products API

Учебный проект для практики построения клиент-серверных приложений, написания тестов с Pytest и E2E-тестирования с Playwright.

## О проекте

Сервер на **FastAPI** реализует CRUD для списка продуктов. Клиентская часть — одностраничный интерфейс на чистом **HTML/CSS/JavaScript**, который общается с сервером через `fetch`. Данные хранятся в памяти.

## Структура

```
Client_Server/
├── app/
│   ├── main.py        # FastAPI приложение, подключение роутера и статики
│   ├── router.py      # эндпоинты: GET, POST, PUT, DELETE /products
│   ├── models.py      # Pydantic-модели Product и ProductUpdate
│   └── database.py    # хранилище в памяти
├── static/
│   ├── index.html     # разметка
│   ├── style.css      # стили
│   └── app.js         # fetch-запросы и рендер таблицы
└── tests/
    ├── conftest.py            # фикстуры: client, reset_db
    ├── test_models.py         # unit-тесты моделей
    ├── test_products_api.py   # integration-тесты API
    └── e2e/
        ├── conftest.py        # запуск сервера, восстановление данных
        └── test_ui.py         # E2E-тесты через браузер
```

## Установка

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install fastapi uvicorn aiofiles requests httpx pytest pytest-playwright && playwright install chromium
```

## Запуск сервера

```bash
uvicorn app.main:app --reload
```

- UI → `http://127.0.0.1:8000`
- Swagger → `http://127.0.0.1:8000/docs`

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/products` | Список всех продуктов |
| GET | `/products/{id}` | Продукт по ID |
| POST | `/products` | Создать продукт |
| PUT | `/products/{id}` | Обновить продукт |
| DELETE | `/products/{id}` | Удалить продукт |

## Запуск через Docker

```bash
# Собрать образ
docker build -t products-api .

# Запустить контейнер
docker run -p 8000:8000 products-api
```

- UI → `http://localhost:8000`
- Swagger → `http://localhost:8000/docs`

## Тесты

```bash
# Unit + integration (без сервера)
python3 -m pytest tests/ -v --ignore=tests/e2e

# E2E (Playwright сам запустит сервер)
python3 -m pytest tests/e2e/ -v

# E2E с видимым браузером
python3 -m pytest tests/e2e/ -v --headed

# Все тесты
python3 -m pytest tests/ -v
```

### Уровни тестирования

| Уровень | Файл | Что проверяет |
|---|---|---|
| Unit | `test_models.py` | валидация Pydantic-моделей |
| Integration | `test_products_api.py` | все API-эндпоинты через TestClient |
| E2E | `test_ui.py` | пользовательские сценарии в браузере |

## Стек

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [Pydantic](https://docs.pydantic.dev/) — валидация данных
- [Pytest](https://pytest.org/) — тестирование
- [Playwright](https://playwright.dev/python/) — E2E-тестирование
