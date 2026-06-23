FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip uv

COPY LICENSE README.md pyproject.toml Makefile ./
COPY src ./src

RUN UV_TORCH_BACKEND=cpu make install-runtime DOCKER_PYTHON=/opt/venv/bin/python


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    APP_NAME="Telco Churn Prediction API" \
    DEBUG="false" \
    LOG_LEVEL="INFO" \
    API_PREFIX="/api" \
    API_V1_PREFIX="/api/v1"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src ./src
COPY models ./models

RUN test -f models/mlp.joblib || (echo "models/mlp.joblib ausente. Rode 'make train' antes do docker build." >&2 && exit 1)

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]