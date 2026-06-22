"""Cliente HTTP da interface para a API de predição."""

from __future__ import annotations

from typing import Any

import requests

DEFAULT_API_BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT_SECONDS = 10


class ApiError(Exception):
    """Erro retornado ou ocorrido ao acessar a API de inferência."""


class ApiConnectionError(ApiError):
    """A API não pôde ser alcançada."""


class ApiTimeoutError(ApiError):
    """A API não respondeu no tempo esperado."""


class ApiResponseError(ApiError):
    """A API respondeu com um status HTTP de erro."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code


def _endpoint(api_base_url: str, path: str) -> str:
    return f"{api_base_url.rstrip('/')}{path}"


def _error_detail(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
    except ValueError:
        return response.text or "A API retornou uma resposta inválida."

    if isinstance(detail, list):
        messages = []
        for error in detail:
            location = ".".join(str(part) for part in error.get("loc", [])[1:])
            message = error.get("msg", "Valor inválido")
            messages.append(f"{location}: {message}" if location else message)
        return " | ".join(messages)
    if isinstance(detail, str):
        return detail
    return "A API retornou um erro sem detalhes."


def _request(method: str, url: str, **kwargs: Any) -> dict[str, Any]:
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT_SECONDS, **kwargs)
    except requests.Timeout as error:
        raise ApiTimeoutError("A API demorou mais de 10 segundos para responder.") from error
    except requests.RequestException as error:
        raise ApiConnectionError("Não foi possível conectar à API de predição.") from error

    if not response.ok:
        raise ApiResponseError(response.status_code, _error_detail(response))

    try:
        return response.json()
    except ValueError as error:
        raise ApiResponseError(response.status_code, "A API retornou JSON inválido.") from error


def get_health(api_base_url: str) -> dict[str, Any]:
    """Obtém o estado do backend de predição."""
    return _request("GET", _endpoint(api_base_url, "/api/v1/health"))


def predict(api_base_url: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Envia um cliente ao endpoint de predição."""
    return _request("POST", _endpoint(api_base_url, "/api/v1/predict"), json=payload)
