FROM python:3.10
LABEL authors="zai"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install -y \
    netcat-openbsd \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    libgl1-mesa-glx \
    build-essential \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
# Установка poetry
RUN python -m pip install poetry

RUN mkdir -p /home/app
RUN mkdir -p /home/app/static


WORKDIR /home

# Копирование файлов с зависимостями
COPY ./pyproject.toml .
COPY ./poetry.lock .

# Установка зависимостей
RUN poetry install --verbose --no-interaction

COPY ./app ./app


ENTRYPOINT ["./app/entrypoint.sh"]