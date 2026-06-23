from datetime import datetime, timezone

from schemas import CustomerInput
from ui.app import (
    GITHUB_REPOSITORY_URL,
    INTERNET_ADD_ON_FIELDS,
    MAX_PREDICTION_HISTORY,
    PT_BR_LABELS,
    add_prediction_history,
    build_payload,
    build_reference_links,
    format_option,
    normalize_dependent_service_values,
)


def test_build_payload_contains_the_customer_id_and_20_model_features():
    values = {
        "customer_id": " TEST-001 ",
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
        "total_charges": 5046,
    }

    payload = build_payload(values)

    assert payload["customer_id"] == "TEST-001"
    assert len(payload) == 21
    assert len(set(payload) - {"customer_id"}) == 20
    assert payload["total_charges"] == 5046.0
    assert set(INTERNET_ADD_ON_FIELDS).issubset(payload)


def test_normalized_dependent_services_produce_a_valid_api_payload():
    values = {
        "customer_id": "TEST-001",
        "zip_code": 90001,
        "gender": "Male",
        "senior_citizen": "Yes",
        "partner": "Yes",
        "dependents": "Yes",
        "tenure_months": 48,
        "phone_service": "No",
        "multiple_lines": "Yes",
        "internet_service": "No",
        "online_security": "Yes",
        "online_backup": "Yes",
        "device_protection": "Yes",
        "tech_support": "Yes",
        "streaming_tv": "Yes",
        "streaming_movies": "Yes",
        "contract": "One year",
        "paperless_billing": "No",
        "payment_method": "Credit card (automatic)",
        "monthly_charges": 105.25,
        "total_charges": 5046.0,
    }

    normalize_dependent_service_values(values, values["phone_service"], values["internet_service"])
    payload = build_payload(values)

    assert payload["multiple_lines"] == "No phone service"
    assert all(payload[field] == "No internet service" for field in INTERNET_ADD_ON_FIELDS)
    assert CustomerInput.model_validate(payload)


def test_select_labels_are_translated_without_changing_contract_values():
    expected_labels = {
        "Yes": "Sim",
        "No": "Não",
        "Female": "Feminino",
        "Male": "Masculino",
        "Fiber optic": "Fibra óptica",
        "No internet service": "Sem serviço de internet",
        "Month-to-month": "Mensal",
        "Credit card (automatic)": "Cartão de crédito (automático)",
    }

    for value, label in expected_labels.items():
        assert PT_BR_LABELS[value] == label
        assert format_option(value) == label


def test_prediction_history_is_newest_first_and_limited_to_ten_entries():
    history = []
    payload = {"customer_id": "TEST-001"}
    result = {
        "customer_id": "TEST-001",
        "prediction_label": "No",
        "churn_probability": 0.1,
        "confidence": 0.9,
    }

    for index in range(MAX_PREDICTION_HISTORY + 2):
        history = add_prediction_history(
            history,
            payload | {"customer_id": f"TEST-{index:03d}"},
            result | {"customer_id": f"TEST-{index:03d}"},
            datetime(2026, 1, 1, 12, 0, index, tzinfo=timezone.utc),
        )

    assert len(history) == MAX_PREDICTION_HISTORY
    assert history[0]["result"]["customer_id"] == "TEST-011"
    assert history[-1]["result"]["customer_id"] == "TEST-002"
    assert history[0]["payload"]["customer_id"] == "TEST-011"


def test_reference_links_use_api_base_url_and_repository_url():
    links = build_reference_links("http://api.example/", "https://docs.example/")

    assert links["api"] == {
        "label": "Documentação da API",
        "url": "http://api.example/docs",
        "enabled": True,
    }
    assert links["github"]["url"] == GITHUB_REPOSITORY_URL
    assert links["mkdocs"] == {
        "label": "Documentação do projeto",
        "url": "https://docs.example",
        "enabled": True,
    }


def test_mkdocs_link_is_disabled_without_an_environment_url():
    links = build_reference_links("http://api.example", None)

    assert links["mkdocs"]["url"] == ""
    assert links["mkdocs"]["enabled"] is False
