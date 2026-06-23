import asyncio
from unittest.mock import Mock

from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

import api_main


def test_app_metadata_uses_settings():
    assert api_main.app.title == api_main.settings.app_name
    assert api_main.app.version == api_main.settings.app_version
    assert api_main.app.description == "API para predição de churn de clientes Telco"


def test_app_includes_cors_middleware_allowing_all_origins():
    cors_middleware = next(
        middleware
        for middleware in api_main.app.user_middleware
        if middleware.cls is CORSMiddleware
    )

    assert cors_middleware.kwargs["allow_origins"] == ["*"]
    assert cors_middleware.kwargs["allow_credentials"] is True
    assert cors_middleware.kwargs["allow_methods"] == ["*"]
    assert cors_middleware.kwargs["allow_headers"] == ["*"]


def test_read_root_returns_api_information():
    response = api_main.read_root()

    assert response == {
        "name": api_main.settings.app_name,
        "version": api_main.settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "predict": "/api/v1/predict",
        },
    }


def test_request_logging_middleware_sets_and_clears_context(monkeypatch):
    tokens = ("request", "client", "endpoint", "start")
    set_request_context = Mock(return_value=tokens)
    clear_request_context = Mock()

    monkeypatch.setattr(api_main.uuid, "uuid4", Mock(return_value="fixed-request-id"))
    monkeypatch.setattr(api_main, "set_request_context", set_request_context)
    monkeypatch.setattr(api_main, "clear_request_context", clear_request_context)

    client = TestClient(api_main.app)

    response = client.get("/")

    assert response.status_code == 200
    set_request_context.assert_called_once_with(
        request_id="fixed-request-id",
        client_ip="testclient",
        endpoint="/",
    )
    clear_request_context.assert_called_once_with(tokens)


def test_request_logging_middleware_clears_context_when_endpoint_raises(monkeypatch):
    tokens = ("request", "client", "endpoint", "start")
    clear_request_context = Mock()

    monkeypatch.setattr(api_main, "set_request_context", Mock(return_value=tokens))
    monkeypatch.setattr(api_main, "clear_request_context", clear_request_context)

    @api_main.app.get("/__test_error")
    def _raise_error():
        raise RuntimeError("boom")

    client = TestClient(api_main.app, raise_server_exceptions=False)

    response = client.get("/__test_error")

    assert response.status_code == 500
    clear_request_context.assert_called_once_with(tokens)


def test_lifespan_logs_startup_and_shutdown(monkeypatch):
    logger = Mock()
    monkeypatch.setattr(api_main, "logger", logger)

    async def run_lifespan():
        async with api_main.lifespan(api_main.app):
            logger.info("inside lifespan")

    asyncio.run(run_lifespan())

    logger.info.assert_any_call(
        f"Iniciando {api_main.settings.app_name} v{api_main.settings.app_version}"
    )
    logger.info.assert_any_call(f"Modo debug: {api_main.settings.debug}")
    logger.info.assert_any_call(f"Encerrando {api_main.settings.app_name}")
