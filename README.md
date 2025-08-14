# 🚀 Payment Service API

---

## Запуск через Docker Compose
1. Установка зависимостей
Убедитесь, что установлены:
- **Docker** ≥ 24.x
- **Docker Compose** ≥ 2.x

2. Запуск
docker-compose up --build -d
3. Что произойдет при запуске:

    Поднимется контейнер с PostgreSQL (db).

    Поднимется контейнер с приложением (app).

    Автоматически применятся миграции.

    В базу будут добавлены дефолтные пользователи:

### Администратор
## email: admin@example.com
## password: admin123

### Обычный пользователь
## email: user@example.com
## password: user123

### Запуск без Docker
1. Установить Python 3.12+

2. Установить Poetry

3. Установить зависимости через Poetry

poetry install

4. Создать базу данных PostgreSQL

CREATE DATABASE test_db;
CREATE USER test WITH PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE test_db TO test;

5. Настроить переменные окружения

В файле .dev.env:
в настройках PostgreSQL прописать настройки для подключения к своей бд

6. Применить миграции
poetry run alembic upgrade head

7. Запустить приложение
poetry run uvicorn src.main:app --reload
