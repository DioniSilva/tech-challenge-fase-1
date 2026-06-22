"""
Endpoints da API v1 - Predict e Health endpoints.
Responsáveis por receber e responder requisições HTTP.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from core.config import settings
from schemas import CustomerInput, HealthResponse, PredictionResponse
from services import PredictService, get_predict_service
from utils.app_logging import logger

# Criar roteador da v1
router = APIRouter(prefix="/v1", tags=["v1"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Verifica o status da aplicação e disponibilidade do modelo",
)
def health_check(
    predict_service: PredictService = Depends(get_predict_service),
) -> HealthResponse:
    """
    Endpoint de health check.

    Verifica:
    - Se a aplicação está rodando
    - Se o modelo está carregado

    Returns:
        HealthResponse: Status da aplicação

    Raises:
        HTTPException: Se o serviço está indisponível
    """
    logger.info("Health check solicitado")

    if predict_service.is_healthy():
        return HealthResponse(
            status="healthy",
            message="API is running correctly and model is loaded",
            version=settings.app_version,
        )
    else:
        logger.error("Serviço não saudável - modelo não carregado")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Service unavailable.",
        )


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Churn",
    description=(
        "Executa a predição de churn com as 20 features aceitas pelo modelo. "
        "Campos extras, tipos incompatíveis e combinações de serviços incoerentes são rejeitados."
    ),
)
def predict(
    customer: CustomerInput,
    predict_service: PredictService = Depends(get_predict_service),
) -> PredictionResponse:
    """
    Endpoint de predição de churn.

    Recebe dados de um cliente e retorna a predição de churn.

    Args:
        customer: Dados do cliente (CustomerInput)
        predict_service: Serviço de predição (injetado)

    Returns:
        PredictionResponse: Resultado da predição

    Raises:
        HTTPException: Se houver erro na predição ou modelo não carregado
    """
    logger.info(f"Predição solicitada para cliente: {customer.customer_id}")

    try:
        # Verificar se serviço está disponível
        if not predict_service.is_healthy():
            logger.error("Modelo não carregado")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded. Service unavailable.",
            )

        # Executar predição
        prediction = predict_service.predict(customer)

        logger.info("Predição realizada com sucesso")

        return prediction

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during prediction",
        )
