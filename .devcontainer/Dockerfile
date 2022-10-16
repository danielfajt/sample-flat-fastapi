FROM python:3.11.0rc2-bullseye

ENV PYTHONUNBUFFERED True

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=False

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /workspace

RUN apt-get update -y && apt-get install -y \
    curl \
    git \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python -


COPY pyproject.toml poetry.lock* ./
RUN poetry install