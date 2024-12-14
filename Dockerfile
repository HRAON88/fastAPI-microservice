FROM python:3.10-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY ./app .
CMD ["poetry", "run", "uvicorn", "__main__:app", "--host", "0.0.0.0", "--port", "8000"]