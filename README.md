# TenderHack Backend Template

Минимальный backend-каркас для хакатона на FastAPI.

Проект собран как шаблон модульного монолита: API-контракты, зависимости, сервисный слой, тестовый каркас, Docker-запуск и Swagger-документация уже подготовлены, а бизнес-логика может добавляться постепенно.

## Что уже есть

- FastAPI-приложение с `create_app()`
- versioned API под `/api/v1`
- healthcheck `GET /health`
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI schema: `/openapi.json`
- базовый DI-слой через `Depends`
- сервисные заглушки для parsing и auth
- pytest-тесты для smoke, health, docs и шаблонных endpoints
- Dockerfile и docker-compose для локального запуска

## Как поднять проект локально

### Вариант 1. Через Docker

Это основной и самый простой способ для текущего шаблона.

1. Убедись, что установлен Docker Desktop.
2. Из корня проекта запусти:

```bash
docker compose up --build app
```

Если у тебя на Windows вместо `docker compose` доступен `docker-compose`, используй PowerShell-скрипт:

```powershell
.\scripts\run.ps1
```

После запуска приложение будет доступно по адресам:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
- `http://localhost:8000/openapi.json`

### Вариант 2. Через Python локально

Если хочешь запускать без Docker, подготовь виртуальное окружение и установи зависимости из `requirements.txt`.

Пример команд:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

На Windows PowerShell активация обычно выглядит так:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Переменные окружения

