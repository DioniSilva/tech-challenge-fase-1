"""
Aplicação FastAPI principal - Ponto de entrada da API.
Configura e inicia o servidor FastAPI com todos os roteadores.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils.app_logging import configurar_logging, logger
from core.config import settings
from api.v1.api import api_router


# Configurar logging
configurar_logging()


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
