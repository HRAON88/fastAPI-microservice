FROM python:3.10-slim

# Получаем UID и GID из аргументов сборки
ARG UID=1000
ARG GID=1000

# Создаем пользователя с тем же UID/GID что и deploy пользователь
RUN groupadd -g ${GID} appgroup && \
    useradd -u ${UID} -g ${GID} -m appuser

# Установка Poetry
RUN pip install poetry

WORKDIR /app

# Копирование и установка зависимостей
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install

# Копирование исходного кода
COPY ./app ./app

# Компиляция Python файлов и установка правильных прав
RUN python -m compileall ./app \
    && chown -R ${UID}:${GID} /app \
    && find ./app -type d -exec chmod 755 {} + \
    && find ./app -type f -exec chmod 644 {} + \
    && ls -la && ls -la app/

# Переключение на пользователя appuser
USER appuser

# Запуск приложения с правильным путем
CMD ["poetry", "run", "uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8002"]
