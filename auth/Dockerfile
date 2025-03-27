FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PATH="/root/.local/bin:/auth/.venv/bin:$PATH"

ADD . /auth
WORKDIR /auth

RUN uv sync --frozen

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
