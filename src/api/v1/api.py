"""
Agregador de roteadores - API v1.
Reúne todos os roteadores da versão 1 da API.
"""
from fastapi import APIRouter
from .endpoints.predict import router as predict_router


# Criar roteador raiz da v1
api_router = APIRouter()

# Incluir todos os roteadores da v1
api_router.include_router(predict_router)


__all__ = ["api_router"]
