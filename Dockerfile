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

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
USER 999

WORKDIR /app
COPY --from=build /app/venv ./venv
COPY ./scripts/start-poetry.sh .
COPY ./server ./server
COPY ./pyproject*.toml ./
COPY ./poetry*.lock ./

EXPOSE 3000

CMD [ "./start-poetry.sh", "poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "3000" ]
