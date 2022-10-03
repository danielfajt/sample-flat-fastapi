FROM python:3.10-slim-bullseye as requirements-stage

ENV PYTHONUNBUFFERED True
WORKDIR /tmp

RUN pip install poetry
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED True
WORKDIR /app

RUN apt-get update -y

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /src /app

# Change to uvicorn
CMD ["python", "main.py"]