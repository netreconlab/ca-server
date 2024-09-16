FROM python:3.12-slim AS build

WORKDIR /app

COPY ./pyproject*.toml ./
COPY ./poetry*.lock ./

RUN apt-get update \
 && apt-get upgrade -y --no-install-recommends \
 && apt-get install -y --no-install-recommends gcc python3-dev \
 && python3 -m venv /app/venv \
 && . /app/venv/bin/activate \
 && python3 -m pip install poetry \
 && poetry install
 
FROM python:3.12-slim AS release

RUN groupadd -g 999 python \
 && useradd -r -u 999 -g python python \
 && mkdir app \
 && chown python:python app
USER 999

WORKDIR /app
COPY --chown=python:python --from=build /app/venv ./venv
COPY --chown=python:python --from=build /app/poetry*.lock ./
COPY --chown=python:python --from=build /app/pyproject*.toml ./
COPY --chown=python:python ./scripts/start-poetry.sh .
COPY --chown=python:python ./server ./server

EXPOSE 3000

CMD [ "./start-poetry.sh", "poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "3000" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:3000/health
