# Этап 1: Установка зависимостей с большим объемом памяти
FROM python:3.10 as builder

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

WORKDIR /home

# Копирование файлов с зависимостями
COPY ./pyproject.toml .
COPY ./poetry.lock .

# Установка Poetry
RUN pip install poetry

# Установка зависимостей проекта
RUN poetry install --verbose --no-interaction

# Этап 2: Копирование необходимых файлов в более легкий образ
FROM python:3.10

WORKDIR /home

# Копирование зависимостей из предыдущего этапа
COPY --from=builder /home /home

# Копирование остальных файлов и установка приложения
COPY ./app ./app

ENTRYPOINT ["./app/entrypoint.sh"]
