FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ../pyproject.toml /app/pyproject.toml
COPY ../uv.lock /app/uv.lock
COPY ../api /app

WORKDIR /app/src
RUN uv sync --frozen --no-cache

EXPOSE 8080

CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8080", "--host", "0.0.0.0", "--workers", "3"]