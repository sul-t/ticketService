FROM python:3.12-alpine

ENV UV_CACHE_DIR=/uv-cache/
ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1
WORKDIR /src

# скачивание зависимостей
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=${UV_CACHE_DIR},id=uv,sharing=locked \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install -r pyproject.toml

ADD main.py config.py .env alembic.ini ./
COPY src ./src
COPY migration ./migration

CMD ["sh",  "-c", "alembic upgrade head && uvicorn main:app --reload --port 8000 --host 0.0.0.0"]