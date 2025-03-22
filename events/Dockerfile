FROM python:3.12-slim

RUN apt update && apt install -y curl 

ADD https://astral.sh/uv/0.6.4/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin:/events/.venv/bin:$PATH"
RUN which uv && uv --version

ADD . /events
WORKDIR /events

RUN uv sync --frozen

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]