Шаблон переменных лежит в [.env.example](C:/Users/BartsitsAV/repos/Hackatons/TenderHack/.env.example#L1).

Основные переменные:

- `APP_NAME` имя приложения
- `APP_ENV` окружение (`development`, `production`)
- `DEBUG` флаг debug-режима
- `HOST` хост запуска
- `PORT` порт приложения
- `DOCS_URL` путь до Swagger UI
- `REDOC_URL` путь до ReDoc
- `OPENAPI_URL` путь до OpenAPI schema
- `DATABASE_URL` строка подключения к БД
- `REDIS_URL` строка подключения к Redis
- `LOG_LEVEL` уровень логирования

### Полезные команды

Через `Makefile`:

```bash
make run
make test
make lint
```

Через PowerShell:

```powershell
.\scripts\run.ps1
.\scripts\test.ps1
.\scripts\lint.ps1
```

Что делают команды:

- `run` поднимает backend
- `test` запускает `pytest` внутри контейнера
- `lint` запускает `ruff check .`

## Структура проекта

```text
.
|-- app/
|   |-- api/
|   |   `-- v1/
|   |       |-- endpoints/
|   |       `-- router.py
|   |-- core/
|   |   |-- config.py
|   |   |-- db.py
|   |   |-- dependencies.py
|   |   |-- exception_handlers.py
|   |   |-- logging.py
|   |   `-- middleware.py
|   |-- models/
|   |-- repositories/
|   |-- schemas/
|   |-- services/
|   `-- main.py
|-- alembic/
|-- tests/
|   |-- integration/
|   `-- unit/
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- pyproject.toml
`-- main.py
```

Кратко по слоям:

- `app/main.py` создание и конфигурация FastAPI-приложения
- `app/api/v1/endpoints/` HTTP-ручки
- `app/api/v1/router.py` агрегация всех роутеров версии API
- `app/schemas/` входные и выходные Pydantic-схемы
- `app/services/` бизнес-логика и сервисные контракты
- `app/repositories/` доступ к данным
- `app/models/` ORM-модели и доменные сущности
- `app/core/` настройки, DI, middleware, logging, обработка ошибок
- `tests/unit/` unit-тесты
- `tests/integration/` интеграционные тесты HTTP-слоя

## Как добавлять новую ручку

В проекте используется последовательность:

`router -> schema -> service -> test`

Ниже рекомендуемый порядок добавления новой фичи.

### 1. Создать схемы

Сначала опиши входные и выходные данные в `app/schemas/`.

Пример:

- `CreateItemRequest`
- `ItemResponse`

Зачем сначала схемы:

- сразу фиксируется API-контракт
- Swagger начинает показывать будущую ручку корректно
- проще писать роут и тесты

### 2. Добавить сервис

Создай или расширь сервис в `app/services/`.

Сервис должен:

- принимать уже готовые параметры
- содержать бизнес-логику
- не зависеть от HTTP-деталей

Роут не должен напрямую реализовывать бизнес-правила.

### 3. Подключить dependency

Если сервису нужны `settings`, `db_session` или другие зависимости, добавь провайдер в `app/core/dependencies.py`.

Идея такая:

- роут запрашивает dependency через `Depends`
- dependency создает сервис
- сервис выполняет логику

### 4. Создать endpoint

Добавь новый файл или новую ручку в `app/api/v1/endpoints/`.

Правила для endpoint:

- использовать `APIRouter`
- указывать `prefix`, `summary`, `tags`
- задавать `response_model`
- не хранить бизнес-логику внутри обработчика
- ошибки бизнес-слоя преобразовывать в корректные HTTP-ответы

### 5. Подключить роутер в общий router

Зарегистрируй новый роутер в [app/api/v1/router.py](C:/Users/BartsitsAV/repos/Hackatons/TenderHack/app/api/v1/router.py#L1).

Без этого ручка не попадет в приложение и не появится в Swagger.

### 6. Написать тест

Для каждой ручки нужен как минимум один интеграционный тест в `tests/integration/`.

Обычно стоит проверить:

- успешный сценарий
- валидацию входных данных
- ошибки бизнес-логики
- ожидаемый HTTP статус
- ожидаемый JSON-ответ

Если логика сложная, дополнительно добавляй unit-тесты для сервиса.

### Мини-пример

1. `app/schemas/item.py`
2. `app/services/item_service.py`
3. `app/core/dependencies.py`
4. `app/api/v1/endpoints/items.py`
5. `app/api/v1/router.py`
6. `tests/integration/test_items.py`

## Правила именования и code-style

### Именование

- файлы и модули: `snake_case`
- функции и переменные: `snake_case`
- классы: `PascalCase`
- константы: `UPPER_SNAKE_CASE`
- Pydantic-схемы: понятные суффиксы `Request`, `Response`
- сервисы: суффикс `Service`
- тесты: `test_*.py`

### Правила по слоям

- endpoint работает с HTTP и dependency injection
- service содержит бизнес-логику
- repository отвечает за доступ к данным
- schema описывает контракт запросов и ответов
- core хранит общую инфраструктуру проекта

Нельзя смешивать эти роли в одном месте без необходимости.

### Code style

- придерживаться простого и предсказуемого Python-кода
- не дублировать логику между роутами
- не создавать сервисы напрямую внутри endpoint, использовать `Depends`
- добавлять `response_model`, `summary` и `tags` для ручек
- писать короткие docstring там, где они реально помогают
- новые ручки сразу отражать тестами
- не складывать бизнес-логику в middleware или schema

### Линтинг

В проекте настроен `ruff`.

Основные проверки описаны в [pyproject.toml](C:/Users/BartsitsAV/repos/Hackatons/TenderHack/pyproject.toml#L1):

- `E` базовые style/error правила
- `F` ошибки Python-кода
- `I` порядок импортов

Запуск:

```bash
make lint
```

или

```powershell
.\scripts\lint.ps1
```

## Документация API

После запуска проекта смотри ручки здесь:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Swagger особенно полезен для шаблонного backend-а, потому что позволяет сразу видеть:

- какие ручки уже подключены
- какие request/response схемы у них есть
- какие статусы и параметры ожидаются

## Текущее состояние шаблона

Сейчас проект содержит именно каркас:

- часть сервисов работает как заглушка и возвращает `501 Not Implemented`
- auth-слой пока без реальной JWT-реализации
- SQLite используется как временный простой storage для шаблона

Это нормально для хакатонного этапа: сначала фиксируется структура, потом постепенно добавляется логика.
