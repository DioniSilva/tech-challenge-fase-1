FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY LICENSE README.md pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip && pip install \
    fastapi \
    uvicorn \
    pydantic-settings \
    python-dotenv \
    numpy \
    pandas \
    scikit-learn \
    joblib \
    imbalanced-learn \
    openpyxl


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

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]