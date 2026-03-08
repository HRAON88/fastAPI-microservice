FROM python:3.10-slim

ARG UID=1000
ARG GID=1000


RUN groupadd -g ${GID} appgroup && \
    useradd -u ${UID} -g ${GID} -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install uv
RUN uv pip install --system -r requirements.txt

# Копирование исходного кода
COPY ./app ./app


USER appuser

ENV PYTHONDONTWRITEBYTECODE 1

# Запуск приложения с правильным путем
CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8002"]
