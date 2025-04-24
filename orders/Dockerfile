FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PATH="/root/.local/bin:/orders/.venv/bin:$PATH"

ADD . /orders
WORKDIR /orders

RUN uv sync --frozen

CMD sh -c "alembic upgrade head && uvicorn main:app --reload --port 8000 --host 0.0.0.0"