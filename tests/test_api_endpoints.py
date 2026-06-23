"""
Testes de endpoints da API com pytest.
Utiliza TestClient do FastAPI para testes sem servidor real.
"""
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api_main import app
from schemas import CustomerInput
from services.predict_service import MODEL_FEATURE_COLUMNS, PredictService


@pytest.fixture
def client():
    """Fixture que fornece um cliente de teste."""
    return TestClient(app)


@pytest.fixture
def valid_customer_data():
    """Fixture com dados válidos de um cliente para teste."""
    return {
        "customer_id": "TEST-001",
        "zip_code": 90001,
        "gender": "Male",
        "senior_citizen": "Yes",
        "partner": "Yes",
        "dependents": "Yes",
        "tenure_months": 48,
        "phone_service": "Yes",
        "multiple_lines": "Yes",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "Yes",
        "streaming_movies": "Yes",
        "contract": "One year",
        "paperless_billing": "No",
        "payment_method": "Credit card (automatic)",
        "monthly_charges": 105.25,
        "total_charges": 5046.00,
    }


class TestRootEndpoint:
    """Testes para o endpoint raiz."""

    def test_root_returns_200(self, client):
        """Testa se o endpoint raiz retorna 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_correct_structure(self, client):
        """Testa se o endpoint raiz retorna estrutura esperada."""
        response = client.get("/")
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert "endpoints" in data


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""

    def test_health_returns_200(self, client):
        """Testa se health check retorna 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_returns_correct_schema(self, client):
        """Testa se health check retorna schema correto."""
        response = client.get("/api/v1/health")
        data = response.json()

        assert "status" in data
        assert "message" in data
        assert "version" in data

    def test_health_status_is_healthy(self, client):
        """Testa se status é 'healthy'."""
        response = client.get("/api/v1/health")
        data = response.json()

        assert data["status"] in ["healthy", "unhealthy"]

    def test_health_has_version(self, client):
        """Testa se versão está presente."""
        response = client.get("/api/v1/health")
        data = response.json()

        assert data["version"] is not None
        assert len(data["version"]) > 0


