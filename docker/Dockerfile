FROM python:3.13-slim AS base

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

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"


FROM base AS production

COPY my-resume/ /resume/
COPY templates/ /templates/

EXPOSE 8000

CMD ["uvicorn", "my_career.adapters.api.app:app", "--host", "0.0.0.0", "--port", "8000"]


FROM base AS test

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY tests/ /app/tests/

ENV OPENAI_API_KEY=test-key
ENV JWT_SECRET=test-secret-long-enough-for-hmac-sha256-requirement

CMD ["pytest"]
