FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --extra postgres --extra redis

FROM python:3.14-slim

RUN useradd --create-home --uid 1000 app

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY main.py config.py ./
COPY src ./src
COPY assets ./assets

RUN mkdir /app/cache /app/numba_cache && chown app:app /app/cache /app/numba_cache

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    NUMBA_CACHE_DIR=/app/numba_cache \
    RUN_LOCALLY=false \
    WEB_CONCURRENCY=2

USER app
EXPOSE 8050

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8050/')"]

CMD ["gunicorn", "main:server", "--bind", "0.0.0.0:8050", "--timeout", "120"]
