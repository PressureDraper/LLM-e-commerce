# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder
 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
 
WORKDIR /app
 
COPY pyproject.toml .
RUN uv sync --no-dev --frozen
 
# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime
 
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
 
COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic
 
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
 
EXPOSE 8000

CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2