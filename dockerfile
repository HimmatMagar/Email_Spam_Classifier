FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies into the system environment
RUN uv sync --frozen --no-dev --no-install-project

# Copy application
COPY . .

RUN uv sync --frozen --no-dev

EXPOSE 5000

CMD ["uv", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]