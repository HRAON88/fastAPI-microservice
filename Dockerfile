FROM python:3.10-slim
RUN pip install poetry

WORKDIR /app

RUN poerty install --no-root

# Копирование исходного кода
COPY ./app ./app

# Запуск приложения с правильным путем
CMD ["poetry", "run", "uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8002"]
