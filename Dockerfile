FROM python:3.10-slim

# Установка Poetry
RUN pip install poetry

WORKDIR /app

# Копирование и установка зависимостей
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install

# Копирование исходного кода
COPY ./app ./app

# Компиляция Python файлов
RUN python -m compileall ./app \
    && find ./app -type d -name "__pycache__" -exec chmod 755 {} + \
    && find ./app -type f -name "*.pyc" -exec chmod 644 {} + \
    && ls -la && ls -la app/

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8002"]

