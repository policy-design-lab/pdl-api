FROM python:3.9-slim

ENV POETRY_VIRTUALENVS_CREATE false

RUN apt update && apt upgrade -y

WORKDIR /usr/src/pdl-api

COPY . .

RUN pip install -U pip
RUN pip install poetry
RUN poetry install

ENV DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=pdl \
    DB_USERNAME=user \
    DB_PASSWORD=password \
    WORKER=4

WORKDIR /usr/src/pdl-api/app

CMD ["gunicorn", "main:app", "--config", "/usr/src/pdl-api/app/controllers/gunicorn_config.py"]

