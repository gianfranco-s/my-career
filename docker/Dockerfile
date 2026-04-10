FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libffi8 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock /app/
COPY src/my_career /app/my_career/
COPY my-resume/ /resume/
COPY templates/ /templates/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "my_career.adapters.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
