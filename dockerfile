FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Copy application
COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 5000

CMD ["uv", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]