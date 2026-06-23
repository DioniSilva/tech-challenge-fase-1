from unittest.mock import Mock, patch

import pytest
import requests

from ui.client import (
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
    get_health,
    predict,
)

API_BASE_URL = "http://api.example"


def make_response(status_code, payload=None, text=""):
    response = Mock(status_code=status_code, ok=200 <= status_code < 300, text=text)
    response.json.return_value = payload
    return response


@patch("ui.client.requests.request")
def test_get_health_returns_json_from_health_endpoint(request):
    request.return_value = make_response(200, {"status": "healthy", "version": "1.0.0"})

    health = get_health(f"{API_BASE_URL}/")

    assert health["status"] == "healthy"
    request.assert_called_once_with("GET", f"{API_BASE_URL}/api/v1/health", timeout=10)


@patch("ui.client.requests.request")
def test_predict_posts_payload(request):
    request.return_value = make_response(200, {"prediction_label": "No"})
    payload = {"customer_id": "TEST-001"}

    prediction = predict(API_BASE_URL, payload)

    assert prediction["prediction_label"] == "No"
    request.assert_called_once_with(
        "POST", f"{API_BASE_URL}/api/v1/predict", timeout=10, json=payload
    )


@pytest.mark.parametrize(
    ("exception", "expected_exception"),
    [
        (requests.Timeout(), ApiTimeoutError),
        (requests.ConnectionError(), ApiConnectionError),
    ],
)
@patch("ui.client.requests.request")
def test_client_translates_connection_errors(request, exception, expected_exception):
    request.side_effect = exception

    with pytest.raises(expected_exception):
        get_health(API_BASE_URL)


@patch("ui.client.requests.request")
def test_client_exposes_fastapi_validation_details(request):
    request.return_value = make_response(
        422,
        {"detail": [{"loc": ["body", "total_charges"], "msg": "Field required"}]},
    )

    with pytest.raises(ApiResponseError, match="total_charges: Field required") as error:
        predict(API_BASE_URL, {})

    assert error.value.status_code == 422


@patch("ui.client.requests.request")
def test_client_exposes_server_error(request):
    request.return_value = make_response(500, {"detail": "Internal server error"})

    with pytest.raises(ApiResponseError, match="Internal server error") as error:
        get_health(API_BASE_URL)

    assert error.value.status_code == 500