class TestPredictEndpoint:
    """Testes para o endpoint de predição."""

    def test_predict_returns_200_with_valid_data(self, client, valid_customer_data):
        """Testa se predict retorna 200 com dados válidos."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        assert response.status_code == 200

    def test_predict_returns_correct_schema(self, client, valid_customer_data):
        """Testa se predict retorna schema correto."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        assert "customer_id" in data
        assert "prediction" in data
        assert "prediction_label" in data
        assert "churn_probability" in data
        assert "confidence" in data

    def test_predict_returns_valid_prediction(self, client, valid_customer_data):
        """Testa se predição retorna valores válidos."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        # Verificar tipos
        assert isinstance(data["customer_id"], str)
        assert isinstance(data["prediction"], int)
        assert isinstance(data["prediction_label"], str)
        assert isinstance(data["churn_probability"], float)
        assert isinstance(data["confidence"], float)

    def test_predict_prediction_is_binary(self, client, valid_customer_data):
        """Testa se predição é 0 ou 1."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        assert data["prediction"] in [0, 1]

    def test_predict_label_matches_prediction(self, client, valid_customer_data):
        """Testa se label corresponde à predição."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        if data["prediction"] == 0:
            assert data["prediction_label"] == "No"
        else:
            assert data["prediction_label"] == "Yes"

    def test_predict_probability_is_valid_range(self, client, valid_customer_data):
        """Testa se probabilidade está entre 0 e 1."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        assert 0.0 <= data["churn_probability"] <= 1.0
        assert 0.0 <= data["confidence"] <= 1.0

    def test_predict_customer_id_is_preserved(self, client, valid_customer_data):
        """Testa se customer_id é preservado na resposta."""
        response = client.post("/api/v1/predict", json=valid_customer_data)
        data = response.json()

        assert data["customer_id"] == valid_customer_data["customer_id"]

    def test_predict_returns_400_with_missing_fields(self, client):
        """Testa se predict retorna 400 com dados incompletos."""
        incomplete_data = {"customer_id": "TEST-002"}
        response = client.post("/api/v1/predict", json=incomplete_data)

        assert response.status_code == 422  # Unprocessable Entity

    def test_predict_returns_400_with_invalid_types(self, client, valid_customer_data):
        """Testa se predict retorna 400 com tipos inválidos."""
        invalid_data = valid_customer_data.copy()
        invalid_data["tenure_months"] = "invalid"  # Should be int

        response = client.post("/api/v1/predict", json=invalid_data)
        assert response.status_code == 422

    def test_predict_returns_400_with_negative_tenure(self, client, valid_customer_data):
        """Testa se predict valida tenure_months >= 0."""
        invalid_data = valid_customer_data.copy()
        invalid_data["tenure_months"] = -5

        response = client.post("/api/v1/predict", json=invalid_data)
        assert response.status_code == 422

    def test_predict_rejects_removed_or_unknown_fields(self, client, valid_customer_data):
        invalid_data = valid_customer_data | {"country": "United States"}

        response = client.post("/api/v1/predict", json=invalid_data)

        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "extra_forbidden"

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("tenure_months", "48"),
            ("monthly_charges", "105.25"),
            ("total_charges", "5046.00"),
            ("zip_code", 100000),
        ],
    )
    def test_predict_rejects_invalid_numeric_input(
        self, client, valid_customer_data, field, value
    ):
        invalid_data = valid_customer_data | {field: value}

        response = client.post("/api/v1/predict", json=invalid_data)

        assert response.status_code == 422

    @pytest.mark.parametrize("value", [float("nan"), float("inf")])
    def test_customer_input_rejects_non_finite_total_charges(self, valid_customer_data, value):
        with pytest.raises(ValidationError):
            CustomerInput.model_validate(valid_customer_data | {"total_charges": value})

    def test_customer_input_rejects_blank_customer_id(self, valid_customer_data):
        with pytest.raises(ValidationError):
            CustomerInput.model_validate(valid_customer_data | {"customer_id": "   "})

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("gender", "Other"),
            ("senior_citizen", "true"),
            ("multiple_lines", "Unknown"),
            ("internet_service", "Satellite"),
            ("online_security", "Unknown"),
            ("contract", "Three year"),
            ("payment_method", "Cash"),
        ],
    )
    def test_predict_rejects_unknown_categories(
        self, client, valid_customer_data, field, value
    ):
        response = client.post("/api/v1/predict", json=valid_customer_data | {field: value})

        assert response.status_code == 422

    @pytest.mark.parametrize(
        "changes",
        [
            {"phone_service": "No"},
            {"phone_service": "Yes", "multiple_lines": "No phone service"},
            {"internet_service": "No"},
            {"internet_service": "DSL", "online_backup": "No internet service"},
        ],
    )
    def test_predict_rejects_inconsistent_services(self, client, valid_customer_data, changes):
        response = client.post("/api/v1/predict", json=valid_customer_data | changes)

        assert response.status_code == 422


class TestPredictInputPreparation:
    def test_prepare_input_contains_only_model_features_in_expected_order(self, valid_customer_data):
        customer = CustomerInput.model_validate(valid_customer_data)
        service = PredictService.__new__(PredictService)

        prepared = service._prepare_input_data(customer)

        assert tuple(prepared.columns) == MODEL_FEATURE_COLUMNS
        assert "customer_id" not in prepared.columns


class TestDocumentation:
    """Testes para documentação automática."""

    def test_swagger_docs_available(self, client):
        """Testa se Swagger UI está disponível."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Testa se ReDoc está disponível."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema_available(self, client):
        """Testa se schema OpenAPI está disponível."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


if __name__ == "__main__":
    # Executar testes com: pytest tests/test_api_endpoints.py -v
    pytest.main([__file__, "-v"])
