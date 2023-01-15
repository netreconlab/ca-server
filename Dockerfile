FROM python:3.10.5

WORKDIR /app

COPY ./pyproject*.toml ./

COPY ./poetry*.lock ./

RUN apt-get update \
      && apt-get upgrade -y \
      && python3 -m pip install poetry \
      && poetry install

