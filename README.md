# Habit and Task Tracker

REST API для управления задачами и привычками на FastAPI. Поддерживает кэширование через Redis и фоновые задачи через Celery.

---

## 🚀 Стек технологий

* **FastAPI** — веб-фреймворк
* **SQLAlchemy** — ORM
* **PostgreSQL** — база данных
* **Redis** — кэш и брокер для Celery
* **Celery** — фоновые задачи
* **Alembic** — миграции
* **Docker** — контейнеризация

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo_url>
cd habbit_task_tracker
```

### 2. Настроить переменные окружения

```bash
cp .env.example .env
```

Заполни `.env` своими значениями.

### 3. Запустить PostgreSQL и Redis

```bash
docker-compose up -d
```

### 4. Применить миграции

```bash
uv run alembic upgrade head
```

### 5. Запустить FastAPI

```bash
uv run uvicorn main:app --reload
```

### 6. Запустить Celery (в отдельном терминале)

```bash
uv run celery -A celery_app worker --loglevel=info
```

---

## 📡 API

После запуска:

* Swagger: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

---

## 📁 Структура проекта

```
habbit_task_tracker/
├── app/                # основное приложение
│   ├── api/            # endpoints (FastAPI)
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # бизнес-логика
│   ├── repository/     # работа с БД
│   └── cache/          # Redis-кэш
├── migrations/         # Alembic миграции
├── celery_app.py       # настройка Celery
├── docker-compose.yml
├── pyproject.toml
└── main.py
```

---

## 🧠 Возможности

* CRUD для задач и категорий
* Кэширование данных в Redis
* Фоновые задачи через Celery
* Фильтрация задач
* Чистое разделение: service / repository / cache

---

## 📌 TODO (опционально)

* Добавить авторизацию
* Покрыть тестами
* Оптимизировать кеширование списков
* Добавить rate limiting
