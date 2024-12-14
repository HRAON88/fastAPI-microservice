FROM python:3.10-slim
RUN pip install poetry
WORKDIR /app
COPY ./fastAPI-microservice /app
RUN poetry install --no-root
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]