FROM python:3.10-alpine
LABEL authors="zai"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
# Установка poetry
RUN python -m pip install --no-cache-dir poetry

RUN mkdir -p /home/app
RUN mkdir -p /home/app/static


WORKDIR /home

# Копирование файлов с зависимостями
COPY ./pyproject.toml .
COPY ./poetry.lock .

# Установка зависимостей
RUN poetry install

COPY ./app ./app

ENTRYPOINT ["./app/entrypoint.sh"]