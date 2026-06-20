"""
Aplicação FastAPI principal - Ponto de entrada da API.
Configura e inicia o servidor FastAPI com todos os roteadores.
"""
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import api_router
from core.config import settings
from utils.app_logging import (clear_request_context, configurar_logging,
                               logger, set_request_context)

# Configurar logging da API com saída JSON estruturada
configurar_logging(json_formatter=True, service_name="telco-churn-API")


# Função chamada ao iniciar a aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de contexto para startup e shutdown da aplicação.

    Startup:
    - Configura logging
    - Valida modelo disponível

    Shutdown:
    - Cleanup se necessário
    """
    # Startup
    logger.info(f"Iniciando {settings.app_name} v{settings.app_version}")
    logger.info(f"Modo debug: {settings.debug}")

    yield

    # Shutdown
    logger.info(f"Encerrando {settings.app_name}")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para predição de churn de clientes Telco",
    lifespan=lifespan,
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    client_ip = request.client.host if request.client else ""
    endpoint = request.url.path

    tokens = set_request_context(
        request_id=request_id,
        client_ip=client_ip,
        endpoint=endpoint,
    )

    try:
        response = await call_next(request)
        return response
    finally:
        clear_request_context(tokens)


# Incluir roteadores
app.include_router(
    api_router,
    prefix=settings.api_prefix,
)


# Root endpoint
@app.get(
    "/",
    summary="API Root",
    description="Retorna informações sobre a API",
    tags=["Root"],
)
def read_root():
    """
    Endpoint raiz da API.

    Returns:
        Informações sobre a API
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "predict": "/api/v1/predict",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
    )
