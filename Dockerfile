# syntax=docker/dockerfile:experimental
FROM python:3.8

RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked apt install unzip

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked pip install -r requirements.txt

COPY . .

CMD ["bash", "./scripts/entrypoint.sh"]
