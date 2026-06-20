"""
Schemas (DTOs) para validação de dados de entrada/saída.
Utiliza Pydantic para validação automática.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomerInput(BaseModel):
    """
    Schema para entrada de dados de um cliente.
    Representa as features do dataset IBM Telco.
    """

    # Identificação
    customer_id: str = Field(..., description="ID do cliente")
    count: int = Field(1, description="Contagem (padrão: 1)")

    # Localização
    country: str = Field(..., description="País do cliente")
    state: str = Field(..., description="Estado/Região")
    city: str = Field(..., description="Cidade")
    zip_code: int = Field(..., description="CEP")
    latitude: float = Field(..., description="Latitude da localização")
    longitude: float = Field(..., description="Longitude da localização")

    # Dados Pessoais
    gender: str = Field(..., description="Gênero (Male/Female)")
    senior_citizen: str = Field(..., description="Senior Citizen (Yes/No)")
    partner: str = Field(..., description="Possui parceiro (Yes/No)")
    dependents: str = Field(..., description="Possui dependentes (Yes/No)")

    # Tenure
    tenure_months: int = Field(..., ge=0, description="Meses de permanência")

    # Serviços Telefônicos
    phone_service: str = Field(..., description="Serviço de telefone (Yes/No)")
    multiple_lines: str = Field(..., description="Múltiplas linhas (Yes/No/No phone service)")

    # Serviços de Internet
    internet_service: str = Field(..., description="Tipo de Internet (DSL/Fiber optic/No)")
    online_security: str = Field(..., description="Online Security (Yes/No/No internet service)")
    online_backup: str = Field(..., description="Online Backup (Yes/No/No internet service)")
    device_protection: str = Field(
        ..., description="Device Protection (Yes/No/No internet service)"
    )
    tech_support: str = Field(..., description="Tech Support (Yes/No/No internet service)")
    streaming_tv: str = Field(..., description="Streaming TV (Yes/No/No internet service)")
    streaming_movies: str = Field(..., description="Streaming Movies (Yes/No/No internet service)")

    # Contrato
    contract: str = Field(..., description="Tipo de contrato (Month-to-month/One year/Two year)")
    paperless_billing: str = Field(..., description="Fatura sem papel (Yes/No)")
    payment_method: str = Field(..., description="Método de pagamento")

    # Charges
    monthly_charges: float = Field(..., ge=0, description="Cobrança mensal em $")
    total_charges: str = Field(..., description="Cobrança total em $")

    # Churn Info (Usado para treinamento, mas opcional em predição)
    churn_label: Optional[str] = Field(None, description="Label de Churn (Yes/No)")
    churn_value: Optional[int] = Field(None, description="Valor de Churn (0/1)")
    churn_score: Optional[int] = Field(None, description="Score de Churn")
    cltv: Optional[int] = Field(None, description="Customer Lifetime Value")
    churn_reason: Optional[str] = Field(None, description="Motivo do Churn")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": "5575-GNVDE",
                "count": 1,
                "country": "United States",
                "state": "California",
                "city": "Los Angeles",
                "zip_code": 90001,
                "latitude": 34.09,
                "longitude": -118.26,
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
                "total_charges": "5046.00",
                "churn_label": "No",
                "churn_value": 0,
                "churn_score": 20,
                "cltv": 5046,
                "churn_reason": None,
            }
        }
    )


class PredictionResponse(BaseModel):
    """
    Schema para resposta de predição.
    """

    customer_id: str = Field(..., description="ID do cliente")
    prediction: int = Field(..., description="Predição (0=Não churn, 1=Churn)")
    prediction_label: str = Field(..., description="Label da predição (Yes/No)")
    prediction_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Probabilidade de churn"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiança da predição (max prob)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": "5575-GNVDE",
                "prediction": 0,
                "prediction_label": "No",
                "prediction_probability": 0.25,
                "confidence": 0.75,
            }
        }
    )


class HealthResponse(BaseModel):
    """Schema para resposta de health check."""

    status: str = Field(..., description="Status da aplicação (healthy/unhealthy)")
    message: str = Field(..., description="Mensagem descritiva")
    version: str = Field(..., description="Versão da aplicação")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "message": "API is running correctly",
                "version": "1.0.0",
            }
        }
    )
