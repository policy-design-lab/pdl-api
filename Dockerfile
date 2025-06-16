FROM python:3.9-slim

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt update \
    && apt upgrade -y \
    && apt install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/pdl-api

# Copy app folder and poetry files to the working directory
COPY app /usr/src/pdl-api/app
COPY pyproject.toml poetry.lock README.md /usr/src/pdl-api/

RUN pip install -U pip \
    && pip install poetry \
    && poetry install \
    && pip install --upgrade psycopg2-binary # Upgrade psycopg2-binary to avoid error related to SCRAM-SHA-256 authentication when running locally

# The values of these default environment variables can be overridden at runtime
ENV DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=pdl \
    DB_USERNAME=user \
    DB_PASSWORD=password \
    API_PORT=5000 \
    WORKER=4 \
    ALL_PROGRAMS_START_YEAR=2018 \
    ALL_PROGRAMS_END_YEAR=2022 \
    TITLE_I_START_YEAR=2014 \
    TITLE_I_END_YEAR=2023 \
    TITLE_II_START_YEAR=2014 \
    TITLE_II_END_YEAR=2023 \
    CROP_INSURANCE_START_YEAR=2014 \
    CROP_INSURANCE_END_YEAR=2023 \
    SNAP_START_YEAR=2018 \
    SNAP_END_YEAR=2022

WORKDIR /usr/src/pdl-api/app

CMD ["gunicorn", "main:app", "--config", "/usr/src/pdl-api/app/controllers/gunicorn_config.py"]

