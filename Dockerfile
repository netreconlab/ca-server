FROM python:3.10-slim AS build

WORKDIR /app

COPY ./pyproject*.toml ./
COPY ./poetry*.lock ./

RUN apt-get update \
      && apt-get upgrade -y --no-install-recommends \
      && python3 -m venv /app/venv \
      && . /app/venv/bin/activate \
      && python3 -m pip install poetry \
      && poetry install
      
FROM python:3.10-slim AS release

WORKDIR /app
COPY --from=build /app/venv ./venv
COPY ./server ./server
COPY ./pyproject*.toml ./
COPY ./poetry*.lock ./

EXPOSE 3000

CMD . /app/venv/bin/activate && exec poetry run uvicorn server.main:app --host 0.0.0.0 --port 3000